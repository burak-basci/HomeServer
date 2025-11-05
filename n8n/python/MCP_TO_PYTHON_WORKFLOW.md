# MCP to Python Workflow Translation

This document captures the exact MCP workflow that successfully uploaded 20 images to Adobe Stock, with detailed notes for Python translation.

## Test Session Results

- **Starting count:** 8 images
- **Uploaded:** 20 images
- **Final count:** 28 images ✅
- **Date:** 2025-11-01

---

## STEP 1: Navigate to Upload Page

### MCP Tool Used
```
mcp__playwright__browser_navigate
```

### Parameters
```json
{
  "url": "https://contributor.stock.adobe.com/de/uploads?upload=1"
}
```

### Result
- Redirected to login page (auth required)
- User logged in manually via Adobe credentials
- After login, reached upload page

### Python Translation
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()

    # Load saved auth state if available
    try:
        context = browser.new_context(storage_state="adobe_auth_state.json")
    except:
        # Manual login required
        pass

    page = context.new_page()
    page.goto("https://contributor.stock.adobe.com/de/uploads?upload=1")

    # Wait for page load
    page.wait_for_load_state("networkidle")
```

### Key Notes
- **Auth persistence:** MCP browser starts fresh each time, doesn't auto-load auth state
- **Manual login:** User logged in via Adobe email/password (not Google)
- **URL parameter:** `?upload=1` opens the upload dialog directly
- **German locale:** `/de/` in URL shows German interface

---

## STEP 2: Verify Page Loaded

### MCP Tool Used
```
mcp__playwright__browser_snapshot
```

### Result
Page snapshot showed:
- Upload dialog visible: "Dateien für deinen ersten Verkauf hochladen"
- Current file count: "Dateitypen: Alle (8)"
- Upload button visible: "suchen" (search/browse)
- 8 existing images displayed in gallery

### Python Translation
```python
# Wait for upload page to load
page.wait_for_selector('button:has-text("suchen")', timeout=30000)

# Extract current count
count_text = page.locator('button:has-text("Dateitypen:")').inner_text()
# Example: "Dateitypen: Alle (8) "
import re
current_count = int(re.search(r'\((\d+)\)', count_text).group(1))
print(f"Current uploads: {current_count}")
```

### Key Notes
- **Count extraction:** Text format is "Dateitypen: Alle (N) " with trailing space
- **Regex pattern:** `\((\d+)\)` extracts number between parentheses
- **Verification:** Essential to capture "before" count for upload verification

---

## STEP 3: Click Upload Button to Open File Chooser

### MCP Tool Used
```
mcp__playwright__browser_click
```

### Parameters
```json
{
  "element": "suchen button",
  "ref": "e81"
}
```

### Result
```
### Modal state
- [File chooser]: can be handled by the "browser_file_upload" tool
```

### Python Translation
```python
# Click the "suchen" button to trigger file chooser
with page.expect_file_chooser() as fc_info:
    page.get_by_role("button", name="suchen").click()
file_chooser = fc_info.value
```

### Key Notes
- **Critical step:** Must click button BEFORE calling file upload
- **File chooser context:** MCP detects file chooser modal automatically
- **Python equivalent:** Use `page.expect_file_chooser()` context manager
- **Button selector:** German text "suchen" = "search/browse"

---

## STEP 4: Upload Files via File Chooser

### MCP Tool Used
```
mcp__playwright__browser_file_upload
```

### Parameters
```json
{
  "paths": [
    "/home/burak/docker/n8n/python/batch2_upload/118-21.10.2025-06:01:22.jpg",
    "/home/burak/docker/n8n/python/batch2_upload/119-21.10.2025-06:01:29.jpg",
    ... (20 files total)
  ]
}
```

### Result
- Files uploaded successfully
- Page showed: "Noch 20 Uploads…" (20 more uploads...)
- Count progressively increased: 8 → 16 → 28

### Python Translation
```python
# Must be called immediately after file_chooser is ready
file_chooser.set_files([
    "/home/burak/docker/n8n/python/batch2_upload/118-21.10.2025-06:01:22.jpg",
    "/home/burak/docker/n8n/python/batch2_upload/119-21.10.2025-06:01:29.jpg",
    # ... all 20 files
])

