#!/usr/bin/env python3
"""
Adobe Stock Upload Script - COMPLETE VERSION
Uploads images AND CSV metadata using file_chooser API

Features:
- Image upload via file chooser API
- CSV metadata upload
- Upload verification
- Authentication state persistence
"""

import os
import re
import sys
import time
import csv
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


def extract_count_from_text(text: str) -> int:
    """Extract count from 'Dateitypen: Alle (N)' format"""
    match = re.search(r'\((\d+)\)', text)
    return int(match.group(1)) if match else 0


def prepare_csv_with_quoted_keywords(csv_path: str) -> str:
    """
    Read CSV and ensure keywords column is properly quoted.
    Returns path to processed CSV file.
    """
    input_path = Path(csv_path)
    output_path = input_path.parent / f"{input_path.stem}_processed.csv"

    with open(input_path, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)

        with open(output_path, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames, quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()

            for row in reader:
                # Ensure Keywords field is properly formatted
                if 'Keywords' in row and row['Keywords']:
                    # If keywords contain commas but aren't quoted, they'll be quoted by csv.QUOTE_MINIMAL
                    pass
                writer.writerow(row)

    print(f"✓ Processed CSV saved to: {output_path}")
    return str(output_path)


def upload_csv_metadata(page, csv_path: str, process_csv: bool = True) -> bool:
    """
    Upload CSV metadata to Adobe Stock.

    Args:
        page: Playwright page object
        csv_path: Path to CSV metadata file
        process_csv: Whether to pre-process CSV for proper keyword quoting

    Returns:
        True if upload successful, False otherwise
    """

    print("\n" + "="*70)
    print("CSV Metadata Upload")
    print("="*70)

    # Pre-process CSV if requested
    if process_csv:
        print("Pre-processing CSV for proper keyword formatting...")
        csv_path = prepare_csv_with_quoted_keywords(csv_path)

    try:
        # STEP 1: Click CSV upload button
        print("\nSTEP 1: Clicking CSV upload button...")
        page.get_by_role("button", name="CSV hochladen").click()
        time.sleep(1)

        # STEP 2: Wait for dialog to appear
        print("STEP 2: Waiting for CSV upload dialog...")
        page.wait_for_selector('dialog:has-text("CSV-Datei mit Metadaten hochladen")', timeout=10000)
        print("✓ Dialog opened")

        # STEP 3: Click the upload button in dialog to trigger file chooser
        print("\nSTEP 3: Triggering file chooser...")
        with page.expect_file_chooser() as fc_info:
            page.get_by_role("button", name="CSV-Datei auswählen und").click()

        # STEP 4: Upload CSV file
        print("STEP 4: Uploading CSV file...")
        file_chooser = fc_info.value
        file_chooser.set_files([csv_path])
        print(f"✓ CSV file set: {csv_path}")

        # STEP 5: Wait for processing message
        print("\nSTEP 5: Waiting for processing to start...")
        page.wait_for_selector('text=Deine CSV-Datei wird verarbeitet', timeout=10000)
        print("✓ CSV processing started")

        # STEP 6: Wait for success message (up to 15 minutes)
        print("STEP 6: Waiting for processing to complete (max 15 minutes)...")
        page.wait_for_selector(
            'text=Daten aus deiner CSV-Datei wurden auf die zugehörigen Dateien angewendet',
            timeout=900000  # 15 minutes
        )
        print("✓ CSV processing completed!")

        # STEP 7: Click refresh button to apply changes
        print("\nSTEP 7: Refreshing page to apply changes...")
        page.get_by_role("button", name="Zum Anzeigen der Änderungen").click()
        time.sleep(3)  # Wait for page to reload
        print("✓ Page refreshed")

        print("\n" + "="*70)
        print("✅ CSV METADATA UPLOADED SUCCESSFULLY")
        print("="*70 + "\n")

        return True

    except PlaywrightTimeout as e:
        print(f"\n❌ TIMEOUT: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def upload_images_and_metadata(
    images_dir: str,
    csv_path: str = None,
    auth_state_file: str = "adobe_auth_state.json",
    headless: bool = False,
    verify_timeout: int = 120,
):
    """
    Upload images and optionally CSV metadata to Adobe Stock.

    Args:
        images_dir: Directory containing images to upload
        csv_path: Optional path to CSV metadata file
        auth_state_file: Path to saved authentication state
        headless: Run browser in headless mode
        verify_timeout: Seconds to wait for upload verification
    """

    # Validate images directory
    images_path = Path(images_dir)
    if not images_path.exists():
        print(f"❌ Error: Directory not found: {images_dir}")
        return False

    # Get list of image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.tif'}
    image_files = [
        str(f.absolute())
        for f in images_path.iterdir()
        if f.suffix.lower() in image_extensions
    ]

    if not image_files:
        print(f"❌ Error: No image files found in {images_dir}")
        return False

    # Validate CSV if provided
    if csv_path and not Path(csv_path).exists():
        print(f"❌ Error: CSV file not found: {csv_path}")
        return False

    print(f"{'='*70}")
    print(f"Adobe Stock Upload - Images + Metadata")
    print(f"{'='*70}")
    print(f"Images: {len(image_files)} files")
    print(f"CSV: {csv_path if csv_path else 'None'}")
    print(f"Auth state: {auth_state_file}")
    print(f"{'='*70}\n")

    with sync_playwright() as p:
        # Launch browser
        print("Launching browser...")
        browser = p.chromium.launch(
            headless=headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
            ]
        )

        # Create context with auth state if available
        context_options = {}
        auth_state_path = Path(auth_state_file)
        if auth_state_path.exists():
            print(f"✓ Loading auth state from {auth_state_file}")
            context_options["storage_state"] = auth_state_file
        else:
            print(f"⚠ No auth state found - manual login required")

        context = browser.new_context(**context_options)

        # Anti-detection measures
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        page = context.new_page()

        try:
            # Navigate to upload page
            print("\nNavigating to upload page...")
            page.goto("https://contributor.stock.adobe.com/de/uploads?upload=1", wait_until="domcontentloaded")
            time.sleep(2)  # Wait for dynamic content

            # Check if we're on login page
            if "auth.services.adobe.com" in page.url:
                print("⚠ Not authenticated - please log in manually")
                print("Waiting 60 seconds for manual login...")
                time.sleep(60)

                if "auth.services.adobe.com" in page.url:
                    print("❌ Still not logged in - aborting")
                    return False

            # === IMAGE UPLOAD ===
            print("\n" + "="*70)
            print("IMAGE UPLOAD")
            print("="*70)

            # Wait for upload button and get current count
            print("\nChecking current upload count...")
            page.wait_for_selector('button:has-text("suchen")', timeout=30000)

            count_button = page.locator('button:has-text("Dateitypen:")')
            count_text = count_button.inner_text()
            current_count = extract_count_from_text(count_text)
            expected_count = current_count + len(image_files)

            print(f"✓ Current count: {current_count}")
            print(f"✓ After upload, expecting: {expected_count} images")

            # Upload images via file chooser API
            print(f"\nUploading {len(image_files)} images via file chooser API...")

            with page.expect_file_chooser() as fc_info:
                page.get_by_role("button", name="suchen").click()

            file_chooser = fc_info.value
            file_chooser.set_files(image_files)

            print(f"✓ Files set via file chooser: {len(image_files)}")

            # Wait for upload to complete
            print(f"\nWaiting for upload count to change to {expected_count}...")

            try:
                page.wait_for_selector(
                    f'button:has-text("Dateitypen: Alle ({expected_count})")',
                    timeout=verify_timeout * 1000
                )

                # Double-check by reading the count
                time.sleep(2)
                final_count_text = count_button.inner_text()
                final_count = extract_count_from_text(final_count_text)

                if final_count == expected_count:
                    print(f"\n{'='*70}")
                    print(f"✅ IMAGE UPLOAD SUCCESS: {expected_count} images")
                    print(f"{'='*70}\n")
                else:
                    print(f"\n❌ IMAGE UPLOAD FAILED")
                    print(f"Expected: {expected_count}, Got: {final_count}")
                    return False

            except PlaywrightTimeout:
                print(f"\n❌ IMAGE UPLOAD TIMEOUT")
                print(f"Count did not reach {expected_count} within {verify_timeout} seconds")
                return False

            # === CSV UPLOAD (if provided) ===
            if csv_path:
                time.sleep(2)  # Brief pause before CSV upload

                csv_success = upload_csv_metadata(page, csv_path, process_csv=True)

                if not csv_success:
                    print("\n⚠ CSV upload failed, but images were uploaded successfully")
                    # Don't return False - images are already uploaded

            # Keep browser open for manual verification
            if not headless:
                print("\nBrowser will stay open for 30 seconds for manual verification...")
                time.sleep(30)

            return True

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False

        finally:
            if not headless:
                print("\nClosing browser...")
            context.close()
            browser.close()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Upload images and metadata to Adobe Stock using file chooser API"
    )
    parser.add_argument(
        "images_dir",
        help="Directory containing images to upload"
    )
    parser.add_argument(
        "--csv",
        help="Path to CSV metadata file"
    )
    parser.add_argument(
        "--auth-state",
        default="adobe_auth_state.json",
        help="Path to authentication state file (default: adobe_auth_state.json)"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )
    parser.add_argument(
        "--verify-timeout",
        type=int,
        default=120,
        help="Seconds to wait for upload verification (default: 120)"
    )

    args = parser.parse_args()

    success = upload_images_and_metadata(
        images_dir=args.images_dir,
        csv_path=args.csv,
        auth_state_file=args.auth_state,
        headless=args.headless,
        verify_timeout=args.verify_timeout,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
