# To initialize the test, copy the following text to your OS's command window: python -m unittest test_sequence_stats.py
# Make sure that the path is set to the directory that holds both the test file (test_sequence_stats.py) and the program file (sequence_stats.py).

import unittest
from collections import Counter
from sequence_stats import calculate_statistics, read_file
import os

class TestSequenceStats(unittest.TestCase):

    def test_calculate_statistics_actg_only(self):
        sequence = "AAACCCGGGTTT"
        stats = calculate_statistics(sequence)
        
        self.assertEqual(stats["total"], 12)
        self.assertEqual(stats["character_count"], Counter({"A": 3, "C": 3, "G": 3, "T": 3}))
        self.assertAlmostEqual(stats["percentages"]["A"], 25.0)
        self.assertAlmostEqual(stats["percentages"]["C"], 25.0)
        self.assertAlmostEqual(stats["percentages"]["G"], 25.0)
        self.assertAlmostEqual(stats["percentages"]["T"], 25.0)
        self.assertEqual(stats["character_count"]["Unknown"], 0)
        self.assertAlmostEqual(stats["percentages"]["Unknown"], 0.0)

    def test_calculate_statistics_with_unknown(self):
        sequence = "AAACCCGGGTTTXXX"
        stats = calculate_statistics(sequence)

        self.assertEqual(stats["total"], 15)
        self.assertEqual(stats["character_count"], Counter({"A": 3, "C": 3, "G": 3, "T": 3, "X": 3, "Unknown": 3}))
        self.assertAlmostEqual(stats["percentages"]["A"], 25.0)  # Fixed expected percentage
        self.assertAlmostEqual(stats["percentages"]["C"], 25.0)
        self.assertAlmostEqual(stats["percentages"]["G"], 25.0)
        self.assertAlmostEqual(stats["percentages"]["T"], 25.0)
        self.assertAlmostEqual(stats["percentages"]["Unknown"], 20.0)

    def test_calculate_statistics_empty_sequence(self):
        sequence = ""
        stats = calculate_statistics(sequence)

        self.assertEqual(stats["total"], 0)
        self.assertEqual(stats["character_count"], Counter())
        self.assertEqual(stats["percentages"], {"A": 0, "C": 0, "T": 0, "G": 0, "Unknown": 0})

    def test_read_file(self):
        with open("test_sequence.txt", "w") as f:
            f.write("AAACCCGGGTTTXXX")

        with open("test_sequence.txt", "r") as f:
            sequence = read_file("test_sequence.txt")

        self.assertEqual(sequence, "AAACCCGGGTTTXXX")

    def test_read_file(self):
            # Write the test sequence to the file
            with open("test_sequence.txt", "w") as f:
                f.write("AAACCCGGGTTTXXX")
    
            try:
                with open("test_sequence.txt", "r") as f:
                    sequence = read_file("test_sequence.txt")
                
                self.assertEqual(sequence, "AAACCCGGGTTTXXX")
            finally:
                os.remove("test_sequence.txt")

if __name__ == "__main__":
    unittest.main()
