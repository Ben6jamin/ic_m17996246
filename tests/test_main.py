import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import decrypt, encrypt, frequency, index_of_coincidence


class ProjectTests(unittest.TestCase):
    def test_frequency_ignores_nonletters_and_lowercases(self):
        counts = frequency("Aa! B2z")
        self.assertEqual(counts["a"], 2)
        self.assertEqual(counts["b"], 1)
        self.assertEqual(counts["z"], 1)
        self.assertEqual(sum(counts.values()), 4)

    def test_known_vigenere_example(self):
        self.assertEqual(encrypt("attackatdawn", "lemon"), "LXFOPVEFRNHR")
        self.assertEqual(decrypt("LXFOPVEFRNHR", "lemon"), "attackatdawn")

    def test_ic_for_identical_letters(self):
        self.assertEqual(index_of_coincidence("aaaaaaaaaa"), 1.0)


if __name__ == "__main__":
    unittest.main()
