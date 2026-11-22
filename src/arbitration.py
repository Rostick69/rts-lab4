"""Арбитраж на общей шине, передача начатого сообщения не прерывается."""

from fractions import Fraction
from functools import lru_cache
from heapq import heappop, heappush
from math import lcm

from timing import delivery_delay, transmission_time


@lru_cache(maxsize=1)
def delivery_samples(messages, channel):
    periods = [Fraction(str(m.period_ms)) for m in messages]
    # Общая единица позволяет найти гиперпериод и для дробных периодов.
    scale = lcm(*(p.denominator for p in periods))
    horizon = Fraction(lcm(*(int(p * scale) for p in periods)), scale)
    count = sum(int(horizon / p) for p in periods)
    if count > 100000:
        raise ValueError("В гиперпериоде больше 100 000 сообщений")
    load = sum(transmission_time(m, channel) / p for m, p in zip(messages, periods))
    if load > 1:
        raise ValueError("Канал перегружен: очередь растёт от периода к периоду")

    releases = []
    for msg, period in zip(messages, periods):
        for i in range(int(horizon / period)):
            releases.append((i * period, msg.priority, msg))
    releases.sort(key=lambda event: (event[0], event[1]))

    samples = {m: [] for m in messages}
    queue = []
    index = 0
    now = Fraction(0)
    while index < len(releases) or queue:
        if not queue:
            now = max(now, releases[index][0])
        while index < len(releases) and releases[index][0] <= now:
            released, priority, msg = releases[index]
            heappush(queue, (priority, released, msg))
            index += 1
        _, released, msg = heappop(queue)
        samples[msg].append(now - released + delivery_delay(msg, channel))
        now += transmission_time(msg, channel)
    return samples


def arbitration_time(msg, all_msgs, channel):
    return max(delivery_samples(tuple(all_msgs), channel)[msg])
