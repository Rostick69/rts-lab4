"""Практическая работа № 4. Анализ общей шины контроллеров."""

import argparse
from pathlib import Path

from input_data import load_channel, load_messages
from output import show
from results import calculate

DATA = Path(__file__).resolve().parents[1] / "data"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("messages", nargs="?", type=Path, default=DATA / "variant2.csv")
    parser.add_argument("--channel", type=Path, default=DATA / "channel.csv")
    args = parser.parse_args()
    try:
        channel = load_channel(args.channel)
        messages = load_messages(args.messages)
        results = calculate(messages, channel)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(2, f"Ошибка входных данных: {error}\n")
    print(f"Набор: {args.messages.name}. Скорость: {channel.bitrate} бит/с.")
    show(messages, results)


if __name__ == "__main__":
    main()
