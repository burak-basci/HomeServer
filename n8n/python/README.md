This folder contains a small Selenium helper and a runner script to upload assets to Adobe Stock.

Quick steps to create a Python 3.13.7 virtual environment and install dependencies:

1. If you have python3.13 available as `python3.13`:

```bash
cd $(dirname "$0")
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. If you don't have python3.13, consider using pyenv to install it:

```bash
pyenv install 3.13.7
pyenv virtualenv 3.13.7 n8n-py-3.13.7
pyenv activate n8n-py-3.13.7
pip install -r requirements.txt
```

Usage (after activating the venv):

```bash
python upload_and_edit_adobe_stock.py /path/to/images_dir /path/to/metadata.csv
```

Notes:
- The web UI for Adobe Stock changes frequently. You may need to adjust selectors in `APIs/adobe_stock/adobe_stock_selenium.py`.
- For non-headless runs (useful for debugging), adjust the `headless` parameter when constructing the helper in the script.
