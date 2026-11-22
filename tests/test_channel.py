"""Контрольные примеры. Запуск: python -m unittest discover -s tests."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from input_data import load_channel, load_messages
from models import Message
from results import calculate, meets_deadline


class ChannelTests(unittest.TestCase):
    def setUp(self):
        self.channel = load_channel(ROOT / "data/channel.csv")

    def test_methodical_example(self):
        rows = calculate(load_messages(ROOT / "data/example.csv"), self.channel)
        self.assertEqual([r.transmission for r in rows], [2, 4, 8])
        self.assertEqual([float(r.basic) for r in rows], [2.3, 4.3, 8.3])
        self.assertEqual([float(r.worst) for r in rows], [6.3, 6.3, 14.3])
        self.assertEqual([r.spread for r in rows], [4, 0, 4])

    def test_variant_deadlines(self):
        messages = load_messages(ROOT / "data/variant2.csv")
        rows = calculate(messages, self.channel)
        self.assertEqual([meets_deadline(r, m.deadline_ms)
                          for m, r in zip(messages, rows)], [False, False, True, False])

    def test_single_message_on_deadline(self):
        msg = Message("A", 1, 500, 10, 1.3)
        row, = calculate([msg], self.channel)
        self.assertEqual(row.spread, 0)
        self.assertTrue(meets_deadline(row, msg.deadline_ms))

    def test_overload(self):
        msg = Message("A", 1, 1000, 1, 1)
        with self.assertRaisesRegex(ValueError, "перегружен"):
            calculate([msg], self.channel)
