"""Multi-source intrinsic risk encoder with current-history deviation features."""

from __future__ import annotations

from collections.abc import Mapping

import torch
from torch import Tensor, nn
from torch.nn import functional as F


class MultiSourceRiskEncoder(nn.Module):
    """Encode current observations and strictly prior company history.

    Each source is projected separately. The deviation representation contains
    signed difference, absolute difference, element-wise product, cosine
    similarity, and history availability. Missing histories contribute zeros.
    """

    def __init__(
        self,
        source_dims: Mapping[str, int],
        hidden_dim: int = 32,
        deviation_hidden_dim: int = 64,
    ) -> None:
        super().__init__()
        if not source_dims:
            raise ValueError("source_dims must not be empty")
        self.source_names = tuple(source_dims)
        self.hidden_dim = hidden_dim
        self.projectors = nn.ModuleDict(
            {name: nn.Linear(dim, hidden_dim) for name, dim in source_dims.items()}
        )
        self.source_embeddings = nn.Parameter(torch.zeros(len(source_dims), hidden_dim))
        self.current_query = nn.Parameter(torch.empty(hidden_dim))
        deviation_dim = hidden_dim * 3 + 2
        self.deviation_mlps = nn.ModuleDict(
            {
                name: nn.Sequential(
                    nn.Linear(deviation_dim, deviation_hidden_dim),
                    nn.GELU(),
                    nn.Linear(deviation_hidden_dim, hidden_dim),
                )
                for name in source_dims
            }
        )
        self.deviation_query = nn.Parameter(torch.empty(hidden_dim))
        self.fusion = nn.Sequential(nn.Linear(hidden_dim * 2 + 1, hidden_dim), nn.GELU())
        self.classifier = nn.Linear(hidden_dim, 1)
        nn.init.normal_(self.source_embeddings, std=0.02)
        nn.init.normal_(self.current_query, std=hidden_dim**-0.5)
        nn.init.normal_(self.deviation_query, std=hidden_dim**-0.5)

    def forward(
        self,
        current: Mapping[str, Tensor],
        history: Mapping[str, Tensor],
        history_mask: Tensor,
    ) -> tuple[Tensor, Tensor, dict[str, Tensor]]:
        """Return intrinsic hidden state, probability, and interpretable details.

        ``current[name]`` has shape ``[N, D]``; ``history[name]`` has shape
        ``[N, T, D]``; and ``history_mask`` has shape ``[N, T]``. History must
        contain only point-in-time-available observations.
        """
        self._validate_inputs(current, history, history_mask)
        current_tokens = []
        history_tokens = []
        weights = history_mask.to(dtype=history_mask.dtype).float()
        history_count = weights.sum(dim=1)
        history_available = history_count > 0

        for index, name in enumerate(self.source_names):
            current_token = torch.tanh(
                self.projectors[name](current[name]) + self.source_embeddings[index]
            )
            n_rows, n_steps, _ = history[name].shape
            projected_history = torch.tanh(
                self.projectors[name](history[name].reshape(n_rows * n_steps, -1))
                + self.source_embeddings[index]
            ).reshape(n_rows, n_steps, self.hidden_dim)
            history_token = (projected_history * weights[:, :, None]).sum(dim=1)
            history_token = history_token / history_count.clamp_min(1)[:, None]
            current_tokens.append(current_token)
            history_tokens.append(history_token)

        current_stack = torch.stack(current_tokens, dim=1)
        history_stack = torch.stack(history_tokens, dim=1)
        current_scores = torch.einsum("nsd,d->ns", current_stack, self.current_query)
        current_attention = torch.softmax(current_scores / self.hidden_dim**0.5, dim=1)
        current_state = (current_attention[:, :, None] * current_stack).sum(dim=1)

        signed = current_stack - history_stack
        absolute = signed.abs()
        product = current_stack * history_stack
        cosine = F.cosine_similarity(current_stack, history_stack, dim=2, eps=1e-8)
        availability = history_available.to(current_stack.dtype)[:, None, None]
        relation_features = torch.cat(
            [
                signed,
                absolute,
                product,
                cosine[:, :, None],
                availability.expand(-1, len(self.source_names), -1),
            ],
            dim=2,
        )
        deviation_tokens = torch.stack(
            [
                self.deviation_mlps[name](relation_features[:, index])
                for index, name in enumerate(self.source_names)
            ],
            dim=1,
        ) * availability
        deviation_scores = torch.einsum("nsd,d->ns", deviation_tokens, self.deviation_query)
        deviation_attention = torch.softmax(deviation_scores / self.hidden_dim**0.5, dim=1)
        deviation_state = (deviation_attention[:, :, None] * deviation_tokens).sum(dim=1)

        h0 = self.fusion(
            torch.cat(
                [current_state, deviation_state, history_available[:, None].to(current_stack.dtype)],
                dim=1,
            )
        )
        logit = self.classifier(h0).squeeze(-1)
        probability = torch.sigmoid(logit)
        return h0, probability, {
            "intrinsic_logit": logit,
            "current_attention": current_attention,
            "deviation_attention": deviation_attention,
            "history_available": history_available,
            "cosine": cosine,
        }

    def _validate_inputs(
        self,
        current: Mapping[str, Tensor],
        history: Mapping[str, Tensor],
        history_mask: Tensor,
    ) -> None:
        expected = set(self.source_names)
        if set(current) != expected or set(history) != expected:
            raise ValueError(f"current and history sources must equal {sorted(expected)}")
        if history_mask.ndim != 2:
            raise ValueError("history_mask must have shape [N, T]")
        rows, steps = history_mask.shape
        for name in self.source_names:
            if current[name].ndim != 2 or current[name].shape[0] != rows:
                raise ValueError(f"invalid current tensor for source {name}")
            if history[name].ndim != 3 or history[name].shape[:2] != (rows, steps):
                raise ValueError(f"invalid history tensor for source {name}")
