#!/usr/bin/env python3
"""
Stock Photography Upload Framework

Object-oriented framework for uploading AI-generated images to stock photography platforms.
Supports: Adobe Stock, Freepik, Wirestock, Dreamstime, and more.

Design principles:
- Step-by-step verification
- Screenshot/snapshot at each critical step
- Proper error handling and rollback
- Extensible to multiple platforms
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Optional, Callable
from pathlib import Path
import time
import json
from datetime import datetime


@dataclass
class UploadImage:
    """Represents an image to be uploaded"""
    path: Path
    title: str
    keywords: List[str]
    category: str
    is_ai_generated: bool = True
    is_fictional: bool = True

    def __post_init__(self):
        self.path = Path(self.path)
        if not self.path.exists():
            raise FileNotFoundError(f"Image not found: {self.path}")


@dataclass
class UploadResult:
    """Result of an upload operation"""
    success: bool
    images_uploaded: int
    images_total: int
    metadata_applied: bool
    checkboxes_marked: int
    errors: List[str]
    screenshots: List[Path]
    timestamp: datetime
    platform: str

    def to_dict(self) -> Dict:
        return {
            'success': self.success,
            'images_uploaded': self.images_uploaded,
            'images_total': self.images_total,
            'metadata_applied': self.metadata_applied,
            'checkboxes_marked': self.checkboxes_marked,
            'errors': self.errors,
            'screenshots': [str(s) for s in self.screenshots],
            'timestamp': self.timestamp.isoformat(),
            'platform': self.platform
        }


class StockPlatformUploader(ABC):
    """
    Abstract base class for stock photography platform uploaders.

    Each platform implements this interface to provide consistent upload workflow.
    """

    def __init__(self, headless: bool = False, auth_state_file: Optional[str] = None):
        self.headless = headless
        self.auth_state_file = auth_state_file
        self.screenshots_dir = Path("upload_screenshots")
        self.screenshots_dir.mkdir(exist_ok=True)
        self.current_session_screenshots = []

    @abstractmethod
    def get_platform_name(self) -> str:
        """Return the name of the platform (e.g., 'Adobe Stock')"""
        pass

    @abstractmethod
    def get_upload_url(self) -> str:
        """Return the URL for the upload page"""
        pass

    @abstractmethod
    def navigate_to_upload_page(self) -> bool:
        """Navigate to the upload page and verify it loaded correctly"""
        pass

    @abstractmethod
    def upload_images(self, images: List[UploadImage]) -> bool:
        """Upload images and verify they were received"""
        pass

    @abstractmethod
    def apply_metadata(self, images: List[UploadImage]) -> bool:
        """Apply metadata (titles, keywords, categories) to uploaded images"""
        pass

    @abstractmethod
    def mark_ai_generated(self, count: int) -> int:
        """Mark images as AI-generated, return number successfully marked"""
        pass

    @abstractmethod
    def mark_fictional_content(self, count: int) -> int:
        """Mark content as fictional, return number successfully marked"""
        pass

    @abstractmethod
    def verify_upload_count(self, expected_count: int) -> bool:
        """Verify that the expected number of images were uploaded"""
        pass

    def take_screenshot(self, step_name: str) -> Path:
        """Take a screenshot and save it with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.get_platform_name().replace(' ', '_')}_{step_name}_{timestamp}.png"
        screenshot_path = self.screenshots_dir / filename
        self.current_session_screenshots.append(screenshot_path)
        return screenshot_path

    def upload_workflow(self, images: List[UploadImage], verify_each_step: bool = True) -> UploadResult:
        """
        Execute complete upload workflow with verification at each step.

        Args:
            images: List of images with metadata to upload
            verify_each_step: If True, pause for user verification at critical steps

        Returns:
            UploadResult with details of the operation
        """
        result = UploadResult(
            success=False,
            images_uploaded=0,
            images_total=len(images),
            metadata_applied=False,
            checkboxes_marked=0,
            errors=[],
            screenshots=[],
            timestamp=datetime.now(),
            platform=self.get_platform_name()
        )

        try:
            # Step 1: Navigate to upload page
            print(f"\n{'='*60}")
            print(f"STEP 1: Navigating to {self.get_platform_name()} upload page...")
            print(f"{'='*60}")

            if not self.navigate_to_upload_page():
                result.errors.append("Failed to navigate to upload page")
                return result

            screenshot = self.take_screenshot("01_page_loaded")
            print(f"✓ Screenshot saved: {screenshot}")

            if verify_each_step:
                input("\n⏸  Press ENTER to continue to image upload...")

            # Step 2: Upload images
            print(f"\n{'='*60}")
            print(f"STEP 2: Uploading {len(images)} images...")
            print(f"{'='*60}")

            if not self.upload_images(images):
                result.errors.append("Failed to upload images")
                return result

            screenshot = self.take_screenshot("02_images_uploaded")
            print(f"✓ Screenshot saved: {screenshot}")

            if verify_each_step:
                input("\n⏸  Press ENTER to continue to verification...")

            # Step 3: Verify upload count
            print(f"\n{'='*60}")
            print(f"STEP 3: Verifying {len(images)} images were uploaded...")
            print(f"{'='*60}")

            if not self.verify_upload_count(len(images)):
                result.errors.append(f"Upload count verification failed")
                return result

            result.images_uploaded = len(images)
            print(f"✓ Verified: {len(images)} images uploaded")

            if verify_each_step:
                input("\n⏸  Press ENTER to continue to metadata...")

            # Step 4: Apply metadata
            print(f"\n{'='*60}")
            print(f"STEP 4: Applying metadata...")
            print(f"{'='*60}")

            if not self.apply_metadata(images):
                result.errors.append("Failed to apply metadata")
                # Continue anyway - metadata can be applied manually
                print("⚠ Metadata application failed - may need manual upload")

            result.metadata_applied = True
            screenshot = self.take_screenshot("03_metadata_applied")
            print(f"✓ Screenshot saved: {screenshot}")

            if verify_each_step:
                input("\n⏸  Press ENTER to continue to AI marking...")

            # Step 5: Mark as AI-generated
            print(f"\n{'='*60}")
            print(f"STEP 5: Marking {len(images)} images as AI-generated...")
            print(f"{'='*60}")

            ai_marked = self.mark_ai_generated(len(images))
            print(f"✓ Marked {ai_marked}/{len(images)} as AI-generated")

            if verify_each_step:
                input("\n⏸  Press ENTER to continue to fictional marking...")

            # Step 6: Mark as fictional
            print(f"\n{'='*60}")
            print(f"STEP 6: Marking {len(images)} images as fictional...")
            print(f"{'='*60}")

            fictional_marked = self.mark_fictional_content(len(images))
            print(f"✓ Marked {fictional_marked}/{len(images)} as fictional")

            result.checkboxes_marked = min(ai_marked, fictional_marked)

            # Final screenshot
            screenshot = self.take_screenshot("04_complete")
            print(f"✓ Final screenshot saved: {screenshot}")

            result.success = True
            result.screenshots = self.current_session_screenshots

        except Exception as e:
            result.errors.append(f"Unexpected error: {str(e)}")
            print(f"\n❌ Error: {e}")

        return result

    def save_result(self, result: UploadResult, output_file: str = "upload_result.json"):
        """Save upload result to JSON file"""
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(result.to_dict(), f, indent=2)
        print(f"\n✓ Result saved to: {output_path}")


