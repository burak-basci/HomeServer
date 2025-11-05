# Adobe Stock Upload Automation - SUCCESS!

## Summary

After extensive debugging, we successfully automated Adobe Stock image uploads using **Python Playwright with the file chooser API**.

## The Problem

Previous attempts to automate Adobe Stock uploads with Python Playwright failed because we were using `element.set_input_files()` directly on the hidden `<input>` element. Adobe's anti-automation system detects and blocks this approach.

## The Solution

Use Playwright's **file chooser API** which properly simulates the OS-level file picker dialog:

```python
# Click upload button to trigger file chooser
with page.expect_file_chooser() as fc_info:
    page.get_by_role("button", name="suchen").click()

# Set files via the file chooser object
file_chooser = fc_info.value
file_chooser.set_files(image_files)
```

## Test Results

| Test | Method | Images | Starting Count | Final Count | Result |
|------|--------|--------|----------------|-------------|--------|
| 1 | MCP Playwright | 20 | 8 | 28 | ✅ Success |
| 2 | Python Script | 2 | 28 | 30 | ✅ Success |

## Key Files

1. **`upload_adobe_stock_working.py`** - Working Python script using file chooser API
2. **`MCP_TO_PYTHON_WORKFLOW.md`** - Complete documentation of MCP workflow and translation
3. **`FINDINGS_AND_CONCLUSION.md`** - All debugging attempts and learnings

## Usage

```bash
# Basic usage
python upload_adobe_stock_working.py /path/to/images/

# With custom auth state
python upload_adobe_stock_working.py /path/to/images/ --auth-state my_auth.json

# Headless mode
python upload_adobe_stock_working.py /path/to/images/ --headless

# Custom verification timeout
python upload_adobe_stock_working.py /path/to/images/ --verify-timeout 180
```

## How We Discovered This

1. **MCP Playwright uploads worked** - We uploaded 20 images successfully via Claude Code's MCP tools
2. **Python attempts all failed** - Direct `set_input_files()` never triggered uploads
3. **Analyzed MCP code** - MCP uses `fileChooser.setFiles()` not `element.set_input_files()`
4. **Implemented in Python** - Used `page.expect_file_chooser()` context manager
5. **Tested successfully** - Uploaded 2 images, verified count increased 28 → 30

## Why This Works

The file chooser API is different from direct input manipulation:

| Method | How it works | Adobe's response |
|--------|--------------|------------------|
| `input.set_input_files()` | Sets files directly on DOM element | ❌ Blocked - detects automation |
| `file_chooser.set_files()` | Simulates OS file picker dialog | ✅ Accepted - appears legitimate |

## Workflow Steps

1. **Navigate** to `https://contributor.stock.adobe.com/de/uploads?upload=1`
2. **Wait** for page load and authenticate if needed
3. **Extract** current upload count from "Dateitypen: Alle (N)"
4. **Click** the "suchen" (browse) button
5. **Capture** the file chooser with `page.expect_file_chooser()`
6. **Set files** via `file_chooser.set_files(image_paths)`
7. **Wait** for count to update to `current + uploaded`
8. **Verify** success by checking final count

## What's Next

- [ ] Add CSV metadata upload functionality
- [ ] Add checkbox automation (AI-generated, fictional people)
- [ ] Test with larger batches (50-100 images)
- [ ] Add progress reporting during upload
- [ ] Handle upload errors and retries
- [ ] Extend to other stock platforms

## Credits

This solution was discovered through:
- Testing MCP Playwright tools in Claude Code
- Analyzing MCP's underlying Playwright implementation
- Systematic debugging of upload failures
- Translating working MCP workflow to Python

**Date:** 2025-11-01
**Total debugging sessions:** Multiple over several hours
**Final breakthrough:** Discovering MCP uses file chooser API
