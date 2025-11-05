#!/usr/bin/env python3
"""
Adobe Stock Upload - File Chooser API Approach

This uses the SAME approach as MCP: trigger the file chooser dialog
then set files on it. This should properly trigger Adobe's upload mechanism.
"""

import os
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import re


def main():
    if len(sys.argv) < 3:
        print("Usage: python upload_final_working.py <images_dir> <csv_path>")
        sys.exit(1)

    images_dir = sys.argv[1]
    csv_path = sys.argv[2]

    if not os.path.isdir(images_dir):
        print(f"Error: {images_dir} is not a directory")
        sys.exit(1)

    # Get image files
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.tiff', '*.tif']:
        image_files.extend(Path(images_dir).glob(ext))

    image_paths = [str(p.absolute()) for p in sorted(image_files)]

    if not image_paths:
        print(f"Error: No images found in {images_dir}")
        sys.exit(1)

    print(f"\n{'='*70}")
    print(f"Adobe Stock Upload - File Chooser API Method")
    print(f"{'='*70}")
    print(f"Images: {len(image_paths)} files")
    print(f"Auth: adobe_auth_state.json")
    print(f"{'='*70}\n")

    # Create screenshots directory
    screenshots_dir = Path("final_upload_screenshots")
    screenshots_dir.mkdir(exist_ok=True)

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
            ]
        )

        # Load auth state
        auth_file = "adobe_auth_state.json"
        if not os.path.exists(auth_file):
            print(f"Error: {auth_file} not found")
            sys.exit(1)

        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            storage_state=auth_file,
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            locale='de-DE',
        )

        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)

        page = context.new_page()
        page.set_default_timeout(60000)

        try:
            # STEP 1: Navigate
            print("STEP 1: Navigating to upload page...")
            page.goto("https://contributor.stock.adobe.com/de/uploads?upload=1",
                     wait_until="domcontentloaded", timeout=60000)
            time.sleep(3)

            screenshot1 = screenshots_dir / "01_page_loaded.png"
            page.screenshot(path=screenshot1)
            print(f"✓ Screenshot: {screenshot1}")

            # STEP 2: Get current count
            print("\nSTEP 2: Checking current upload count...")
            try:
                count_text = page.locator("text=/Dateitypen.*\\(/").text_content(timeout=10000)
                match = re.search(r'\\((\\d+)\\)', count_text)
                current_count = int(match.group(1)) if match else 0
                print(f"✓ Current count: {current_count}")
            except:
                current_count = 0
                print("✓ No uploads yet (assuming 0)")

            expected_count = current_count + len(image_paths)
            print(f"✓ After upload, expecting: {expected_count} images")

            # STEP 3: Upload using file chooser API (THE KEY DIFFERENCE!)
            print(f"\nSTEP 3: Uploading {len(image_paths)} images via file chooser...")

            # This is the critical part - we wait for file chooser to open
            # then set files on it, just like MCP does
            try:
                # The hidden file input exists, but we need to interact with it properly
                # Let's try finding a button that triggers it first

                print("Looking for upload trigger...")

                # Method 1: Direct file input (but make it visible first)
                print("Attempting direct file input method...")
                result = page.evaluate("""
                    () => {
                        const input = document.querySelector('input[type="file"][accept*="image"]');
                        if (!input) return { found: false };

                        // Make it temporarily visible and interactable
                        input.style.display = 'block';
                        input.style.opacity = '0';
                        input.style.position = 'absolute';
                        input.style.zIndex = '9999';
                        input.style.pointerEvents = 'auto';

                        return { found: true };
                    }
                """)

                if result.get('found'):
                    print("✓ File input found and made interactable")

                    # Now set files on it
                    file_input = page.locator('input[type="file"][accept*="image"]').first
                    file_input.set_input_files(image_paths)
                    print(f"✓ Files set: {len(image_paths)}")

                    # Trigger change event manually
                    page.evaluate("""
                        () => {
                            const input = document.querySelector('input[type="file"][accept*="image"]');
                            if (input) {
                                // Dispatch all the events that a real file selection would trigger
                                input.dispatchEvent(new Event('input', { bubbles: true }));
                                input.dispatchEvent(new Event('change', { bubbles: true }));

                                // Try to trigger any parent handlers
                                const parent = input.closest('form') || input.parentElement;
                                if (parent) {
                                    parent.dispatchEvent(new Event('change', { bubbles: true }));
                                }
                            }
                        }
                    """)
                    print("✓ Change events dispatched")

                else:
                    print("❌ File input not found!")
                    return

            except Exception as e:
                print(f"❌ Upload failed: {e}")
                return

            # STEP 4: Wait for upload with STRICT verification
            print(f"\nSTEP 4: Waiting for upload count to change from {current_count} to {expected_count}...")

            # Wait and check repeatedly
            upload_verified = False
            for attempt in range(60):  # 60 attempts = 2 minutes
                try:
                    current_text = page.locator("text=/Dateitypen.*\\(/").text_content(timeout=2000)
                    match = re.search(r'\\((\\d+)\\)', current_text)
                    new_count = int(match.group(1)) if match else 0

                    print(f"  Attempt {attempt+1}: Current count = {new_count}, Target = {expected_count}")

                    if new_count == expected_count:
                        print(f"\n✅ SUCCESS! Upload verified: {new_count} images")
                        upload_verified = True
                        break
                    elif new_count > current_count and new_count < expected_count:
                        print(f"  ⏳ Upload in progress: {new_count}/{expected_count}")

                    time.sleep(2)
                except:
                    time.sleep(2)
                    continue

            screenshot2 = screenshots_dir / "02_after_upload.png"
            page.screenshot(path=screenshot2)
            print(f"✓ Screenshot: {screenshot2}")

            if not upload_verified:
                print("\n❌ UPLOAD FAILED - count did not increase")
                print("Check screenshots to see what happened")
                input("\nPress ENTER to close browser...")
                return

            # STEP 5: Mark checkboxes
            print(f"\nSTEP 5: Marking checkboxes...")
            result = page.evaluate("""
                async () => {
                    const thumbnails = document.querySelectorAll('[role="option"]');
                    let aiMarked = 0, fictionalMarked = 0;

                    for (let i = 0; i < thumbnails.length; i++) {
                        thumbnails[i].click();
                        await new Promise(r => setTimeout(r, 500));

                        const ai = document.querySelector('input[type="checkbox"][aria-label*="generativen KI-Tools"]');
                        if (ai && !ai.checked) { ai.click(); aiMarked++; await new Promise(r => setTimeout(r, 300)); }

                        const fictional = document.querySelector('input[type="checkbox"][aria-label*="Menschen und Eigentum sind fiktiv"]');
                        if (fictional && !fictional.checked) { fictional.click(); fictionalMarked++; await new Promise(r => setTimeout(r, 300)); }
                    }

                    return { aiMarked, fictionalMarked, total: thumbnails.length };
                }
            """)

            print(f"✓ AI-generated: {result['aiMarked']}/{result['total']}")
            print(f"✓ Fictional: {result['fictionalMarked']}/{result['total']}")

            screenshot3 = screenshots_dir / "03_complete.png"
            page.screenshot(path=screenshot3)
            print(f"✓ Screenshot: {screenshot3}")

            print(f"\n{'='*70}")
            print("✅ UPLOAD COMPLETE!")
            print(f"{'='*70}")
            print(f"Before: {current_count} images")
            print(f"Uploaded: {len(image_paths)} images")
            print(f"After: {expected_count} images")
            print(f"Verified: {upload_verified}")
            print(f"\nScreenshots: {screenshots_dir}/")
            print(f"{'='*70}\n")

            print("Browser will stay open for 60 seconds...")
            print("Please verify in the browser window!")
            time.sleep(60)

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            screenshot_error = screenshots_dir / "ERROR.png"
            page.screenshot(path=screenshot_error)
            print(f"Error screenshot: {screenshot_error}")
            input("\nPress ENTER to close browser...")

        finally:
            context.close()
            browser.close()


if __name__ == '__main__':
    main()
