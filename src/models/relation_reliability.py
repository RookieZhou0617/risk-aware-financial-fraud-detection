"""Reliability gating and NULL-aware cross-relation fusion."""

from __future__ import annotations

import math

import torch
from torch import Tensor, nn


class RelationReliabilityGate(nn.Module):
    """Estimate a soft reliability score for each node-relation context."""

    def __init__(self, relation_dim: int, hidden_dim: int = 16, prior: float = 0.1) -> None:
        super().__init__()
        if not 0.0 < prior < 1.0:
            raise ValueError("prior must be strictly between zero and one")
        self.network = nn.Sequential(
            nn.Linear(6 + relation_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, 1),
        )
        nn.init.zeros_(self.network[-1].weight)
        nn.init.constant_(self.network[-1].bias, math.log(prior / (1.0 - prior)))

    def forward(self, statistics: Tensor, relation_embeddings: Tensor) -> Tensor:
        return torch.sigmoid(self.network(torch.cat([statistics, relation_embeddings], dim=-1))).squeeze(-1)


class CrossRelationFusion(nn.Module):
    """Fuse relation contexts while allowing the model to select no relation."""

    def __init__(self, hidden_dim: int, relation_dim: int) -> None:
        super().__init__()
        self.attention = nn.Sequential(
            nn.Linear(hidden_dim * 2 + relation_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(
        self,
        h0: Tensor,
        relation_contexts: Tensor,
        relation_embeddings: Tensor,
        available: Tensor,
        reliability: Tensor,
    ) -> tuple[Tensor, Tensor]:
        node_count, relation_count, hidden_dim = relation_contexts.shape
        gated = relation_contexts * reliability[:, :, None]
        null_context = h0.new_zeros((node_count, 1, hidden_dim))
        contexts = torch.cat([gated, null_context], dim=1)
        null_embedding = h0.new_zeros((1, relation_embeddings.shape[-1]))
        embeddings = torch.cat([relation_embeddings, null_embedding], dim=0)
        expanded_h0 = h0[:, None, :].expand(-1, relation_count + 1, -1)
        expanded_embeddings = embeddings[None].expand(node_count, -1, -1)
        scores = self.attention(torch.cat([expanded_h0, contexts, expanded_embeddings], dim=2)).squeeze(-1)
        mask = torch.cat(
            [available, torch.ones((node_count, 1), dtype=torch.bool, device=h0.device)],
            dim=1,
        )
        attention = torch.softmax(scores.masked_fill(~mask, -torch.inf), dim=1)
        graph_context = (attention[:, :, None] * contexts).sum(dim=1)
        return graph_context, attention
