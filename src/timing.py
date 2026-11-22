"""Расчёт времени в миллисекундах."""

from fractions import Fraction


def transmission_time(msg, channel):
    return Fraction(1000 * msg.bits, channel.bitrate)


def delivery_delay(msg, channel):
    return (transmission_time(msg, channel) + Fraction(str(channel.propagation_ms))
            + Fraction(str(channel.processing_ms)))


def jitter(delays):
    """Разность между максимальной и минимальной задержками одного потока."""
    return max(delays) - min(delays)
