#!/usr/bin/env python3
"""
Simple auth state saver - opens browser, waits 60 seconds for you to log in, then saves.
"""
import os
import sys
import time

from APIs.adobe_stock.adobe_stock_playwright import AdobeStockPlaywrightAPI


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    download_dir = os.path.join(current_path, "downloads")
    auth_state_path = os.path.join(current_path, "adobe_auth_state.json")

    print("=" * 60)
    print("Opening browser... You have 60 seconds to log in!")
    print("=" * 60)

    client = AdobeStockPlaywrightAPI(
        download_dir=download_dir,
        headless=False,
        auth_state_file=auth_state_path
    )

    client.open_contributor_portal()

    print("Waiting 60 seconds for you to log in...")
    print("Make sure you reach the upload/dashboard page!")

    for i in range(60, 0, -1):
        print(f"\r{i} seconds remaining...", end="", flush=True)
        time.sleep(1)

    print("\n\nSaving authentication state...")
    client.save_auth_state()

    print("✓ Done! Closing browser...")
    client.close()

    return 0


if __name__ == '__main__':
    sys.exit(main())
