# Python venv Cheatsheet

## Install

```bash
# usually built-in, if not:
sudo apt install python3-venv   # Debian/Ubuntu
sudo dnf install python3        # Fedora/RHEL (included)
```

## Create

```bash
python3 -m venv .venv
```

## Activate

```bash
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows
```

Prompt changes to `(.venv)` — you're inside.

## Deactivate

```bash
deactivate
```

## Install packages (while inside)

```bash
pip install requests
pip freeze > requirements.txt
pip install -r requirements.txt
```

## Delete

```bash
rm -rf .venv
```
