# GEMINI.md

## Project Overview

This project provides a Python script to automate the process of uploading images and their corresponding metadata to the Adobe Stock contributor portal. It uses Selenium to control a web browser and perform the necessary actions on the website.

The main script, `upload_and_edit_adobe_stock.py`, orchestrates the process, while the `AdobeStockSeleniumAPI` class in `APIs/adobe_stock/adobe_stock_selenium.py` encapsulates the low-level interactions with the Adobe Stock website.

## Dependencies

The project uses Python 3.13 and its dependencies are listed in `requirements.txt`. To install them, first create and activate a virtual environment, then use pip:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the script

To run the script, you need to provide the path to the directory containing the images and the path to the CSV file with the metadata.

```bash
python upload_and_edit_adobe_stock.py /path/to/images_dir /path/to/metadata.csv
```

### Command-line arguments

-   `images_dir`: Path to the directory containing the images to upload.
-   `csv_path`: Path to the CSV file with the metadata to upload.
-   `--headless`: (Optional) Run the browser in headless mode.
-   `--profile-dir`: (Optional) Path to a Chrome user profile directory to reuse.
-   `--debugger-address`: (Optional) Attach to an existing Chrome debugger address like `127.0.0.1:9222`.
-   `--do-release`: (Optional) Perform the final release/submit. By default, the script runs in a "dry-run" mode.

## Configuration

### Credentials

For automated login, you can set the following environment variables:

-   `ADOBE_USERNAME`: Your Adobe Stock username.
-   `ADOBE_PASSWORD`: Your Adobe Stock password.

If these variables are not set, you will need to log in manually in the browser window that Selenium opens.

## Project Structure

-   `upload_and_edit_adobe_stock.py`: The main script that you run.
-   `APIs/adobe_stock/adobe_stock_selenium.py`: Contains the `AdobeStockSeleniumAPI` class, which handles the browser automation.
-   `requirements.txt`: A list of the Python packages that this project needs.
-   `README.md`: The original README file for this project.
