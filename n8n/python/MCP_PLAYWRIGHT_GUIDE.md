# Adobe Stock MCP Playwright Automation Guide

This guide explains how to use Claude Code's MCP Playwright tools to automate Adobe Stock image uploads with metadata.

## Overview

The MCP (Model Context Protocol) Playwright tools allow Claude Code to directly control a web browser and automate complex workflows. This automation handles:

1. **Login** - Access Adobe Stock contributor portal
2. **Image Upload** - Upload multiple images at once
3. **CSV Metadata** - Apply titles, keywords, and categories via CSV
4. **AI Flagging** - Mark all images as AI-generated (required by Adobe)
5. **Fictional People** - Mark AI-generated people as fictional
6. **Submission** - Release assets for review (optional)

## Files Created

### 1. `adobe_stock_mcp_playwright.py`
Core automation module with the `AdobeStockMCPAutomation` class. Provides high-level methods:
- `login()` - Handle authentication
- `upload_images()` - Upload image files
- `upload_csv()` - Upload metadata CSV
- `mark_ai_and_fictional()` - Flag AI content and fictional people
- `release_all()` - Submit for review
- `run_full_workflow()` - Execute complete workflow

### 2. `upload_adobe_stock_mcp.py`
Command-line interface for the automation. Handles:
- Argument parsing
- Input validation
- Workflow orchestration
- Progress reporting

### 3. `demo_adobe_stock_mcp.py`
Interactive demonstration showing exact MCP tool calls needed at each step. Useful for:
- Understanding the workflow
- Debugging issues
- Learning MCP Playwright patterns

## Prerequisites

### 1. Images Directory
Create a directory containing your images:
```
images/
├── image1.jpg
├── image2.jpg
├── image3.png
└── ...
```

Supported formats: `.jpg`, `.jpeg`, `.png`, `.tiff`, `.tif`

### 2. Metadata CSV File
Create a UTF-8 encoded CSV with these columns:

| Column | Description | Example |
|--------|-------------|---------|
| `Filename` | Exact filename | `image1.jpg` |
| `Title` | Descriptive title (5-7 words) | `Beautiful sunset over mountain landscape` |
| `Keywords` | Comma-separated (up to 49) | `sunset,mountain,landscape,nature,sky` |
| `Category` | Numeric category ID | `11` (Landscape) |

**Example CSV:**
```csv
Filename,Title,Keywords,Category
image1.jpg,Beautiful sunset landscape,"sunset,landscape,nature,sky,clouds",11
image2.jpg,Modern office workspace,"office,workspace,modern,business,desk",3
image3.jpg,Fresh organic vegetables,"vegetables,organic,fresh,food,healthy",7
```

**Category IDs:**
See `adobe_stock.md` for the complete list. Common ones:
- `3` - Business
- `7` - Food
- `11` - Landscape
- `13` - People
- `19` - Technology

## Usage

### Option 1: Ask Claude Code Directly (Recommended)

Simply ask Claude Code to run the automation:

```
Claude, please upload my Adobe Stock images using the MCP automation.
Images are in: /path/to/images
Metadata CSV: /path/to/metadata.csv
This is a dry-run, don't submit yet.
```

Or for actual submission:

```
Claude, please run the Adobe Stock MCP automation with:
- Images: ./test_images
- CSV: ./metadata.csv
- Do the final submission (--do-release)
```

### Option 2: Run the Demo First

To see what will happen without doing it:

```bash
python demo_adobe_stock_mcp.py /path/to/images /path/to/metadata.csv
```

This prints all the MCP tool calls that will be made.

### Option 3: Direct Script Execution

```bash
# Dry-run (no submission)
python upload_adobe_stock_mcp.py /path/to/images /path/to/metadata.csv

# With actual submission
python upload_adobe_stock_mcp.py /path/to/images /path/to/metadata.csv --do-release

# With authentication
export ADOBE_USERNAME="your@email.com"
export ADOBE_PASSWORD="yourpassword"
python upload_adobe_stock_mcp.py /path/to/images /path/to/metadata.csv --do-release
```

## MCP Playwright Workflow Details

### Step 1: Navigate to Contributor Portal

```python
mcp__playwright__browser_navigate(
    url="https://contributor.stock.adobe.com/"
)
```

### Step 2: Check Login Status

```python
# Take snapshot to see current page
snapshot = mcp__playwright__browser_snapshot()

# Check if login required
if "Sign in" in snapshot or "Log in" in snapshot:
    # Manual login required or use credentials
    ...
```

### Step 3: Upload Images

```python
# Take snapshot to find upload input
snapshot = mcp__playwright__browser_snapshot()

# Upload all images at once
mcp__playwright__browser_file_upload(
    paths=[
        "/absolute/path/to/image1.jpg",
        "/absolute/path/to/image2.jpg",
        ...
    ]
)

# Wait for uploads to complete
mcp__playwright__browser_wait_for(time=5)

# Verify thumbnails appeared
snapshot = mcp__playwright__browser_snapshot()
```

### Step 4: Upload CSV Metadata

```python
# Find CSV upload input
snapshot = mcp__playwright__browser_snapshot()

# Upload CSV
mcp__playwright__browser_file_upload(
    paths=["/absolute/path/to/metadata.csv"]
)

# Wait for processing
mcp__playwright__browser_wait_for(time=3)
```

