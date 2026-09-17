#!/usr/bin/env python3
"""CS 5158/6058 Project 1 - Index of Coincidence and Vigenere cipher."""

from __future__ import annotations

import argparse
import math
import re
from collections import Counter
from pathlib import Path

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ENGLISH_FREQUENCIES = {
    "a": 0.08167, "b": 0.01492, "c": 0.02782, "d": 0.04253,
    "e": 0.12702, "f": 0.02228, "g": 0.02015, "h": 0.06094,
    "i": 0.06966, "j": 0.00153, "k": 0.00772, "l": 0.04025,
    "m": 0.02406, "n": 0.06749, "o": 0.07507, "p": 0.01929,
    "q": 0.00095, "r": 0.05987, "s": 0.06327, "t": 0.09056,
    "u": 0.02758, "v": 0.00978, "w": 0.02360, "x": 0.00150,
    "y": 0.01974, "z": 0.00074,
}


def letters_only(text: str) -> str:
    """Return lowercase ASCII a-z letters, ignoring all other characters."""
    return "".join(re.findall(r"[a-z]", text.lower()))


def read_letters(filename: str | Path) -> str:
    return letters_only(Path(filename).read_text(encoding="utf-8"))


def frequency(text: str) -> dict[str, int]:
    clean = letters_only(text)
    counts = Counter(clean)
    return {letter: counts.get(letter, 0) for letter in ALPHABET}


def ic_from_counts(counts: dict[str, int]) -> float:
    n = sum(counts.values())
    if n < 2:
        return 0.0
    return sum(value * (value - 1) for value in counts.values()) / (n * (n - 1))


def index_of_coincidence(text: str) -> float:
    return ic_from_counts(frequency(text))


def validate_key(key: str) -> str:
    clean = letters_only(key)
    if clean != key.lower() or not 3 <= len(clean) <= 19:
        raise ValueError("The key must contain only letters and have length 3-19.")
    return clean


def encrypt(plaintext: str, key: str) -> str:
    clean = letters_only(plaintext)
    key = validate_key(key)
    output = []
    for index, character in enumerate(clean):
        shift = ord(key[index % len(key)]) - ord("a")
        output.append(chr((ord(character) - ord("a") + shift) % 26 + ord("A")))
    return "".join(output)


def decrypt(ciphertext: str, key: str) -> str:
    clean = letters_only(ciphertext)
    key = validate_key(key)
    output = []
    for index, character in enumerate(clean):
        shift = ord(key[index % len(key)]) - ord("a")
        output.append(chr((ord(character) - ord("a") - shift) % 26 + ord("a")))
    return "".join(output)


def average_column_ic(ciphertext: str, key_length: int) -> float:
    clean = letters_only(ciphertext)
    columns = [clean[offset::key_length] for offset in range(key_length)]
    return sum(index_of_coincidence(column) for column in columns) / key_length


def key_length_evidence(ciphertext: str, english_ic: float, min_len: int, max_len: int):
    """Return candidate lengths. A small penalty favors the fundamental period over multiples."""
    evidence = []
    for length in range(min_len, max_len + 1):
        average_ic = average_column_ic(ciphertext, length)
        score = abs(average_ic - english_ic) + 0.00035 * length
        evidence.append((length, average_ic, score))
    return evidence


def chi_squared_for_shift(column: str, shift: int) -> float:
    n = len(column)
    observed = Counter((ord(char) - ord("a") - shift) % 26 for char in column)
    total = 0.0
    for index, letter in enumerate(ALPHABET):
        expected = ENGLISH_FREQUENCIES[letter] * n
        total += (observed.get(index, 0) - expected) ** 2 / expected
    return total


def recover_key(ciphertext: str, key_length: int):
    clean = letters_only(ciphertext)
    key_letters = []
    all_scores = []
    for position in range(key_length):
        column = clean[position::key_length]
        scores = [(ALPHABET[shift], chi_squared_for_shift(column, shift)) for shift in range(26)]
        scores.sort(key=lambda item: item[1])
        key_letters.append(scores[0][0])
        all_scores.append(scores)
    return "".join(key_letters), all_scores


def attack(ciphertext: str, english_ic: float, min_len: int = 3, max_len: int = 19,
           forced_length: int | None = None, verbose: bool = True):
    clean = letters_only(ciphertext)
    if len(clean) < 100:
        raise ValueError("Ciphertext is too short for a dependable frequency attack.")
    evidence = key_length_evidence(clean, english_ic, min_len, max_len)
    chosen_length = forced_length or min(evidence, key=lambda row: row[2])[0]
    key, letter_scores = recover_key(clean, chosen_length)

    if verbose:
        print("KEY-LENGTH EVIDENCE (smaller selection score is better)")
        print("length  average_IC  distance_from_English_IC  selection_score")
        for length, average_ic, score in evidence:
            marker = "  <-- selected" if length == chosen_length else ""
            print(f"{length:>6}  {average_ic:>10.6f}  {abs(average_ic-english_ic):>24.6f}  {score:>15.6f}{marker}")
        print("\nKEY-LETTER EVIDENCE (chi-square; smaller is better)")
        for position, scores in enumerate(letter_scores, start=1):
            best_five = ", ".join(f"{letter}:{score:.2f}" for letter, score in scores[:5])
            print(f"position {position:>2}: {best_five}  -> {scores[0][0]}")
        print(f"\nRecovered key length: {chosen_length}")
        print(f"Recovered key string: {key}")
    return chosen_length, key, evidence, letter_scores