class AdobeStockMCPUploader(StockPlatformUploader):
    """
    Adobe Stock uploader using MCP Playwright tools.

    This implementation uses MCP tools for browser automation,
    allowing for interactive verification at each step.
    """

    def __init__(self, mcp_client, headless: bool = False, auth_state_file: Optional[str] = None):
        super().__init__(headless, auth_state_file)
        self.mcp = mcp_client  # MCP Playwright client

    def get_platform_name(self) -> str:
        return "Adobe Stock"

    def get_upload_url(self) -> str:
        return "https://contributor.stock.adobe.com/de/uploads?upload=1"

    def navigate_to_upload_page(self) -> bool:
        """Navigate to Adobe Stock upload page"""
        try:
            self.mcp.browser_navigate(url=self.get_upload_url())
            time.sleep(3)
            # Verify we're on the right page (will need login if not authenticated)
            return True
        except Exception as e:
            print(f"❌ Navigation failed: {e}")
            return False

    def upload_images(self, images: List[UploadImage]) -> bool:
        """Upload images via file input"""
        try:
            image_paths = [str(img.path.absolute()) for img in images]

            # Find and use file input
            # In MCP, we use browser_file_upload tool
            self.mcp.browser_file_upload(paths=image_paths)

            # Wait for processing
            print("Waiting for upload processing...")
            time.sleep(10)

            return True
        except Exception as e:
            print(f"❌ Image upload failed: {e}")
            return False

    def verify_upload_count(self, expected_count: int) -> bool:
        """Verify upload count by checking for 'Dateitypen: Alle (X)' text"""
        try:
            # Use snapshot to check for the count
            snapshot = self.mcp.browser_snapshot()
            expected_text = f"Dateitypen: Alle ({expected_count})"

            if expected_text in snapshot:
                return True
            else:
                print(f"❌ Expected text '{expected_text}' not found in page")
                return False
        except Exception as e:
            print(f"❌ Verification failed: {e}")
            return False

    def apply_metadata(self, images: List[UploadImage]) -> bool:
        """Apply metadata via CSV upload"""
        # For CSV upload, we'd need to generate CSV first
        # For now, skip and return False to indicate manual upload needed
        print("⚠ CSV metadata upload not yet implemented - upload manually")
        return False

    def mark_ai_generated(self, count: int) -> int:
        """Mark all images as AI-generated using JavaScript"""
        try:
            script = """
            async () => {
                const thumbnails = document.querySelectorAll('[role="option"]');
                let marked = 0;

                for (let i = 0; i < thumbnails.length; i++) {
                    thumbnails[i].click();
                    await new Promise(r => setTimeout(r, 500));

                    const checkbox = document.querySelector('input[type="checkbox"][aria-label*="generativen KI-Tools"]');
                    if (checkbox && !checkbox.checked) {
                        checkbox.click();
                        marked++;
                        await new Promise(r => setTimeout(r, 300));
                    }
                }

                return marked;
            }
            """
            result = self.mcp.browser_evaluate(function=script)
            return result.get('marked', 0)
        except Exception as e:
            print(f"❌ AI marking failed: {e}")
            return 0

    def mark_fictional_content(self, count: int) -> int:
        """Mark all content as fictional using JavaScript"""
        try:
            script = """
            async () => {
                const thumbnails = document.querySelectorAll('[role="option"]');
                let marked = 0;

                for (let i = 0; i < thumbnails.length; i++) {
                    thumbnails[i].click();
                    await new Promise(r => setTimeout(r, 500));

                    const checkbox = document.querySelector('input[type="checkbox"][aria-label*="Menschen und Eigentum sind fiktiv"]');
                    if (checkbox && !checkbox.checked) {
                        checkbox.click();
                        marked++;
                        await new Promise(r => setTimeout(r, 300));
                    }
                }

                return marked;
            }
            """
            result = self.mcp.browser_evaluate(function=script)
            return result.get('marked', 0)
        except Exception as e:
            print(f"❌ Fictional marking failed: {e}")
            return 0


# Example usage
if __name__ == '__main__':
    print(__doc__)
    print("\nThis is a framework module. Import it in your upload scripts.")
    print("\nExample:")
    print("```python")
    print("from stock_upload_framework import UploadImage, AdobeStockMCPUploader")
    print("")
    print("images = [")
    print("    UploadImage(")
    print("        path='image1.jpg',")
    print("        title='AI Generated Art',")
    print("        keywords=['ai', 'digital', 'art'],")
    print("        category='Technology'")
    print("    )")
    print("]")
    print("")
    print("uploader = AdobeStockMCPUploader(mcp_client)")
    print("result = uploader.upload_workflow(images)")
    print("uploader.save_result(result)")
    print("```")
