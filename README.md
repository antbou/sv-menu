# sv-menu

**sv-menu** is a command-line tool to display daily or weekly restaurant menus from the SV Group's La Mobilière, Nyon cafeteria — right in your terminal.

Built for simplicity and for those who just want to eat without thinking.

---

## 🧩 Features

- Scrapes dynamic menu data using [Playwright](https://playwright.dev/)
- Supports daily or full-week menu display
- Pretty CLI output with categories (🥦 Jardin, 🥩 Menu, 🥣 Soupe, etc.)
- Dockerized for portability

---

## 🚀 Quickstart

### 1. Clone the project

```bash
git clone https://github.com/antbou/sv-menu.git
cd sv-menu
```

### 2. Using Poetry (local)

Make sure you have [Poetry](https://python-poetry.org/) installed.

```bash
poetry install
poetry run sv-menu            # Displays week's menu
poetry run sv-menu --date 2025-07-22   # Displays a specific day
```

---

## 🐳 Using Docker (via Makefile)

### Build the image

```bash
make build
```

### Run the app

```bash
make run
# Or to display a specific date's menu:
make run-args ARGS="--date 2025-07-24"
```

### Open a shell inside the container

```bash
make shell
```

### Clean Docker environment

```bash
make clean
```

## 📅 Output example

```text
📅 Tuesday
🥦 Jardin
  Focaccia antipasti — Pesto de basilic Aubergines, courgettes et poivrons
    💵 EXT CHF 13.30   INT CHF 7.50

🥩 Menu
  Escalope de porc Milanaise — Tagliatelle al dente Carottes rôties
    💵 EXT CHF 13.30   INT CHF 7.50

🥣 Soupe du jour
  Soupe de petits pois — Et basilic
    💵 EXT CHF 1.80   INT CHF 1.50
```

## 📄 License

MIT — Feel free to use, fork and contribute.
