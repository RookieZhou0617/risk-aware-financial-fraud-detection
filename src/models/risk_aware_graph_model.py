"""Anchor-preserving multi-source risk-aware graph model."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import torch
from torch import Tensor, nn

from .multi_source_risk_encoder import MultiSourceRiskEncoder
from .relation_reliability import CrossRelationFusion, RelationReliabilityGate
from .relational_message import RiskAwareRelationalMessage


class RiskAwareGraphModel(nn.Module):
    """Add selective relational evidence to a stable intrinsic risk anchor.

    The graph residual projection is initialized to zero, so the initial graph
    model exactly matches the intrinsic prediction. Set ``freeze_intrinsic`` to
    protect a pretrained anchor while fitting only the graph branch.
    """

    def __init__(
        self,
        source_dims: Mapping[str, int],
        relation_names: Sequence[str],
        hidden_dim: int = 32,
        relation_dim: int = 8,
        gate_prior: float = 0.1,
        freeze_intrinsic: bool = True,
    ) -> None:
        super().__init__()
        if not relation_names or len(relation_names) != len(set(relation_names)):
            raise ValueError("relation_names must be non-empty and unique")
        self.relation_names = tuple(relation_names)
        self.intrinsic_encoder = MultiSourceRiskEncoder(source_dims, hidden_dim=hidden_dim)
        self.relation_embeddings = nn.Embedding(len(relation_names), relation_dim)
        self.relational_message = RiskAwareRelationalMessage(hidden_dim, relation_dim)
        self.reliability_gate = RelationReliabilityGate(relation_dim, prior=gate_prior)
        self.relation_fusion = CrossRelationFusion(hidden_dim, relation_dim)
        self.graph_projection = nn.Linear(hidden_dim, hidden_dim, bias=False)
        nn.init.zeros_(self.graph_projection.weight)
        self.freeze_intrinsic = freeze_intrinsic
        if freeze_intrinsic:
            self.set_intrinsic_trainable(False)

    def set_intrinsic_trainable(self, trainable: bool) -> None:
        """Freeze or unfreeze the intrinsic encoder and classifier."""
        self.freeze_intrinsic = not trainable
        for parameter in self.intrinsic_encoder.parameters():
            parameter.requires_grad_(trainable)
            if not trainable:
                parameter.grad = None

    def train(self, mode: bool = True) -> "RiskAwareGraphModel":
        super().train(mode)
        if self.freeze_intrinsic:
            self.intrinsic_encoder.eval()
        return self

    def graph_parameters(self):
        """Iterate only over parameters outside the intrinsic anchor."""
        return (
            parameter
            for name, parameter in self.named_parameters()
            if not name.startswith("intrinsic_encoder.")
        )

    def forward(
        self,
        current: Mapping[str, Tensor],
        history: Mapping[str, Tensor],
        history_mask: Tensor,
        relations: Mapping[str, Tensor],
    ) -> tuple[Tensor, dict[str, Tensor]]:
        if set(relations) != set(self.relation_names):
            raise ValueError("relations must match the configured relation_names")
        if self.freeze_intrinsic:
            with torch.no_grad():
                h0, p0, intrinsic_details = self.intrinsic_encoder(current, history, history_mask)
            h0, p0 = h0.detach(), p0.detach()
        else:
            h0, p0, intrinsic_details = self.intrinsic_encoder(current, history, history_mask)

        contexts, statistics, availability = [], [], []
        embeddings = self.relation_embeddings.weight
        for index, name in enumerate(self.relation_names):
            context, stats, available = self.relational_message(
                h0, p0, relations[name], embeddings[index]
            )
            contexts.append(context)
            statistics.append(stats)
            availability.append(available)
        relation_contexts = torch.stack(contexts, dim=1)
        relation_statistics = torch.stack(statistics, dim=1)
        relation_available = torch.stack(availability, dim=1)
        expanded_embeddings = embeddings[None].expand(h0.shape[0], -1, -1)
        reliability = self.reliability_gate(relation_statistics, expanded_embeddings)
        reliability = reliability * relation_available.to(reliability.dtype)
        graph_context, relation_attention = self.relation_fusion(
            h0, relation_contexts, embeddings, relation_available, reliability
        )
        delta_h_graph = self.graph_projection(graph_context)
        h_final = h0 + delta_h_graph
        logits = self.intrinsic_encoder.classifier(h_final).squeeze(-1)
        return logits, {
            **intrinsic_details,
            "h_intrinsic": h0,
            "p_intrinsic": p0,
            "relation_statistics": relation_statistics,
            "relation_reliability": reliability,
            "relation_attention": relation_attention[:, :-1],
            "null_attention": relation_attention[:, -1],
            "graph_context": graph_context,
            "delta_h_graph": delta_h_graph,
            "h_final": h_final,
        }
