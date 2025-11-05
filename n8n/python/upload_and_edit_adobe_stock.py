#!/usr/bin/env python3
import os
import os
import sys
import shutil
import argparse

from APIs.adobe_stock.adobe_stock_selenium import AdobeStockSeleniumAPI


def main():
    parser = argparse.ArgumentParser(description="Upload images and CSV to Adobe Stock (dry-run by default)")
    parser.add_argument("images_dir", help="Path to directory containing images to upload")
    parser.add_argument("csv_path", help="Path to CSV file with metadata to upload")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--profile-dir", help="Path to Chrome user profile directory to reuse (optional)")
    parser.add_argument("--debugger-address", help="Attach to an existing Chrome debugger address like 127.0.0.1:9222")
    parser.add_argument("--do-release", action="store_true", help="Perform the final release/submit (default: dry-run)")
    args = parser.parse_args()

    # Validate inputs
    if not os.path.isdir(args.images_dir):
        print("images_dir does not exist or is not a directory", file=sys.stderr)
        sys.exit(2)
    if not os.path.isfile(args.csv_path):
        print("csv_path does not exist or is not a file", file=sys.stderr)
        sys.exit(2)

    current_path = os.path.dirname(os.path.abspath(__file__))
    download_dir = os.path.join(current_path, "downloads")
    os.makedirs(download_dir, exist_ok=True)

    # Check for a mounted chromedriver first, else None and let helper use webdriver-manager
    local_chromedriver = "/chromedriver/chromedriver"
    chromedriver_path = local_chromedriver if os.path.exists(local_chromedriver) else None

    client = AdobeStockSeleniumAPI(download_dir=download_dir, chromedriver_path=chromedriver_path,
                                   headless=args.headless, profile_dir=args.profile_dir,
                                   debugger_address=args.debugger_address)

    try:
        # Attempt optional automated login if env vars provided (may not work for SSO)
        username = os.environ.get("ADOBE_USERNAME")
        password = os.environ.get("ADOBE_PASSWORD")
        if username and password:
            client.login(username=username, password=password)

        print("Uploading images...")
        client.upload_images(args.images_dir)

        print("Uploading CSV metadata...")
        client.upload_csv(args.csv_path)

        print("Marking AI-generated and fictional humans flags...")
        client.mark_ai_and_fictional()

        if args.do_release:
            print("Releasing assets (final submit)...")
            client.release_all()
        else:
            print("Dry-run: skipping final release. Re-run with --do-release to submit assets.")

        client.quit()
        print("Done")
        return 0
    except Exception as e:
        print(f"Failed: {e}", file=sys.stderr)
        try:
            client.quit()
        except Exception:
            pass
        return 1


if __name__ == '__main__':
    sys.exit(main())
