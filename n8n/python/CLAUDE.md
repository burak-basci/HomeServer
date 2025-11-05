# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This project automates the upload of AI-generated images to stock photography platforms, specifically Adobe Stock. It uses Playwright (recommended) or Selenium to automate web interactions since most platforms lack contributor APIs.

## Environment Setup

The project requires Python 3.13.7 with a virtual environment:

```bash
# Using python3.13
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Or using pyenv
pyenv install 3.13.7
pyenv virtualenv 3.13.7 n8n-py-3.13.7
pyenv activate n8n-py-3.13.7
pip install -r requirements.txt
```

## Running the Upload Script

### MCP Playwright Version (Claude Code Integration - Newest)

Use Claude Code's built-in MCP Playwright tools for interactive automation:

```bash
python upload_adobe_stock_mcp.py /path/to/images_dir /path/to/metadata.csv
```

Or simply ask Claude Code:
```
"Upload my Adobe Stock images from /path/to/images with metadata /path/to/metadata.csv"
```

See `MCP_PLAYWRIGHT_GUIDE.md` for detailed documentation.

### Playwright Version (Recommended for standalone)

```bash
python upload_adobe_stock_playwright.py /path/to/images_dir /path/to/metadata.csv
```

### Selenium Version (Legacy)

```bash
python upload_and_edit_adobe_stock.py /path/to/images_dir /path/to/metadata.csv
```

### Command-line Arguments

- `images_dir`: Directory containing images to upload (.jpg, .jpeg, .png, .tiff, .tif)
- `csv_path`: CSV file with metadata (UTF-8 encoded)
- `--headless`: Run browser in headless mode
- `--profile-dir`: Reuse Chrome user profile directory (for session persistence)
- `--debugger-address`: Attach to existing Chrome debugger (e.g., `127.0.0.1:9222`)
- `--do-release`: Actually submit assets (default is dry-run)

### Authentication

**Recommended: Save Authentication State (One-Time Setup)**

The best way to handle authentication is to save your login session once and reuse it:

```bash
# Run this once to save your login
python save_adobe_auth.py --no-headless

# Follow the prompts, log in manually, then press ENTER
# Your session will be saved to adobe_auth_state.json

# Future runs will use the saved session automatically
python upload_adobe_stock_playwright.py /path/to/images /path/to/metadata.csv
```

**Alternative: Environment Variables (may not work with SSO)**

Set environment variables for automated login:
- `ADOBE_USERNAME`: Adobe Stock username
- `ADOBE_PASSWORD`: Adobe Stock password

```bash
export ADOBE_USERNAME="your@email.com"
export ADOBE_PASSWORD="yourpassword"
python upload_adobe_stock_playwright.py /path/to/images /path/to/metadata.csv --save-auth
```

If neither auth state file nor credentials are provided, manual login is required in the browser window.

## CSV Metadata Format

Required columns for Adobe Stock uploads:

| Column | Description |
|--------|-------------|
| `Filename` | Exact filename (e.g., `image.jpg`) |
| `Title` | Descriptive title (5-7 words recommended) |
| `Keywords` | Comma-separated keywords (up to 49) |
| `Category` | Numeric category ID (see adobe_stock.md for IDs) |

## Architecture

### Core Components

**upload_adobe_stock_mcp.py** (Newest - MCP Integration) - Claude Code MCP Playwright entry point:
1. Validates input paths
2. Provides workflow instructions for Claude Code
3. Uses MCP Playwright tools for browser automation
4. Interactive and adaptive workflow execution
5. See `MCP_PLAYWRIGHT_GUIDE.md` for details

**APIs/adobe_stock/adobe_stock_mcp_playwright.py** - `AdobeStockMCPAutomation` class:
- Uses Claude Code's MCP Playwright tools
- Interactive browser automation via MCP
- Methods: `login()`, `upload_images()`, `upload_csv()`, `mark_ai_and_fictional()`, `release_all()`
- Designed for use within Claude Code environment

**demo_adobe_stock_mcp.py** - Interactive demo showing MCP tool calls:
- Demonstrates exact MCP Playwright workflow
- Shows tool calls needed at each step
- Useful for understanding and debugging

**upload_adobe_stock_playwright.py** (Recommended for standalone) - Main Playwright-based entry point:
1. Validates input paths
2. Initializes the Playwright helper
3. Orchestrates the upload workflow:
   - Login (if credentials provided)
   - Upload images
   - Upload CSV metadata
   - Mark AI-generated and fictional human flags
   - Release assets (if `--do-release` flag set)

**upload_and_edit_adobe_stock.py** (Legacy) - Original Selenium-based entry point with same workflow

**APIs/adobe_stock/adobe_stock_playwright.py** - `AdobeStockPlaywrightAPI` class for browser automation:
- Chromium browser initialization via Playwright
- Support for headless mode, persistent context, and CDP connection
- More reliable selectors and better waiting mechanisms than Selenium
- Context manager support for automatic cleanup
- Methods: `login()`, `upload_images()`, `upload_csv()`, `mark_ai_and_fictional()`, `release_all()`

**APIs/adobe_stock/adobe_stock_selenium.py** - Legacy `AdobeStockSeleniumAPI` class:
- Chrome/ChromeDriver initialization with webdriver-manager
- Support for headless mode, profile reuse, and debugger attachment
- Best-effort selectors for Adobe Stock UI (subject to change)
- Methods: `login()`, `upload_images()`, `upload_csv()`, `mark_ai_and_fictional()`, `release_all()`

**APIs/selenium/** - Reusable Selenium infrastructure (appears to be for a different project - Immoware24 property management system)

### Browser Setup

**Playwright Setup (Recommended):**
After installing requirements, install Playwright browsers:
```bash
playwright install chromium
```

The Playwright script supports:
1. New browser launch (default)
2. Persistent context with profile directory (`--profile-dir`)
3. CDP connection to existing Chrome (`--debugger-address`)

**Selenium/ChromeDriver Setup (Legacy):**
The Selenium script supports multiple ChromeDriver configurations:
1. Mounted driver at `/chromedriver/chromedriver` (Docker environment)
2. Auto-download via `webdriver-manager` (default)
3. Custom path via constructor

When attaching to existing Chrome (`--debugger-address`), it attempts to match ChromeDriver version to the running browser.

## Important Notes

- Adobe Stock UI changes frequently - selectors in `adobe_stock_selenium.py` may need updates
- Script defaults to dry-run mode; use `--do-release` to actually submit assets
- Images must be flagged as AI-generated and people marked as fictional
- Downloads go to `downloads/` subdirectory by default

## Platform Documentation

See individual markdown files for platform-specific details:
- `MCP_PLAYWRIGHT_GUIDE.md` - Comprehensive guide for MCP Playwright automation (newest)
- `adobe_stock.md` - Category IDs, metadata requirements, upload workflow
- `overview.md` - Comparison table of different stock platforms
- `my_plan.md` - Multi-platform upload strategy (Wirestock aggregator + direct uploads)

## Automation Comparison

| Version | Use Case | Browser Control | Execution |
|---------|----------|----------------|-----------|
| **MCP Playwright** | Claude Code integration | MCP tools | Interactive via Claude |
| **Playwright** | Standalone automation | Python Playwright API | Fully automated |
| **Selenium** | Legacy support | Python Selenium API | Fully automated |

**Recommendation**: Use MCP Playwright when working with Claude Code, or standalone Playwright for scripts.
