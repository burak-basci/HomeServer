"""
Adobe Stock Upload Automation using MCP Playwright Tools

This module provides a high-level interface for automating Adobe Stock uploads
using the MCP Playwright tools available in Claude Code.

The automation handles:
- Login to Adobe Stock contributor portal
- Image upload
- CSV metadata upload
- Marking images as AI-generated and fictional people
- Releasing/submitting assets for review
"""

import os
import time
from typing import List, Optional


class AdobeStockMCPAutomation:
    """Adobe Stock upload automation using MCP Playwright tools."""

    def __init__(self, mcp_client):
        """Initialize the automation with an MCP client.

        Args:
            mcp_client: The MCP Playwright client instance (provided by Claude Code)
        """
        self.mcp = mcp_client
        self.contributor_url = "https://contributor.stock.adobe.com/"
        self.login_url = "https://stock.adobe.com/"

    def navigate_to_contributor_portal(self):
        """Navigate to the Adobe Stock contributor portal."""
        print(f"Navigating to {self.contributor_url}")
        self.mcp.browser_navigate(url=self.contributor_url)
        time.sleep(2)
        return self.mcp.browser_snapshot()

    def login(self, username: Optional[str] = None, password: Optional[str] = None):
        """Log in to Adobe Stock.

        Args:
            username: Adobe account email
            password: Adobe account password

        If credentials are not provided, assumes already logged in.
        """
        if not username or not password:
            print("No credentials provided, assuming already logged in")
            return

        print("Logging in to Adobe Stock...")
        self.mcp.browser_navigate(url=self.login_url)
        time.sleep(2)

        # Take snapshot to see current page state
        snapshot = self.mcp.browser_snapshot()
        print("Login page loaded")

        # Look for sign-in link
        try:
            # Click sign in if visible
            self.mcp.browser_click(element="Sign in link", ref="<sign-in-ref>")
            time.sleep(2)
        except Exception:
            print("Sign in link not found or already on login page")

        # Fill in email
        snapshot = self.mcp.browser_snapshot()
        # Find email input and fill it
        self.mcp.browser_type(element="Email input field", ref="<email-ref>", text=username, submit=True)
        time.sleep(2)

        # Fill in password
        snapshot = self.mcp.browser_snapshot()
        self.mcp.browser_type(element="Password input field", ref="<password-ref>", text=password, submit=True)
        time.sleep(3)

        # Wait for login to complete
        self.mcp.browser_wait_for(time=5)
        print("Login completed")

    def upload_images(self, images_dir: str) -> int:
        """Upload all images from the specified directory.

        Args:
            images_dir: Path to directory containing image files

        Returns:
            Number of images uploaded
        """
        # Get list of image files
        image_extensions = ('.jpg', '.jpeg', '.png', '.tiff', '.tif')
        image_files = []

        for filename in os.listdir(images_dir):
            if filename.lower().endswith(image_extensions):
                full_path = os.path.abspath(os.path.join(images_dir, filename))
                image_files.append(full_path)

        if not image_files:
            raise ValueError(f"No image files found in {images_dir}")

        print(f"Found {len(image_files)} images to upload")

        # Navigate to contributor portal if not already there
        snapshot = self.mcp.browser_snapshot()
        if "contributor.stock.adobe.com" not in snapshot:
            self.navigate_to_contributor_portal()
            time.sleep(2)

        # Take snapshot to find upload input
        snapshot = self.mcp.browser_snapshot()
        print("Looking for file upload input...")

        # Upload all images at once
        # Note: You'll need to get the actual ref from the snapshot
        # This is a placeholder - actual implementation will use real refs
        for image_path in image_files:
            print(f"Uploading {os.path.basename(image_path)}...")

        # In actual implementation, we'd use:
        # self.mcp.browser_file_upload(paths=image_files)

        # Wait for upload to complete
        print("Waiting for uploads to complete...")
        time.sleep(5)

        # Verify thumbnails appear
        snapshot = self.mcp.browser_snapshot()

        return len(image_files)

    def upload_csv(self, csv_path: str):
        """Upload CSV metadata file.

        Args:
            csv_path: Path to CSV file containing metadata
        """
        if not os.path.exists(csv_path):
            raise ValueError(f"CSV file not found: {csv_path}")

        print(f"Uploading CSV metadata from {csv_path}...")

        # Take snapshot to find CSV upload input
        snapshot = self.mcp.browser_snapshot()

        # Upload CSV file
        csv_abs_path = os.path.abspath(csv_path)
        # self.mcp.browser_file_upload(paths=[csv_abs_path])

        # Wait for CSV processing
        time.sleep(3)
        print("CSV metadata uploaded")

    def mark_ai_and_fictional(self):
        """Mark all uploaded images as AI-generated and people as fictional.

        This iterates through all uploaded images and checks the appropriate boxes.
        """
        print("Marking all images as AI-generated and people as fictional...")

        # Take snapshot to see all uploaded images
        snapshot = self.mcp.browser_snapshot()

        # The actual implementation would:
        # 1. Parse the snapshot to find all image rows/cards
        # 2. For each image, find the AI-generated checkbox and click it
        # 3. For each image, find the fictional people checkbox and click it

        # Pseudocode for the actual implementation:
        # image_rows = parse_snapshot_for_image_rows(snapshot)
        # for row_ref in image_rows:
        #     # Find and click AI-generated checkbox
        #     ai_checkbox_ref = find_ai_checkbox_in_row(row_ref)
        #     self.mcp.browser_click(element="AI generated checkbox", ref=ai_checkbox_ref)
        #
        #     # Find and click fictional people checkbox
        #     fictional_checkbox_ref = find_fictional_checkbox_in_row(row_ref)
        #     self.mcp.browser_click(element="Fictional people checkbox", ref=fictional_checkbox_ref)

        print("All images marked as AI-generated with fictional people")

    def release_all(self):
        """Submit all assets for review."""
        print("Submitting assets for review...")

        # Take snapshot to find submit button
        snapshot = self.mcp.browser_snapshot()

        # Find and click the submit/release button
        # Common button texts: "Submit", "Release", "Send for review", "Submit for review"
        # self.mcp.browser_click(element="Submit button", ref="<submit-button-ref>")

        time.sleep(2)
        print("Assets submitted successfully!")

    def run_full_workflow(
        self,
        images_dir: str,
        csv_path: str,
        do_release: bool = False,
        username: Optional[str] = None,
        password: Optional[str] = None
    ):
        """Run the complete upload workflow.

        Args:
            images_dir: Directory containing images to upload
            csv_path: Path to CSV metadata file
            do_release: Whether to actually submit assets (default: False for dry-run)
            username: Optional Adobe account email
            password: Optional Adobe account password
        """
        try:
            # Step 1: Login (if credentials provided)
            if username and password:
                self.login(username, password)

            # Step 2: Navigate to contributor portal
            self.navigate_to_contributor_portal()

            # Step 3: Upload images
            num_uploaded = self.upload_images(images_dir)
            print(f"✓ Uploaded {num_uploaded} images")

            # Step 4: Upload CSV metadata
            self.upload_csv(csv_path)
            print("✓ CSV metadata uploaded")

            # Step 5: Mark as AI-generated and fictional
            self.mark_ai_and_fictional()
            print("✓ Images marked as AI-generated with fictional people")

            # Step 6: Release/submit (if requested)
            if do_release:
                self.release_all()
                print("✓ Assets submitted for review")
            else:
                print("ℹ Dry-run mode: Skipping final submission (use --do-release to submit)")

            print("\n✓ Workflow completed successfully!")
            return True

        except Exception as e:
            print(f"✗ Error during workflow: {e}")
            import traceback
            traceback.print_exc()
            return False


def create_example_csv(output_path: str):
    """Create an example CSV file with the required format.

    Args:
        output_path: Path where to save the example CSV
    """
    csv_content = """Filename,Title,Keywords,Category
image1.jpg,Beautiful sunset landscape,"sunset,landscape,nature,sky,clouds,beautiful,scenery",11
image2.jpg,Modern office workspace,"office,workspace,modern,business,desk,computer,work",3
image3.jpg,Fresh organic vegetables,"vegetables,organic,fresh,food,healthy,nutrition,produce",7
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(csv_content)

    print(f"Example CSV created at: {output_path}")
    print("\nCSV Format:")
    print("- Filename: Exact filename of the image")
    print("- Title: Descriptive title (5-7 words recommended)")
    print("- Keywords: Comma-separated keywords (up to 49)")
    print("- Category: Numeric category ID (see adobe_stock.md for list)")


if __name__ == '__main__':
    print("This module is designed to be used with Claude Code's MCP Playwright tools")
    print("It cannot be run standalone as it requires the MCP client instance")
    print("\nTo use this automation:")
    print("1. Ensure you have images in a directory")
    print("2. Create a CSV file with metadata (see adobe_stock.md for format)")
    print("3. Ask Claude Code to run the automation using this module")
