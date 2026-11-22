"""Итоговые показатели по каждому сообщению."""

from dataclasses import dataclass
from fractions import Fraction

from arbitration import arbitration_time, delivery_samples
from timing import delivery_delay, jitter, transmission_time


@dataclass(frozen=True)
class Result:
    transmission: Fraction
    basic: Fraction
    worst: Fraction
    spread: Fraction


def meets_deadline(msg, deadline):
    """Сравнивает максимальную задержку из результата с дедлайном."""
    return msg.worst <= Fraction(str(deadline))


def calculate(messages, channel):
    samples = delivery_samples(tuple(messages), channel)
    return [Result(transmission_time(m, channel), delivery_delay(m, channel),
                   arbitration_time(m, messages, channel), jitter(samples[m]))
            for m in messages]
