"""Run one graph-only optimization step on entirely synthetic data."""

from __future__ import annotations

import sys
from pathlib import Path

import torch
from torch.nn import functional as F

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.models import RiskAwareGraphModel  # noqa: E402


def ring_edges(node_count: int, offset: int) -> torch.Tensor:
    targets = torch.arange(node_count)
    peers = (targets + offset) % node_count
    return torch.stack([peers, targets])


def main() -> None:
    torch.manual_seed(7)
    node_count, history_steps = 24, 2
    source_dims = {"financial": 12, "mda_text": 8, "self_history": 4, "risk": 3}
    relation_names = ("shared_auditor", "investment", "related_party")
    current = {name: torch.randn(node_count, dim) for name, dim in source_dims.items()}
    history = {
        name: torch.randn(node_count, history_steps, dim) for name, dim in source_dims.items()
    }
    history_mask = torch.ones(node_count, history_steps, dtype=torch.bool)
    history_mask[:4, 0] = False
    history_mask[:2, 1] = False
    latent_risk = current["financial"][:, :3].sum(dim=1) + 0.5 * current["risk"].sum(dim=1)
    labels = (latent_risk > latent_risk.median()).float()
    relations = {
        "shared_auditor": ring_edges(node_count, 1),
        "investment": ring_edges(node_count, 3),
        "related_party": ring_edges(node_count, 5),
    }

    model = RiskAwareGraphModel(
        source_dims,
        relation_names,
        hidden_dim=16,
        relation_dim=4,
        freeze_intrinsic=True,
    )
    optimizer = torch.optim.Adam(model.graph_parameters(), lr=1e-2)
    model.train()
    logits, details = model(current, history, history_mask, relations)
    initial_loss = F.binary_cross_entropy_with_logits(logits, labels)
    initial_identity_error = details["delta_h_graph"].abs().max().item()
    optimizer.zero_grad()
    initial_loss.backward()
    optimizer.step()
    updated_logits, updated = model(current, history, history_mask, relations)
    updated_loss = F.binary_cross_entropy_with_logits(updated_logits, labels)

    print("Synthetic demo completed")
    print(f"nodes={node_count}, relations={len(relation_names)}")
    print(f"initial graph-residual max abs={initial_identity_error:.6f}")
    print(f"loss before step={initial_loss.item():.6f}")
    print(f"loss after step={updated_loss.item():.6f}")
    print(f"mean NULL attention={updated['null_attention'].mean().item():.6f}")


if __name__ == "__main__":
    main()
