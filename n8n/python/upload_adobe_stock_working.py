#!/usr/bin/env python3
"""
Adobe Stock Upload Script - WORKING VERSION
Uses the file_chooser API (the same approach as MCP Playwright)

This script successfully uploads images to Adobe Stock using the proper
file chooser API instead of direct input manipulation.

Key insight: Adobe blocks direct set_input_files() but accepts file_chooser.set_files()
"""

import os
import re
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


def extract_count_from_text(text: str) -> int:
    """Extract count from 'Dateitypen: Alle (N)' format"""
    match = re.search(r'\((\d+)\)', text)
    return int(match.group(1)) if match else 0


def upload_images_to_adobe_stock(
    images_dir: str,
    auth_state_file: str = "adobe_auth_state.json",
    headless: bool = False,
    verify_timeout: int = 120,
):
    """
    Upload images to Adobe Stock using file chooser API.

    Args:
        images_dir: Directory containing images to upload
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

    print(f"{'='*70}")
    print(f"Adobe Stock Upload - File Chooser API Method")
    print(f"{'='*70}")
    print(f"Images: {len(image_files)} files")
    print(f"Directory: {images_dir}")
    print(f"Auth state: {auth_state_file}")
    print(f"{'='*70}\n")

    with sync_playwright() as p:
        # Launch browser
        print("STEP 1: Launching browser...")
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
            # STEP 2: Navigate to upload page
            print("\nSTEP 2: Navigating to upload page...")
            page.goto("https://contributor.stock.adobe.com/de/uploads?upload=1")
            page.wait_for_load_state("networkidle")

            # Check if we're on login page
            if "auth.services.adobe.com" in page.url:
                print("⚠ Not authenticated - please log in manually")
                print("Waiting 60 seconds for manual login...")
                time.sleep(60)

                # Check if still on login page
                if "auth.services.adobe.com" in page.url:
                    print("❌ Still not logged in - aborting")
                    return False

            # STEP 3: Wait for upload button and get current count
            print("\nSTEP 3: Checking current upload count...")
            page.wait_for_selector('button:has-text("suchen")', timeout=30000)

            count_button = page.locator('button:has-text("Dateitypen:")')
            count_text = count_button.inner_text()
            current_count = extract_count_from_text(count_text)
            expected_count = current_count + len(image_files)

            print(f"✓ Current count: {current_count}")
            print(f"✓ After upload, expecting: {expected_count} images")

            # STEP 4: Click upload button and use file chooser API
            print(f"\nSTEP 4: Uploading {len(image_files)} images via file chooser API...")

            # This is the KEY: Use file chooser API, not direct input manipulation
            with page.expect_file_chooser() as fc_info:
                page.get_by_role("button", name="suchen").click()

            file_chooser = fc_info.value
            file_chooser.set_files(image_files)

            print(f"✓ Files set via file chooser: {len(image_files)}")

            # STEP 5: Wait for upload to complete
            print(f"\nSTEP 5: Waiting for upload count to change to {expected_count}...")

            try:
                # Wait for the count text to update
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
                    print(f"✅ SUCCESS! Upload verified: {expected_count} images")
                    print(f"{'='*70}\n")

                    # Keep browser open for manual verification
                    if not headless:
                        print("Browser will stay open for 30 seconds for manual verification...")
                        time.sleep(30)

                    return True
                else:
                    print(f"\n❌ UPLOAD FAILED")
                    print(f"Expected: {expected_count}, Got: {final_count}")
                    return False

            except PlaywrightTimeout:
                print(f"\n❌ UPLOAD TIMEOUT")
                print(f"Count did not reach {expected_count} within {verify_timeout} seconds")

                # Get final count
                final_count_text = count_button.inner_text()
                final_count = extract_count_from_text(final_count_text)
                print(f"Final count: {final_count}")

                return False

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
        description="Upload images to Adobe Stock using file chooser API"
    )
    parser.add_argument(
        "images_dir",
        help="Directory containing images to upload"
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

    success = upload_images_to_adobe_stock(
        images_dir=args.images_dir,
        auth_state_file=args.auth_state,
        headless=args.headless,
        verify_timeout=args.verify_timeout,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
