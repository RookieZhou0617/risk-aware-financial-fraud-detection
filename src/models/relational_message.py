"""Risk-aware peer messaging without a graph-framework dependency."""

from __future__ import annotations

import torch
from torch import Tensor, nn
from torch.nn import functional as F


class RiskAwareRelationalMessage(nn.Module):
    """Build peer-to-target messages and relation-level evidence summaries."""

    def __init__(self, hidden_dim: int, relation_dim: int) -> None:
        super().__init__()
        input_dim = hidden_dim * 3 + relation_dim + 1
        self.message_mlp = nn.Sequential(
            nn.Linear(input_dim, hidden_dim * 2),
            nn.GELU(),
            nn.Linear(hidden_dim * 2, hidden_dim),
        )

    def forward(
        self,
        h0: Tensor,
        p0: Tensor,
        edge_index: Tensor,
        relation_embedding: Tensor,
    ) -> tuple[Tensor, Tensor, Tensor]:
        """Aggregate peer messages and return statistics for every target node.

        ``edge_index[0]`` contains peer indices and ``edge_index[1]`` target
        indices. Statistics are peer count, similarity mean/std, absolute risk
        gap mean, peer-risk dispersion, and relation-context norm.
        """
        if edge_index.ndim != 2 or edge_index.shape[0] != 2:
            raise ValueError("edge_index must have shape [2, E]")
        node_count, hidden_dim = h0.shape
        peers, targets = edge_index.long()
        context = h0.new_zeros((node_count, hidden_dim))
        statistics = h0.new_zeros((node_count, 6))
        available = torch.zeros(node_count, dtype=torch.bool, device=h0.device)
        if peers.numel() == 0:
            return context, statistics, available
        if peers.min() < 0 or targets.min() < 0 or peers.max() >= node_count or targets.max() >= node_count:
            raise ValueError("edge_index contains an out-of-range node index")

        peer_hidden, target_hidden = h0[peers], h0[targets]
        signed = peer_hidden - target_hidden
        rel = relation_embedding.expand(peers.numel(), -1)
        messages = self.message_mlp(
            torch.cat(
                [peer_hidden, signed, signed.abs(), (p0[peers] - p0[targets])[:, None], rel],
                dim=1,
            )
        )
        ones = h0.new_ones(peers.numel())
        counts = h0.new_zeros(node_count).index_add_(0, targets, ones)
        context.index_add_(0, targets, messages)
        context = context / counts.clamp_min(1)[:, None]
        available = counts > 0

        similarity = F.cosine_similarity(peer_hidden, target_hidden, dim=1, eps=1e-8)
        risk_gap = (p0[peers] - p0[targets]).abs()
        peer_risk = p0[peers]
        sim_sum = h0.new_zeros(node_count).index_add_(0, targets, similarity)
        sim_square_sum = h0.new_zeros(node_count).index_add_(0, targets, similarity.square())
        gap_sum = h0.new_zeros(node_count).index_add_(0, targets, risk_gap)
        risk_sum = h0.new_zeros(node_count).index_add_(0, targets, peer_risk)
        risk_square_sum = h0.new_zeros(node_count).index_add_(0, targets, peer_risk.square())
        denominator = counts.clamp_min(1)
        sim_mean = sim_sum / denominator
        risk_mean = risk_sum / denominator
        sim_std = (sim_square_sum / denominator - sim_mean.square()).clamp_min(0).sqrt()
        risk_std = (risk_square_sum / denominator - risk_mean.square()).clamp_min(0).sqrt()
        statistics = torch.stack(
            [
                torch.log1p(counts),
                sim_mean,
                sim_std,
                gap_sum / denominator,
                risk_std,
                torch.linalg.vector_norm(context, dim=1),
            ],
            dim=1,
        )
        statistics = statistics * available[:, None]
        return context, statistics, available
