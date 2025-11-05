#!/usr/bin/env python3
"""
Mark all uploaded images as AI-generated and fictional people/property.

This script:
1. Navigates through all pages of uploads
2. For each image, clicks it and marks TWO checkboxes in sequence:
   - FIRST: "Mit generativen KI-Tools erstellt" (AI-generated) checkbox
   - SECOND: "Menschen und Eigentum sind fiktiv" (People/property are fictional) checkbox
     (This second checkbox appears AFTER checking the first one)
"""

import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


def mark_ai_checkboxes_for_all_images(
    auth_state_file: str = "adobe_auth_state.json",
    headless: bool = False,
    max_images: int = None,
):
    """
    Mark all uploaded images as AI-generated with fictional people/property.

    Args:
        auth_state_file: Path to saved authentication state
        headless: Run browser in headless mode
        max_images: Maximum number of images to process (None = all)
    """

    print(f"{'='*70}")
    print(f"Adobe Stock - Mark AI Generated Images")
    print(f"{'='*70}")
    print(f"Auth state: {auth_state_file}")
    print(f"Max images: {max_images if max_images else 'All'}")
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

        # Create context with auth state
        context_options = {}
        auth_state_path = Path(auth_state_file)
        if auth_state_path.exists():
            print(f"✓ Loading auth state from {auth_state_file}")
            context_options["storage_state"] = auth_state_file
        else:
            print(f"⚠ No auth state found - manual login required")

        context = browser.new_context(**context_options)
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        page = context.new_page()

        try:
            # Navigate to uploads page
            print("\nNavigating to uploads page...")
            page.goto("https://contributor.stock.adobe.com/de/uploads", wait_until="domcontentloaded")
            time.sleep(2)  # Wait for dynamic content

            # Check authentication
            if "auth.services.adobe.com" in page.url:
                print("❌ Not authenticated - please run save_auth_simple.py first")
                return False

            # Dismiss cookie consent if present
            try:
                cookie_accept = page.locator('#onetrust-accept-btn-handler')
                if cookie_accept.is_visible(timeout=2000):
                    cookie_accept.click()
                    print("✓ Dismissed cookie consent")
                    time.sleep(1)
            except:
                pass  # Cookie dialog not present or already dismissed

            # Get all thumbnail images
            print("\nFinding all images...")
            page.wait_for_selector('[role="option"]', timeout=10000)

            # Get initial count
            thumbnails = page.locator('[role="option"]').all()
            total_images = len(thumbnails)

            print(f"✓ Found {total_images} images to process")

            if max_images:
                total_images = min(total_images, max_images)
                print(f"  (Processing first {total_images} images)")

            # Process each image
            processed = 0
            for i in range(total_images):
                try:
                    print(f"\n[{i+1}/{total_images}] Processing image...")

                    # Dismiss cookie consent if it reappears
                    try:
                        cookie_accept = page.locator('#onetrust-accept-btn-handler')
                        if cookie_accept.is_visible(timeout=500):
                            cookie_accept.click()
                            time.sleep(0.5)
                    except:
                        pass

                    # Re-query thumbnails (page might have updated)
                    thumbnails = page.locator('[role="option"]').all()

                    if i >= len(thumbnails):
                        print(f"  ⚠ Image {i+1} no longer exists, skipping")
                        continue

                    # Click the thumbnail to select it
                    thumbnails[i].click()
                    time.sleep(0.5)  # Wait for detail panel to update

                    # Mark as AI-generated
                    # Find the checkbox by looking for one near the AI text
                    try:
                        # Wait for the detail panel to load
                        page.wait_for_selector('text=Mit generativen KI-Tools erstellt', timeout=3000)

                        # STEP 1: Find and check the first AI checkbox
                        all_checkboxes = page.locator('input[type="checkbox"]').all()

                        ai_checked = False
                        for cb in all_checkboxes:
                            # Check if this checkbox is near "generativen KI-Tools" text
                            parent = cb.locator('xpath=../..')
                            parent_text = parent.text_content() if parent else ""

                            if "generativen KI-Tools" in parent_text:
                                if not cb.is_checked():
                                    cb.click()
                                    print("  ✓ Marked as AI-generated")
                                    time.sleep(0.5)  # Wait for second checkbox to appear
                                else:
                                    print("  ✓ Already marked as AI-generated")
                                ai_checked = True
                                break

                        if not ai_checked:
                            print("  ⚠ AI checkbox not found")

                        # STEP 2: Find and check the second checkbox (Menschen und Eigentum sind fiktiv)
                        # This checkbox appears AFTER checking the first one
                        if ai_checked:
                            time.sleep(0.5)  # Give UI time to show second checkbox

                            # Re-query all checkboxes (new one appeared)
                            all_checkboxes = page.locator('input[type="checkbox"]').all()

                            fictional_checked = False
                            for cb in all_checkboxes:
                                parent = cb.locator('xpath=../..')
                                parent_text = parent.text_content() if parent else ""

                                if "Menschen und Eigentum sind fiktiv" in parent_text:
                                    if not cb.is_checked():
                                        cb.click()
                                        print("  ✓ Marked people/property as fictional")
                                    else:
                                        print("  ✓ Already marked as fictional")
                                    fictional_checked = True
                                    break

                            if not fictional_checked:
                                print("  ⚠ Fictional checkbox not found")

                    except Exception as e:
                        print(f"  ⚠ Could not mark checkboxes: {e}")

                    # STEP 3: Click "Änderungen speichern" (Save changes) button
                    try:
                        save_button = page.get_by_role("button", name="Änderungen speichern")
                        if save_button.is_visible(timeout=1000):
                            save_button.click()
                            print("  ✓ Changes saved")
                            time.sleep(0.5)  # Wait for save to complete
                    except Exception as e:
                        # Save button might not be visible if no changes were made
                        pass

                    processed += 1

                    # Brief pause between images
                    time.sleep(0.3)

                except Exception as e:
                    print(f"  ❌ Error processing image {i+1}: {e}")
                    continue

            print(f"\n{'='*70}")
            print(f"✅ COMPLETED!")
            print(f"Processed: {processed}/{total_images} images")
            print(f"{'='*70}\n")

            # Keep browser open for verification
            if not headless:
                print("Browser will stay open for 10 seconds for verification...")
                time.sleep(10)

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
        description="Mark all Adobe Stock uploads as AI-generated with fictional people"
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
        "--max-images",
        type=int,
        help="Maximum number of images to process (default: all)"
    )

    args = parser.parse_args()

    success = mark_ai_checkboxes_for_all_images(
        auth_state_file=args.auth_state,
        headless=args.headless,
        max_images=args.max_images,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
