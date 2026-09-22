#!/usr/bin/env python3
"""
Vision Module - Image Processing and Screenshot Capabilities
Extends Claude Bot with visual analysis and screenshot features
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
import base64
import json

logger = logging.getLogger(__name__)


class ImageProcessor:
    """Process and analyze images."""

    def __init__(self):
        self.supported_formats = ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp']
        self.max_image_size = 20 * 1024 * 1024  # 20MB
        logger.info("✓ Image Processor initialized")

    def load_image(self, image_path: str) -> Optional[bytes]:
        """Load image from file."""
        path = Path(image_path)

        if not path.exists():
            logger.error(f"✗ Image not found: {image_path}")
            return None

        if path.suffix.lower() not in self.supported_formats:
            logger.error(f"✗ Unsupported format: {path.suffix}")
            return None

        try:
            with open(path, 'rb') as f:
                image_data = f.read()

            if len(image_data) > self.max_image_size:
                logger.error(f"✗ Image too large: {len(image_data)} bytes")
                return None

            logger.info(f"✓ Loaded image: {image_path}")
            return image_data
        except Exception as e:
            logger.error(f"✗ Failed to load image: {e}")
            return None

    def encode_to_base64(self, image_data: bytes) -> str:
        """Encode image to base64."""
        return base64.b64encode(image_data).decode('utf-8')

    def get_image_info(self, image_path: str) -> Dict[str, Any]:
        """Get image metadata."""
        path = Path(image_path)

        if not path.exists():
            return {'error': 'File not found'}

        try:
            size = path.stat().st_size
            return {
                'path': str(path),
                'name': path.name,
                'format': path.suffix.lower(),
                'size_bytes': size,
                'size_mb': round(size / 1024 / 1024, 2),
                'modified': datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
            }
        except Exception as e:
            return {'error': str(e)}


class ScreenshotCapture:
    """Capture and manage screenshots."""

    def __init__(self, output_dir: str = "./screenshots"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.screenshots = []
        logger.info(f"✓ Screenshot Capture initialized - saving to {output_dir}")

    def capture_screen(self, name: Optional[str] = None) -> Optional[str]:
        """
        Capture screenshot.
        Note: Requires platform-specific implementation
        """
        logger.info("📸 Capturing screenshot...")

        # Generate filename
        if not name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"screenshot_{timestamp}.png"

        filepath = self.output_dir / name

        try:
            # Try to use PIL/Pillow if available
            try:
                from PIL import ImageGrab
                screenshot = ImageGrab.grab()
                screenshot.save(filepath)
                logger.info(f"✓ Screenshot saved: {filepath}")
                self.screenshots.append(str(filepath))
                return str(filepath)
            except ImportError:
                # Fallback: create a placeholder
                logger.warning("PIL not available - creating placeholder")
                self._create_placeholder(filepath)
                return str(filepath)
        except Exception as e:
            logger.error(f"✗ Failed to capture screenshot: {e}")
            return None

    def _create_placeholder(self, filepath: Path):
        """Create placeholder screenshot metadata."""
        metadata = {
            'type': 'screenshot_placeholder',
            'timestamp': datetime.now().isoformat(),
            'note': 'Screenshot functionality requires PIL/Pillow library',
            'install': 'pip install pillow',
        }
        with open(filepath.with_suffix('.json'), 'w') as f:
            json.dump(metadata, f, indent=2)

    def get_screenshot_history(self) -> List[str]:
        """Get list of captured screenshots."""
        return self.screenshots

    def list_screenshots(self) -> List[Dict[str, Any]]:
        """List all screenshots with metadata."""
        screenshots = []
        for file_path in self.output_dir.glob("*.png"):
            screenshots.append({
                'name': file_path.name,
                'path': str(file_path),
                'size': file_path.stat().st_size,
                'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            })
        return screenshots


class VisionAnalyzer:
    """Analyze images using Claude."""

    def __init__(self):
        self.image_processor = ImageProcessor()
        self.screenshot_capture = ScreenshotCapture()
        logger.info("✓ Vision Analyzer initialized")

    def analyze_image(self, image_path: str, prompt: str = "Describe this image") -> Dict[str, Any]:
        """Analyze image and return description."""
        logger.info(f"🔍 Analyzing image: {image_path}")

        # Load image
        image_data = self.image_processor.load_image(image_path)
        if not image_data:
            return {'error': 'Failed to load image'}

        # Get image info
        info = self.image_processor.get_image_info(image_path)

        # Encode to base64
        b64_image = self.image_processor.encode_to_base64(image_data)

        return {
            'status': 'ready_for_analysis',
            'image_info': info,
            'prompt': prompt,
            'image_size_kb': len(b64_image) / 1024,
            'note': 'Send to Claude for visual analysis',
        }

    def analyze_screenshot(self, name: Optional[str] = None) -> Dict[str, Any]:
        """Capture and analyze screenshot."""
        screenshot_path = self.screenshot_capture.capture_screen(name)
        if not screenshot_path:
            return {'error': 'Failed to capture screenshot'}

        return self.analyze_image(screenshot_path, "Analyze this screenshot")

    def batch_analyze(self, image_paths: List[str]) -> List[Dict[str, Any]]:
        """Analyze multiple images."""
        results = []
        for image_path in image_paths:
            result = self.analyze_image(image_path)
            results.append(result)
        return results


class DialogueBoxCapture:
    """Capture dialogue/conversation to image."""

    def __init__(self, output_dir: str = "./dialogue_captures"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.captures = []
        logger.info(f"✓ Dialogue Capture initialized - saving to {output_dir}")

    def capture_dialogue(self, dialogue: str, title: str = "Dialogue") -> Optional[str]:
        """
        Save dialogue/conversation as text with metadata.
        Can be converted to image using HTML/CSS rendering.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dialogue_{timestamp}.txt"
        filepath = self.output_dir / filename

        # Create dialogue file with metadata
        content = f"""DIALOGUE CAPTURE
=================
Title: {title}
Timestamp: {timestamp}
{'-' * 50}

{dialogue}

{'-' * 50}
Captured by Claude Local Bot v3.5
"""

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"✓ Dialogue captured: {filepath}")
            self.captures.append({
                'file': str(filepath),
                'title': title,
                'timestamp': timestamp,
            })
            return str(filepath)
        except Exception as e:
            logger.error(f"✗ Failed to capture dialogue: {e}")
            return None

    def create_dialogue_html(self, dialogue: str, title: str = "Dialogue") -> Optional[str]:
        """Create HTML version of dialogue for screenshot."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dialogue_{timestamp}.html"
        filepath = self.output_dir / filename

        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            padding: 24px;
        }}
        .header {{
            border-bottom: 2px solid #667eea;
            padding-bottom: 12px;
            margin-bottom: 20px;
        }}
        .title {{
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }}
        .timestamp {{
            font-size: 12px;
            color: #999;
            margin-top: 4px;
        }}
        .dialogue {{
            line-height: 1.8;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-size: 14px;
        }}
        .footer {{
            border-top: 1px solid #eee;
            margin-top: 20px;
            padding-top: 12px;
            font-size: 12px;
            color: #999;
            text-align: right;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="title">{title}</div>
            <div class="timestamp">{timestamp}</div>
        </div>
        <div class="dialogue">{dialogue}</div>
        <div class="footer">Captured by Claude Local Bot v3.5</div>
    </div>
</body>
</html>"""

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)

            logger.info(f"✓ Dialogue HTML created: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"✗ Failed to create dialogue HTML: {e}")
            return None


def main():
    """Test vision module."""
    print("\n🖼️  Claude Vision Module v3.5")
    print("=" * 60)
    print("Features:")
    print("  ✓ Image Analysis")
    print("  ✓ Screenshot Capture")
    print("  ✓ Dialogue Capture")
    print("  ✓ Batch Processing")
    print("=" * 60 + "\n")

    # Test Vision Analyzer
    analyzer = VisionAnalyzer()

    # Test Screenshot
    print("📸 Testing screenshot capture...")
    result = analyzer.screenshot_capture.capture_screen("test_capture")
    print(f"  Screenshot: {result}\n")

    # Test Dialogue Capture
    dialogue_capturer = DialogueBoxCapture()
    test_dialogue = """User: Hello Claude Bot!
Claude: Hi! How can I help you today?
User: Can you analyze this code?
Claude: Of course! Please share the code."""

    print("💬 Testing dialogue capture...")
    dialogue_path = dialogue_capturer.capture_dialogue(test_dialogue, "Sample Conversation")
    print(f"  Dialogue saved: {dialogue_path}\n")

    # Create HTML version
    print("🌐 Creating dialogue HTML...")
    html_path = dialogue_capturer.create_dialogue_html(test_dialogue, "Sample Conversation")
    print(f"  HTML created: {html_path}\n")

    print("✓ Vision Module tests completed!")


if __name__ == '__main__':
    main()
