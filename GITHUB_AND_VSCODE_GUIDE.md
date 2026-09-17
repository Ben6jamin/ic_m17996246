# VS Code and GitHub Guide

## 1 Open the project

1. Extract the ZIP file.
2. Open VS Code, choose **File > Open Folder**, and select `ic_m17996246`.
3. Open **Terminal > New Terminal**. Confirm that the prompt ends in `ic_m17996246`.

## 2 Create the Python environment

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 build_project.py
python3 --version
```

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python build_project.py
python --version
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` in that terminal and try activation again.

## 3 Run the tests

```bash
python3 -m unittest discover -s tests -v
```

On Windows, use `python` instead of `python3` in every command if that is the command recognized by your computer.

After `python3 build_project.py`, confirm that `build/ic_project.pyz` appears in the VS Code Explorer. This is the runnable project generated from the files in `src`.

## 4 Run Tasks 1 through 3 and capture screenshots

Run each command separately. Follow `SCREENSHOT_CHECKLIST.md` and keep the VS Code window visible.

```bash
python3 build/ic_project.pyz frequency --input data/english_source.txt
python3 build/ic_project.pyz encrypt --input data/task2_plaintext.txt --key bearcats --limit 100 --output data/task2_ciphertext.txt
python3 build/ic_project.pyz decrypt --input data/task2_ciphertext.txt --key bearcats --limit 100 --output data/task2_decrypted.txt
python3 build/ic_project.pyz attack --input data/m17996246_ishimwe.txt --english-ic data/english_ic.txt
```

For the plot screenshot, click `data/frequency_plot.png` in the VS Code Explorer after Task 1 finishes.

## 5 Complete Task 4

1. Upload `data/m17996246_ishimwe.txt` to the Canvas shared folder before the Task 4 upload deadline.
2. Download every `.txt` file from that folder, including your own.
3. Put all of them directly inside `data/shared_ciphertexts`.
4. Run:

```bash
python3 build/ic_project.pyz attack-folder --folder data/shared_ciphertexts --english-ic data/english_ic.txt
```

5. Open `data/task4_results.txt`. Paste every line into the Task 4 section of `report_template.docx` and capture the terminal result for Screenshot 8.

## 6 Finish the report

1. Open `report_template.docx` in Microsoft Word.
2. Replace the UCID, course, operating system, and Python version placeholders.
3. Replace each red screenshot placeholder with the corresponding screenshot from your laptop.
4. Paste the complete Task 4 results.
5. Save the editable document, then choose **File > Save As** or **Export > PDF** and name the final file `report.pdf`.
6. Open the PDF and check every page before submitting.

## 7 Push the repository to GitHub

Create an empty GitHub repository named `ic_m17996246` without a README, license, or `.gitignore`. Then run these commands from the VS Code terminal:

```bash
git init
git add .
git commit -m "Complete index of coincidence project"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/ic_m17996246.git
git push -u origin main
```

Replace `YOUR_GITHUB_USERNAME` with your GitHub username. If GitHub asks you to authenticate, use the browser sign-in flow shown by VS Code. Do not place passwords or tokens in project files.

## 8 Submit to Canvas

The assignment asks for a ZIP of the code. Before making it, ensure `report.pdf` is inside the project root. In Finder or File Explorer, compress the complete `ic_m17996246` folder. Open the ZIP once and verify that it contains `src`, `data`, `tests`, `requirements.txt`, and `report.pdf`, then upload that ZIP to Canvas.

The `build` directory must also remain in the project. It contains `ic_project.pyz`, the runnable Python archive produced by `build_project.py`.
