# sv-menu cli

**sv-menu** is a command-line tool to display daily or weekly restaurant menus from the SV Group's La Mobilière, Nyon cafeteria — right in your terminal.

Built for simplicity and for those who just want to eat without thinking.

---

## 🧩 Features

- Supports daily or full-week menu display
- Pretty CLI output with categories (🥦 Jardin, 🥩 Menu, 🥣 Soupe, etc.)
- Packaged as a portable `.pyz` executable — no need to install dependencies or Docker

---

## 🚀 Quickstart

### 1. Download the latest release

Go to the [Releases page](https://github.com/antbou/sv-menu/releases) and download the latest `sv-menu.pyz` file.

### 2. Run the CLI

Make sure you have Python 3.7+ installed, then run:

```bash
python sv-menu.pyz            # Displays the week’s menu
python sv-menu.pyz --day monday   # Displays menu for a specific day
python sv-menu.pyz --no-cache     # Force fresh data, ignore cache
```

## 🛠️ For developers

If you want to develop or run the project from source, follow these steps:

### Clone the repository

```bash
git clone https://github.com/antbou/sv-menu.git
cd sv-menu
```

### Install dependencies with Poetry

```bash
poetry install
```

### Run the CLI locally

```bash
poetry run sv-menu
```

Or with arguments:

```bash
poetry run sv-menu --day monday
poetry run sv-menu --no-cache
```

### Use Makefile commands

- Export `requirements.txt` (for shiv packaging):

  ```bash
  make requirements
  ```

- Build the portable executable `.pyz` with shiv:

  ```bash
  make shiv
  ```

- Run the CI workflow locally (requires [act](https://github.com/nektos/act)):

  ```bash
  make ci
  ```

- Clean build artifacts (`sv-menu.pyz` and `requirements.txt`):

  ```bash
  make clean
  ```

## 📅 Example Output

```text
📅 Tuesday 2026-02-18
🥦 Jardin
  Focaccia antipasti — Pesto de basilic Aubergines, courgettes et poivrons
    💵 13.30 / 7.50
----------------------------------------
🥩 Menu
  Escalope de porc Milanaise — Tagliatelle al dente Carottes rôties
    💵 13.30 / 7.50
----------------------------------------
🥣 Soupe du jour
  Soupe de petits pois — Et basilic
    💵 1.80 / 1.50
```

## 📄 License

MIT — Feel free to use, fork and contribute.
