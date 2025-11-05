#!/usr/bin/env python3
"""
Save Adobe Stock authentication state for future automated uploads.

This script opens a browser, lets you log in manually, and then saves your
authentication state (cookies, localStorage, etc.) to a JSON file. Future runs
of the upload script can reuse this auth state without requiring login.

Usage:
    python save_adobe_auth.py
    python save_adobe_auth.py --auth-state /path/to/custom_auth.json
    python save_adobe_auth.py --no-headless  # See the browser while logging in
"""
import os
import sys
import argparse
import time

from APIs.adobe_stock.adobe_stock_playwright import AdobeStockPlaywrightAPI


def main():
    parser = argparse.ArgumentParser(
        description="Save Adobe Stock authentication state for future uploads"
    )
    parser.add_argument(
        "--auth-state",
        default="adobe_auth_state.json",
        help="Path to save authentication state JSON file (default: adobe_auth_state.json)"
    )
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Show browser window (default: headless)"
    )
    args = parser.parse_args()

    current_path = os.path.dirname(os.path.abspath(__file__))
    download_dir = os.path.join(current_path, "downloads")
    auth_state_path = args.auth_state if os.path.isabs(args.auth_state) else os.path.join(current_path, args.auth_state)

    print("=" * 60)
    print("Adobe Stock Authentication State Saver")
    print("=" * 60)
    print()
    print("This script will:")
    print("1. Open Adobe Stock contributor portal in a browser")
    print("2. Wait for you to log in manually")
    print("3. Save your authentication state to a file")
    print()
    print(f"Auth state will be saved to: {auth_state_path}")
    print()
    print("Press ENTER when you're ready to continue...")
    input()

    try:
        # Initialize browser with visible window
        client = AdobeStockPlaywrightAPI(
            download_dir=download_dir,
            headless=not args.no_headless,
            auth_state_file=auth_state_path
        )

        # Navigate to contributor portal
        print("Opening Adobe Stock contributor portal...")
        client.open_contributor_portal()

        print()
        print("=" * 60)
        print("PLEASE LOG IN NOW")
        print("=" * 60)
        print()
        print("1. Complete the login process in the browser window")
        print("2. Make sure you reach the contributor dashboard/upload page")
        print("3. Come back here and press ENTER when you're logged in")
        print()
        input("Press ENTER after you've logged in successfully...")

        # Save authentication state
        print()
        print("Saving authentication state...")
        client.save_auth_state()

        # Verify it works by reloading
        print("Verifying saved state...")
        client.page.reload()
        time.sleep(2)

        # Check if still logged in
        current_url = client.page.url
        if "contributor.stock.adobe.com" in current_url and "auth" not in current_url:
            print()
            print("=" * 60)
            print("SUCCESS!")
            print("=" * 60)
            print()
            print(f"Authentication state saved to: {auth_state_path}")
            print()
            print("You can now run upload_adobe_stock_playwright.py without logging in:")
            print(f"  python upload_adobe_stock_playwright.py /path/to/images /path/to/metadata.csv")
            print()
            print("The script will automatically use the saved authentication state.")
            print("=" * 60)
        else:
            print()
            print("WARNING: Verification failed. You may need to log in again.")
            print(f"Current URL: {current_url}")

        # Close browser
        client.close()
        return 0

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
