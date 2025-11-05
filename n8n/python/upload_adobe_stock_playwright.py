#!/usr/bin/env python3
"""
Upload images and metadata CSV to Adobe Stock using Playwright automation.

This script automates the Adobe Stock contributor workflow:
1. Login (optional, if ADOBE_USERNAME and ADOBE_PASSWORD are set)
2. Upload images from a directory
3. Upload CSV metadata
4. Mark all images as AI-generated with fictional people
5. Release/submit assets (only if --do-release flag is used)

Usage:
    python upload_adobe_stock_playwright.py /path/to/images /path/to/metadata.csv
    python upload_adobe_stock_playwright.py /path/to/images /path/to/metadata.csv --do-release
    python upload_adobe_stock_playwright.py /path/to/images /path/to/metadata.csv --headless
    python upload_adobe_stock_playwright.py /path/to/images /path/to/metadata.csv --debugger-address localhost:9222
"""
import os
import sys
import argparse

from APIs.adobe_stock.adobe_stock_playwright import AdobeStockPlaywrightAPI


def main():
    parser = argparse.ArgumentParser(
        description="Upload images and CSV to Adobe Stock using Playwright (dry-run by default)"
    )
    parser.add_argument("images_dir", help="Path to directory containing images to upload")
    parser.add_argument("csv_path", help="Path to CSV file with metadata to upload")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument(
        "--profile-dir",
        help="Path to Chrome user profile directory to reuse (optional, for session persistence)"
    )
    parser.add_argument(
        "--debugger-address",
        help="Connect to existing Chrome debugger address like localhost:9222"
    )
    parser.add_argument(
        "--do-release",
        action="store_true",
        help="Perform the final release/submit (default: dry-run)"
    )
    parser.add_argument(
        "--auth-state",
        help="Path to authentication state JSON file (for session persistence)"
    )
    parser.add_argument(
        "--save-auth",
        action="store_true",
        help="Save authentication state after login (for future runs)"
    )
    args = parser.parse_args()

    # Validate inputs
    if not os.path.isdir(args.images_dir):
        print(f"Error: images_dir '{args.images_dir}' does not exist or is not a directory", file=sys.stderr)
        sys.exit(2)
    if not os.path.isfile(args.csv_path):
        print(f"Error: csv_path '{args.csv_path}' does not exist or is not a file", file=sys.stderr)
        sys.exit(2)

    # Setup download directory
    current_path = os.path.dirname(os.path.abspath(__file__))
    download_dir = os.path.join(current_path, "downloads")
    os.makedirs(download_dir, exist_ok=True)

    # Default auth state file path
    auth_state_file = args.auth_state or os.path.join(current_path, "adobe_auth_state.json")

    # Initialize Playwright API
    try:
        with AdobeStockPlaywrightAPI(
            download_dir=download_dir,
            headless=args.headless,
            profile_dir=args.profile_dir,
            debugger_address=args.debugger_address,
            auth_state_file=auth_state_file
        ) as client:

            # Check if already logged in via saved auth state
            already_logged_in = os.path.exists(auth_state_file)

            # Attempt optional automated login if env vars provided and not already logged in
            username = os.environ.get("ADOBE_USERNAME")
            password = os.environ.get("ADOBE_PASSWORD")
            if username and password and not already_logged_in:
                print("Logging in with provided credentials...")
                client.login(username=username, password=password)

                # Save auth state if requested
                if args.save_auth:
                    client.save_auth_state()
            elif already_logged_in:
                print(f"Using saved authentication state from {auth_state_file}")
            else:
                print("No credentials provided, assuming already logged in or manual login required")

            print(f"Uploading images from {args.images_dir}...")
            client.upload_images(args.images_dir)

            print(f"Uploading CSV metadata from {args.csv_path}...")
            client.upload_csv(args.csv_path)

            print("Marking all assets as AI-generated with fictional people...")
            client.mark_ai_and_fictional()

            if args.do_release:
                print("Releasing assets (final submit)...")
                client.release_all()
                print("✓ Assets submitted successfully!")
            else:
                print("Dry-run: skipping final release. Re-run with --do-release to submit assets.")

            print("✓ Done!")
            return 0

    except Exception as e:
        print(f"✗ Failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