def save_frequency_plot(counts: dict[str, int], output: str | Path) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit("matplotlib is missing. Run: python -m pip install -r requirements.txt") from exc
    total = sum(counts.values()) or 1
    percentages = [100 * counts[letter] / total for letter in ALPHABET]
    plt.figure(figsize=(11, 5.5))
    bars = plt.bar(list(ALPHABET), percentages, color="#d71920", edgecolor="#7a0c10")
    plt.title("English Letter Frequency Distribution")
    plt.xlabel("Letter")
    plt.ylabel("Frequency (%)")
    plt.grid(axis="y", alpha=0.25)
    for bar, value in zip(bars, percentages):
        plt.text(bar.get_x() + bar.get_width() / 2, value + 0.08, f"{value:.1f}",
                 ha="center", va="bottom", fontsize=7)
    plt.tight_layout()
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output, dpi=180)
    print(f"Frequency plot saved to: {output}")


def cmd_frequency(args):
    text = Path(args.input).read_text(encoding="utf-8")
    clean = letters_only(text)
    counts = frequency(text)
    print(f"Source file: {args.input}")
    print(f"Number of letters analyzed: {len(clean)}")
    print("\nLETTER FREQUENCIES")
    print("letter  count  percentage")
    for letter in ALPHABET:
        percentage = (100 * counts[letter] / len(clean)) if clean else 0
        print(f"{letter:>6}  {counts[letter]:>5}  {percentage:>9.4f}%")
    value = ic_from_counts(counts)
    print(f"\nIndex of Coincidence: {value:.6f}")
    save_frequency_plot(counts, args.plot)
    if args.ic_output:
        Path(args.ic_output).write_text(f"{value:.10f}\n", encoding="utf-8")


def cmd_encrypt(args):
    plaintext = read_letters(args.input)
    if args.limit:
        plaintext = plaintext[:args.limit]
    ciphertext = encrypt(plaintext, args.key)
    print(f"Plaintext length: {len(plaintext)}")
    print(f"Key: {args.key.lower()}")
    print(f"Plaintext: {plaintext}")
    print(f"Ciphertext: {ciphertext}")
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(ciphertext + "\n", encoding="utf-8")
        print(f"Ciphertext saved to: {args.output}")


def cmd_decrypt(args):
    ciphertext = read_letters(args.input).upper()
    if args.limit:
        ciphertext = ciphertext[:args.limit]
    plaintext = decrypt(ciphertext, args.key)
    print(f"Ciphertext length: {len(ciphertext)}")
    print(f"Key: {args.key.lower()}")
    print(f"Ciphertext: {ciphertext}")
    print(f"Plaintext: {plaintext}")
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(plaintext + "\n", encoding="utf-8")


def load_ic(value: str) -> float:
    path = Path(value)
    return float(path.read_text().strip()) if path.exists() else float(value)


def cmd_attack(args):
    ciphertext = read_letters(args.input).upper()
    attack(ciphertext, load_ic(args.english_ic), args.min_length, args.max_length, args.key_length)


def cmd_attack_folder(args):
    folder = Path(args.folder)
    files = sorted(folder.glob("*.txt"))
    if not files:
        raise SystemExit(f"No .txt files found in {folder}")
    results = []
    for file in files:
        clean = read_letters(file).upper()
        try:
            length, key, _, _ = attack(clean, load_ic(args.english_ic), args.min_length,
                                       args.max_length, verbose=False)
            results.append(f"filename: {file.name}    recovered key string: {key}")
        except ValueError as exc:
            results.append(f"filename: {file.name}    ERROR: {exc}")
    report = "\n".join(results) + "\n"
    print("TASK 4 SUMMARY")
    print(report, end="")
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(report, encoding="utf-8")
    print(f"Summary saved to: {args.output}")


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("frequency", help="Task 1: frequency table, plot, and IC")
    p.add_argument("--input", required=True)
    p.add_argument("--plot", default="data/frequency_plot.png")
    p.add_argument("--ic-output", default="data/english_ic.txt")
    p.set_defaults(func=cmd_frequency)

    p = sub.add_parser("encrypt", help="Task 2: Vigenere encryption")
    p.add_argument("--input", required=True)
    p.add_argument("--key", required=True)
    p.add_argument("--limit", type=int)
    p.add_argument("--output")
    p.set_defaults(func=cmd_encrypt)

    p = sub.add_parser("decrypt", help="Task 2: Vigenere decryption")
    p.add_argument("--input", required=True)
    p.add_argument("--key", required=True)
    p.add_argument("--limit", type=int)
    p.add_argument("--output")
    p.set_defaults(func=cmd_decrypt)

    p = sub.add_parser("attack", help="Task 3: recover a Vigenere key")
    p.add_argument("--input", required=True)
    p.add_argument("--english-ic", default="data/english_ic.txt")
    p.add_argument("--min-length", type=int, default=3)
    p.add_argument("--max-length", type=int, default=19)
    p.add_argument("--key-length", type=int, help="Optional known/verified key length")
    p.set_defaults(func=cmd_attack)

    p = sub.add_parser("attack-folder", help="Task 4: attack every .txt file in a folder")
    p.add_argument("--folder", default="data/shared_ciphertexts")
    p.add_argument("--english-ic", default="data/english_ic.txt")
    p.add_argument("--min-length", type=int, default=3)
    p.add_argument("--max-length", type=int, default=19)
    p.add_argument("--output", default="data/task4_results.txt")
    p.set_defaults(func=cmd_attack_folder)
    return parser


def main():
    args = build_parser().parse_args()
    try:
        args.func(args)
    except ValueError as exc:
        raise SystemExit(f"Error: {exc}") from exc


if __name__ == "__main__":
    main()
