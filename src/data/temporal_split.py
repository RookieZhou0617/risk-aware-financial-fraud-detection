"""Fail-closed helpers for rolling temporal evaluation and cross-fitting."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class TemporalFold:
    """An expanding-window split with validation strictly before test."""

    train_years: tuple[int, ...]
    validation_year: int
    test_year: int

    def __post_init__(self) -> None:
        if not self.train_years:
            raise ValueError("train_years must not be empty")
        if max(self.train_years) >= self.validation_year or self.validation_year >= self.test_year:
            raise ValueError("required ordering is train < validation < test")


def expanding_window_splits(
    years: Iterable[int], *, minimum_train_years: int = 3
) -> tuple[TemporalFold, ...]:
    """Create consecutive expanding folds from sorted, gap-free years."""
    ordered = _validated_years(years)
    if minimum_train_years < 1:
        raise ValueError("minimum_train_years must be positive")
    if len(ordered) < minimum_train_years + 2:
        raise ValueError("not enough years for train, validation, and test")
    return tuple(
        TemporalFold(ordered[:index], ordered[index], ordered[index + 1])
        for index in range(minimum_train_years, len(ordered) - 1)
    )


def cross_fit_training_folds(
    available_years: Iterable[int], *, target_year: int, minimum_train_years: int = 2
) -> tuple[TemporalFold, ...]:
    """Build historical cross-fit folds without using the target year or future.

    Every returned test year is strictly earlier than ``target_year``. These
    folds can produce out-of-fold risk estimates for a historical risk bank.
    """
    historical = tuple(year for year in _validated_years(available_years) if year < target_year)
    if target_year in historical:
        raise AssertionError("target year entered historical folds")
    folds = expanding_window_splits(historical, minimum_train_years=minimum_train_years)
    if any(fold.test_year >= target_year for fold in folds):
        raise AssertionError("cross-fitting accessed the target or a future year")
    return folds


def _validated_years(years: Iterable[int]) -> tuple[int, ...]:
    ordered = tuple(sorted(int(year) for year in years))
    if len(ordered) != len(set(ordered)):
        raise ValueError("years must be unique")
    if any(right != left + 1 for left, right in zip(ordered, ordered[1:])):
        raise ValueError("years must be consecutive")
    return ordered
