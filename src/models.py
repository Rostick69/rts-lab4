"""Исходные данные промышленного канала."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Channel:
    bitrate: int
    propagation_ms: float
    processing_ms: float


@dataclass(frozen=True)
class Message:
    name: str
    priority: int
    bits: int
    period_ms: float
    deadline_ms: float
