"""Таблица для показа результатов в консоли."""

from results import meets_deadline


def show(messages, results):
    headings = ["Сообщение", "Пр.", "Бит", "Передача", "Базовая", "Максимум",
                "Джиттер", "Дедлайн", "Успело"]
    rows = [headings]
    missed = []
    for msg, result in zip(messages, results):
        ok = meets_deadline(result, msg.deadline_ms)
        if not ok:
            missed.append(msg.name)
        times = (result.transmission, result.basic, result.worst,
                 result.spread, msg.deadline_ms)
        rows.append([msg.name, str(msg.priority), str(msg.bits),
                     *(f"{float(t):.2f}" for t in times), "да" if ok else "нет"])
    widths = [max(map(len, col)) for col in zip(*rows)]
    print("Все значения времени указаны в мс. Приоритет 1 — высший.")
    for row in rows:
        print(" | ".join(value.ljust(w) for value, w in zip(row, widths)))
    if missed:
        print("Дедлайн превышен:", ", ".join(missed))
    else:
        print("Все сообщения укладываются в дедлайн.")
