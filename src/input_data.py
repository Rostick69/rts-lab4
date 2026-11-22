"""Первый CSV задаёт канал, второй — периодические сообщения."""

import csv
from math import isfinite
from pathlib import Path

from models import Channel, Message


def read_rows(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def load_channel(path):
    rows = read_rows(path)
    if len(rows) != 1:
        raise ValueError("В файле канала нужна одна строка данных")
    row = rows[0]
    channel = Channel(int(row["bitrate"]), float(row["propagation_ms"]),
                      float(row["processing_ms"]))
    if channel.bitrate <= 0:
        raise ValueError("Скорость канала должна быть положительной")
    if not all(isfinite(x) and x >= 0 for x in
               (channel.propagation_ms, channel.processing_ms)):
        raise ValueError("Задержки канала должны быть конечными и неотрицательными")
    return channel


def load_messages(path):
    messages = []
    for row in read_rows(path):
        msg = Message(row["name"].strip(), int(row["priority"]), int(row["bits"]),
                      float(row["period_ms"]), float(row["deadline_ms"]))
        if not msg.name or msg.bits <= 0 or msg.priority < 1:
            raise ValueError("Проверьте имя, размер и приоритет сообщения")
        if not all(isfinite(x) and x > 0 for x in (msg.period_ms, msg.deadline_ms)):
            raise ValueError("Период и дедлайн должны быть конечными и положительными")
        if msg.deadline_ms > msg.period_ms:
            raise ValueError("В модели дедлайн не превышает период")
        messages.append(msg)
    if not messages or len({m.priority for m in messages}) != len(messages):
        raise ValueError("Нужны сообщения с различными приоритетами")
    return sorted(messages, key=lambda msg: msg.priority)