# Page automatically processes uploads
```

### Key Notes
- **File chooser API:** This is the KEY difference - MCP uses the file chooser properly
- **Timing:** Must call immediately after file_chooser appears
- **No events needed:** File chooser API triggers all necessary events automatically
- **Multiple files:** All 20 files passed in single array

---

## STEP 5: Wait for Upload Completion

### MCP Tool Used
```
mcp__playwright__browser_wait_for
```

### Parameters
```json
{
  "text": "Dateitypen: Alle (28)"
}
```

### Result
- Waited until text appeared showing final count
- Upload completed successfully in ~20 seconds total

### Python Translation
```python
# Wait for the count to update to expected value
expected_count = current_count + len(files)
page.wait_for_selector(
    f'button:has-text("Dateitypen: Alle ({expected_count})")',
    timeout=120000  # 2 minutes max
)

print(f"✅ Upload verified: {expected_count} images")
```

### Key Notes
- **Text-based wait:** Most reliable verification method
- **Dynamic expectation:** Calculate expected count beforehand
- **Timeout:** Allow sufficient time (2 minutes for 20 images)
- **Progressive upload:** Count increases gradually as files process

---

## STEP 6: Mark Images as AI-Generated and Fictional

### TODO: Currently in progress

We need to:
1. Select all newly uploaded images (the 20 new ones)
2. Check "Mit generativen KI-Tools erstellt" (AI-generated)
3. Click "Nein" for "Erkennbare Personen oder Eigentum?" (No recognizable people/property)

---

## Critical Differences: MCP vs Previous Python Attempts

| Aspect | Previous Python Attempts | MCP Workflow | Why MCP Works |
|--------|-------------------------|--------------|---------------|
| File input method | `set_input_files()` on hidden input | `file_chooser.set_files()` after button click | File chooser API triggers real OS dialog |
| Event dispatch | Manually dispatched input/change events | No manual events needed | File chooser API handles events internally |
| Input visibility | Made input visible, modified styles | No modifications needed | File chooser bypasses DOM manipulation |
| Click timing | Various approaches | Click button FIRST, then set files | Proper sequence triggers file chooser |
| Verification | Checked for any uploads | Waited for specific count increase | Strict verification ensures success |

---

## The Key Insight

**Python Playwright CAN work** - we were using the wrong API!

### What Failed ❌
```python
# Direct file input manipulation (Adobe blocks this)
file_input = page.locator('input[type="file"]')
file_input.set_input_files(files)
```

### What Works ✅
```python
# File chooser API (proper OS-level dialog)
with page.expect_file_chooser() as fc_info:
    page.get_by_role("button", name="suchen").click()
file_chooser = fc_info.value
file_chooser.set_files(files)
```

**The difference:**
- `set_input_files()` = sets files directly on DOM input element (Adobe detects and blocks)
- `file_chooser.set_files()` = simulates OS file picker dialog (Adobe accepts)

---

## Python Script Test Results

### Test 1: MCP Upload
- **Date:** 2025-11-01
- **Method:** MCP Playwright tools
- **Images:** 20 files (batch2_upload/)
- **Result:** ✅ SUCCESS (8 → 28 images)

### Test 2: Python Upload
- **Date:** 2025-11-01
- **Method:** Python with file_chooser API
- **Images:** 2 files (test_batch/)
- **Result:** ✅ SUCCESS (28 → 30 images)

**Script:** `upload_adobe_stock_working.py`

```bash
python upload_adobe_stock_working.py test_batch/
```

Output:
```
✅ SUCCESS! Upload verified: 30 images
```

## Final Conclusion

✅ **PYTHON PLAYWRIGHT WORKS FOR ADOBE STOCK!**

The key was using the **file chooser API** instead of direct input manipulation:

### Working Python Code
```python
# Click button to open file chooser
with page.expect_file_chooser() as fc_info:
    page.get_by_role("button", name="suchen").click()

# Set files via file chooser
file_chooser = fc_info.value
file_chooser.set_files(image_files)

# Wait for upload verification
page.wait_for_selector(f'button:has-text("Dateitypen: Alle ({expected_count})")')
```

This is **exactly** what MCP does behind the scenes, and Adobe accepts it as legitimate file selection.

## Next Steps

1. ✅ MCP workflow documented
2. ✅ Python script created
3. ✅ Python script tested and verified
4. ⬜ Add CSV metadata upload
5. ⬜ Add checkbox automation (AI-generated, fictional)
6. ⬜ Test with full batch (20 images)
7. ⬜ Update CLAUDE.md with new workflow
