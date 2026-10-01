"""Software invariants on synthetic inputs; not thesis experiment replication."""

import unittest

import torch
from torch.nn import functional as F

from src.models import RiskAwareGraphModel
from src.models.relational_message import RiskAwareRelationalMessage


class PublicModelTests(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(7)
        self.model = RiskAwareGraphModel({"a": 3, "b": 2}, ["peer"], hidden_dim=8)
        self.current = {"a": torch.randn(5, 3), "b": torch.randn(5, 2)}
        self.history = {"a": torch.randn(5, 2, 3), "b": torch.randn(5, 2, 2)}
        self.mask = torch.ones(5, 2, dtype=torch.bool)
        self.edges = {"peer": torch.tensor([[1, 2, 3, 4, 0], [0, 1, 2, 3, 4]])}

    def forward(self, edges=None):
        return self.model(self.current, self.history, self.mask, self.edges if edges is None else edges)

    def test_initial_residual_exactly_preserves_anchor(self):
        logits, details = self.forward()
        self.assertEqual(details["delta_h_graph"].abs().max().item(), 0)
        torch.testing.assert_close(logits, details["intrinsic_logit"], rtol=0, atol=0)

    def test_graph_step_keeps_anchor_parameters_frozen(self):
        before = {name: p.detach().clone() for name, p in self.model.intrinsic_encoder.named_parameters()}
        optimizer = torch.optim.Adam(self.model.graph_parameters(), lr=0.01)
        self.model.train()
        self.assertFalse(self.model.intrinsic_encoder.training)
        logits, _ = self.forward()
        F.binary_cross_entropy_with_logits(logits, torch.tensor([0., 1., 0., 1., 0.])).backward()
        self.assertIsNotNone(self.model.graph_projection.weight.grad)
        self.assertGreater(self.model.graph_projection.weight.grad.abs().sum().item(), 0)
        optimizer.step()
        for name, parameter in self.model.intrinsic_encoder.named_parameters():
            self.assertIsNone(parameter.grad)
            torch.testing.assert_close(parameter, before[name], rtol=0, atol=0)

    def test_missing_relations_return_anchor_even_after_projection_changes(self):
        with torch.no_grad():
            self.model.graph_projection.weight.fill_(0.5)
        logits, details = self.forward({"peer": torch.empty(2, 0, dtype=torch.long)})
        torch.testing.assert_close(logits, details["intrinsic_logit"], rtol=0, atol=0)
        torch.testing.assert_close(details["null_attention"], torch.ones(5))

    def test_top_half_with_deterministic_ties(self):
        h = torch.ones(8, 3)
        peers = torch.tensor([7, 3, 6, 1, 4, 2, 5])
        targets = torch.zeros(7, dtype=torch.long)
        chosen, _ = RiskAwareRelationalMessage._select_peers(h, peers, targets)
        self.assertEqual(chosen.tolist(), [1, 2, 3, 4])
        for _ in range(10):
            permutation = torch.randperm(7)
            again, _ = RiskAwareRelationalMessage._select_peers(h, peers[permutation], targets[permutation])
            torch.testing.assert_close(chosen, again)

    def test_similarity_precedes_index_and_each_target_keeps_ceil_half(self):
        h = torch.tensor([[1., 0.], [-1., 0.], [0., 1.], [0.8, 0.2], [1., 0.]])
        peers = torch.tensor([1, 2, 3, 4, 0])
        targets = torch.tensor([0, 0, 0, 0, 1])
        chosen, selected_targets = RiskAwareRelationalMessage._select_peers(h, peers, targets)
        self.assertEqual(chosen.tolist(), [4, 3, 0])
        self.assertEqual(selected_targets.tolist(), [0, 0, 1])


if __name__ == "__main__":
    unittest.main()
