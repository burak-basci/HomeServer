# CSV Upload Test Results

## Test Details
- **Date:** 2025-11-01
- **Images:** 2 test images (118..., 119...)
- **CSV File:** test_metadata.csv
- **Method:** MCP Playwright file chooser API

## CSV Format Used

```csv
Filename,Title,Keywords,Category
118-21.10.2025-06:01:22.jpg,Abstract Digital Art Technology Background,abstract,digital art,technology,background,modern,futuristic,blue,colorful,artistic,11
119-21.10.2025-06:01:29.jpg,Creative AI Generated Geometric Pattern,geometric,pattern,ai generated,creative,modern,abstract,design,colorful,vibrant,11
```

## Upload Workflow

### Step 1: Click "CSV hochladen" button
```javascript
await page.getByRole('button', { name: 'CSV hochladen' }).click();
```

### Step 2: Dialog opens with CSV upload instructions
- Shows requirements (max 5000 rows, 5MB)
- Shows column definitions table
- Offers sample CSV download

### Step 3: Click "CSV-Datei auswählen und hochladen"
```javascript
await page.getByRole('button', { name: 'CSV-Datei auswählen und' }).click();
```
- This triggers the file chooser

### Step 4: Upload CSV via file chooser
```javascript
await fileChooser.setFiles(["/path/to/test_metadata.csv"])
```

### Step 5: Processing message appears
> **"Deine CSV-Datei wird verarbeitet. Dies kann bis zu 15 Minuten dauern. Schließe diese Seite nicht."**
>
> (Your CSV file is being processed. This can take up to 15 minutes. Don't close this page.)

### Step 6: Success message after ~10 seconds
> **"Daten aus deiner CSV-Datei wurden auf die zugehörigen Dateien angewendet."**
>
> (Data from your CSV file has been applied to the associated files.)

### Step 7: Click refresh button
> **"Zum Anzeigen der Änderungen Seite aktualisieren"**
>
> (Refresh page to view the changes)

## Results

### ✅ What Worked
1. **Title field populated correctly:**
   - Image 119: "Creative AI Generated Geometric Pattern"
   - Image 118: "Abstract Digital Art Technology Background"

2. **CSV upload mechanism works:**
   - File was accepted and processed
   - No upload errors
   - Processing completed in ~10 seconds

3. **Category partially applied:**
   - Images show "1" indicators (processing started)
   - Category field still shows different value (may take time to update)

### ⚠️ Partial Issues

1. **Keywords parsing problem:**
   - Only first keyword appears: "geometric"
   - Error message: "Füge mindestens 5 Keywords hinzu" (Add at least 5 keywords)
   - **Likely cause:** Adobe expects semicolon-separated keywords, not comma-separated

2. **Category not immediately visible:**
   - Specified category 11 (Business) in CSV
   - Interface still shows "Menschen" (People)
   - May require time to process or page refresh

## CSV Format Issues

### Problem: Comma-Separated Keywords

Our CSV used:
```
geometric,pattern,ai generated,creative,modern,abstract,design,colorful,vibrant
```

But Adobe likely expects:
```
geometric;pattern;ai generated;creative;modern;abstract;design;colorful;vibrant
```

**OR** the entire keywords field should be quoted:
```
"geometric,pattern,ai generated,creative,modern,abstract,design,colorful,vibrant"
```

### Recommendation

Test with semicolon-separated keywords OR quoted comma-separated keywords:

```csv
Filename,Title,Keywords,Category
118-21.10.2025-06:01:22.jpg,Abstract Digital Art Technology Background,"abstract,digital art,technology,background,modern,futuristic,blue,colorful,artistic",11
119-21.10.2025-06:01:29.jpg,Creative AI Generated Geometric Pattern,"geometric,pattern,ai generated,creative,modern,abstract,design,colorful,vibrant",11
```

## Python Translation

```python
def upload_csv_metadata(csv_path: str, page):
    """Upload CSV metadata to Adobe Stock"""

    # Step 1: Click CSV upload button
    page.get_by_role("button", name="CSV hochladen").click()

    # Step 2: Wait for dialog
    page.wait_for_selector('dialog:has-text("CSV-Datei mit Metadaten hochladen")')

    # Step 3: Click upload button in dialog
    with page.expect_file_chooser() as fc_info:
        page.get_by_role("button", name="CSV-Datei auswählen und").click()

    # Step 4: Set CSV file
    file_chooser = fc_info.value
    file_chooser.set_files([csv_path])

    # Step 5: Wait for processing message
    page.wait_for_selector('text=Deine CSV-Datei wird verarbeitet')

    # Step 6: Wait for success message (up to 15 minutes)
    page.wait_for_selector(
        'text=Daten aus deiner CSV-Datei wurden auf die zugehörigen Dateien angewendet',
        timeout=900000  # 15 minutes
    )

    # Step 7: Click refresh button
    page.get_by_role("button", name="Zum Anzeigen der Änderungen").click()

    # Wait for page to reload
    page.wait_for_load_state("networkidle")

    print("✅ CSV metadata uploaded successfully")
```

## Next Steps

1. **Test with quoted keywords:**
   - Create new CSV with quoted keyword field
   - Re-upload and verify all keywords appear

2. **Verify category updates:**
   - Wait longer or check if category needs manual verification
   - Category may update after full processing

3. **Add to Python script:**
   - Integrate CSV upload function
   - Add CSV format validation
   - Handle keyword quoting automatically

## Conclusion

✅ **CSV upload works via MCP Playwright!**

The upload mechanism is successful, but we need to adjust the CSV format for keywords:
- Use quoted comma-separated keywords, OR
- Use semicolon-separated keywords

The file chooser API approach works perfectly for CSV uploads just like it does for image uploads.