### Step 5: Mark as AI-Generated

```python
# Get current page state
snapshot = mcp__playwright__browser_snapshot()

# For each image, find and click AI checkbox
# Parse snapshot to get checkbox refs
for checkbox_ref in ai_checkbox_refs:
    mcp__playwright__browser_click(
        element="AI generated checkbox",
        ref=checkbox_ref
    )
```

### Step 6: Mark People as Fictional

```python
# Similar to AI marking
for checkbox_ref in fictional_checkbox_refs:
    mcp__playwright__browser_click(
        element="Fictional people checkbox",
        ref=checkbox_ref
    )
```

### Step 7: Submit for Review (if --do-release)

```python
# Find submit button
snapshot = mcp__playwright__browser_snapshot()

# Click submit
mcp__playwright__browser_click(
    element="Submit button",
    ref=submit_button_ref
)

# Wait for confirmation
mcp__playwright__browser_wait_for(time=2)
```

## Authentication Options

### Option 1: Saved Auth State (Recommended)
Save your login session once and reuse it:

```bash
# One-time setup
python save_adobe_auth.py --no-headless
# (login manually, then press ENTER)

# Future runs automatically use saved session
python upload_adobe_stock_mcp.py /path/to/images /path/to/metadata.csv
```

### Option 2: Environment Variables
```bash
export ADOBE_USERNAME="your@email.com"
export ADOBE_PASSWORD="yourpassword"
python upload_adobe_stock_mcp.py /path/to/images /path/to/metadata.csv --save-auth
```

### Option 3: Manual Login
If no credentials provided, the browser will open and you can log in manually.

## Important Notes

### Adobe Stock Requirements

1. **AI Content MUST Be Flagged** - Adobe requires all AI-generated content to be marked. Failure to do so can result in account suspension.

2. **Fictional People** - AI-generated people must be marked as fictional since no model releases exist.

3. **Metadata Quality** - Use descriptive titles and relevant keywords for better discoverability.

4. **File Quality** - Images should be high resolution and commercially viable.

### Dry-Run vs Live Mode

**Dry-Run (Default):**
- Uploads images
- Applies metadata
- Marks AI/fictional flags
- STOPS before final submission
- Safe for testing

**Live Mode (--do-release):**
- Completes all steps including submission
- Assets enter Adobe's review queue
- Cannot be undone

### Troubleshooting

**Issue: "No image files found"**
- Check that images directory contains .jpg, .png, or .tiff files
- Verify the path is correct

**Issue: "CSV file not found"**
- Check CSV path
- Ensure file has .csv extension

**Issue: "Upload input not found"**
- Adobe may have changed their UI
- Check browser console for errors
- Try updating selectors in the script

**Issue: "Checkboxes not found"**
- Take a screenshot to see current page state
- Adobe frequently updates their UI
- May need to adjust selectors

## Comparison with Standard Playwright Version

| Feature | MCP Playwright | Standard Playwright |
|---------|----------------|---------------------|
| **Execution** | Via Claude Code | Standalone Python script |
| **Browser Control** | MCP tool calls | Direct Playwright API |
| **Interactive** | Yes, Claude assists | No, fully automated |
| **Debugging** | Claude can help | Manual debugging |
| **Flexibility** | High, adaptive | Fixed workflow |
| **Complexity** | Lower, guided | Higher, requires coding |

## Example Workflow Session

```
User: Claude, upload my test images to Adobe Stock

Claude: I'll help you with that! Let me start the MCP Playwright automation.

[Calls mcp__playwright__browser_navigate]

Claude: I've navigated to the Adobe Stock contributor portal. Taking a snapshot to see the current state...

[Calls mcp__playwright__browser_snapshot]

Claude: I see you're already logged in. Found 5 images in your directory:
- sunset1.jpg
- sunset2.jpg
- office1.jpg
- office2.jpg
- food1.jpg

Now uploading images...

[Calls mcp__playwright__browser_file_upload]

Claude: Images uploaded successfully! Now applying CSV metadata...

[Calls mcp__playwright__browser_file_upload for CSV]

Claude: Metadata applied. Now marking all images as AI-generated...

[Calls mcp__playwright__browser_click for each AI checkbox]

Claude: All images marked as AI-generated. Marking people as fictional...

[Calls mcp__playwright__browser_click for fictional checkboxes]

Claude: Done! Since this is a dry-run, I'm stopping before submission.
To actually submit, ask me to run with --do-release.
```

## Next Steps

1. **Prepare your images** - Collect high-quality images in a directory
2. **Create metadata CSV** - Use the format described above
3. **Test with dry-run** - Verify everything works without submission
4. **Submit for real** - Use --do-release when ready
5. **Monitor Adobe dashboard** - Check review status online

## Resources

- **Adobe Stock Categories**: See `adobe_stock.md`
- **Platform Comparison**: See `overview.md`
- **Upload Strategy**: See `my_plan.md`
- **Playwright Docs**: See existing `adobe_stock_playwright.py`

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the demo script output
3. Take screenshots at each step for debugging
4. Check Adobe Stock contributor help center
5. Ask Claude Code for assistance with specific errors
