# CS 5158/6058 Project 1: Index of Coincidence

This repository is personalized for **BENJAMIN ISHIMWE**, UCID **M17996246**.

## Required project structure

```text
ic_m17996246/
├── src/          Python source code
├── build/        Generated executable archive ic_project.pyz
├── data/         Inputs, generated ciphertexts, plot, and Task 4 results
└── report.pdf    Draft report; replace it after inserting laptop screenshots
```

The included `report.pdf` is a formatted draft with screenshot placeholders. After running the program on your laptop, insert your screenshots into `report_template.docx` and export it over `report.pdf`.

## Setup

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 build_project.py
```

On Windows PowerShell, activation is `.venv\\Scripts\\Activate.ps1`. Run all commands from the project root.

The included `data/english_source.txt` is *Pride and Prejudice* by Jane Austen from Project Gutenberg. Its source information is recorded in `data/SOURCE.md`.

## Required commands

```bash
# Task 1
python3 build/ic_project.pyz frequency --input data/english_source.txt

# Task 2: exactly 100 cleaned lowercase letters
python3 build/ic_project.pyz encrypt --input data/task2_plaintext.txt --key bearcats --limit 100 --output data/task2_ciphertext.txt
python3 build/ic_project.pyz decrypt --input data/task2_ciphertext.txt --key bearcats --limit 100 --output data/task2_decrypted.txt

# Create the long ciphertext used in Tasks 3 and 4
python3 build/ic_project.pyz encrypt --input data/english_source.txt --key bearcats --output data/m17996246_ishimwe.txt

# Task 3
python3 build/ic_project.pyz attack --input data/m17996246_ishimwe.txt --english-ic data/english_ic.txt

# Task 4: first copy every downloaded Canvas .txt file into data/shared_ciphertexts
python3 build/ic_project.pyz attack-folder --folder data/shared_ciphertexts --english-ic data/english_ic.txt
```

The attack uses average column IC to recover the likely key length. It then uses chi-square English-frequency scoring to recover each Caesar shift/key letter. This is necessary because IC is unchanged by a Caesar shift and therefore cannot identify the individual key letters by itself.

See `REPORT_TEMPLATE.md` and `SCREENSHOT_CHECKLIST.md` for the submission workflow.
For complete setup, screenshot, report, GitHub, and Canvas steps, read `GITHUB_AND_VSCODE_GUIDE.md`.
