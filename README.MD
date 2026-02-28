# Minimalist File Organizer 🗂️✨

This project is a **Python tool for automatic file organization** that sorts files by type and subfolder, focusing on **efficiency and minimalism**.

## 📂 Structure

* `maestro.py` – First functional version (v1.0) of the file organizer.
* `maestro-eficiente.py` – Optimized version of `maestro.py`, with minimalist code, single-character Chinese variables, and improved binary efficiency.
* `cria-muito-arquivo.py` / `cria-pouco-arquivo.py` – Helper scripts to generate test files.

## 🎯 Objective

* Automatically organize files into categorized directories.
* Make the code **lightweight, minimalist, and efficient** in binary.
* Experiment with **Chinese characters as variables**, maintaining human readability and machine compactness.

## 🚀 How to Use

```bash
python maestro-eficiente.py -o /source/path -d /destination/path -r /report/path.csv [options]
```

### ⚙️ Required Arguments

* `-o, --source` : Root directory of the files to organize.
* `-d, --destination` : Directory where the files will be organized.

### 🛠️ Options

* `-r, --report` : Path to generate a CSV report with actions performed (`source`, `destination`, `action`).
* `-c, --copy` : Copy files instead of moving them.
* `--dry-run` : Simulate the operation without moving or copying files (only shows what would be done).

---

Have fun organizing your files! 🚀
