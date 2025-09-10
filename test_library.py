"""Test script for Perspectra library."""

from perspectra_lib import PerspectraProcessor, PerspectraConfig
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

# Add the library to path for testing
sys.path.insert(0, str(Path(__file__).parent))


def create_test_image():
    """Create a simple test image for testing."""
    # Create a simple test image with a white rectangle on black background
    image = np.zeros((400, 600, 3), dtype=np.uint8)

    # Add a white rectangle (simulating a document)
    image[100:300, 150:450] = [255, 255, 255]

    # Add some noise to make it more realistic
    noise = np.random.randint(0, 50, image.shape, dtype=np.uint8)
    image = np.clip(image.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # Convert to PIL and save
    pil_image = Image.fromarray(image)

    # Save to temporary file
    temp_path = tempfile.mktemp(suffix=".jpg")
    pil_image.save(temp_path, "JPEG")

    return temp_path


def test_basic_functionality():
    """Test basic functionality of the library."""
    print("=== Testing Basic Functionality ===")

    # Create test image
    test_image_path = create_test_image()
    print(f"Created test image: {test_image_path}")

    try:
        # Initialize processor
        processor = PerspectraProcessor()
        print("✓ PerspectraProcessor initialized successfully")

        # Test processing from file
        success, error_msg, result_image, duration = processor.process_image_from_file(test_image_path)

        if success:
            print(f"✓ Image processed successfully in {duration:.2f} seconds")
            print(f"  Input image path: {test_image_path}")
            print(f"  Result image shape: {result_image.shape}")
            print(f"  Result image dtype: {result_image.dtype}")
        else:
            print(f"✗ Image processing failed: {error_msg}")
            return False

        # Test base64 output
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()

        success, error_msg, result_base64, duration = processor.process_image_to_base64(image_bytes)

        if success:
            print(f"✓ Base64 conversion successful in {duration:.2f} seconds")
            print(f"  Base64 length: {len(result_base64)} characters")
        else:
            print(f"✗ Base64 conversion failed: {error_msg}")
            return False

        return True

    except Exception as e:
        print(f"✗ Test failed with exception: {str(e)}")
        return False

    finally:
        # Clean up
        if Path(test_image_path).exists():
            Path(test_image_path).unlink()


def test_custom_configuration():
    """Test custom configuration."""
    print("\n=== Testing Custom Configuration ===")

    # Create test image
    test_image_path = create_test_image()

    try:
        # Create custom config
        config = PerspectraConfig(
            padding_ratio=0.15,
            save_transformed=False,  # Don't save debug images in test
            save_contours=False,
            log_level="ERROR"  # Minimize logging output
        )

        processor = PerspectraProcessor(config)
        print("✓ PerspectraProcessor with custom config initialized")

        # Test processing
        success, error_msg, result_image, duration = processor.process_image_from_file(test_image_path)

        if success:
            print(f"✓ Custom config processing successful in {duration:.2f} seconds")
            print(f"  Custom padding ratio: {config.padding_ratio}")
            return True
        else:
            print(f"✗ Custom config processing failed: {error_msg}")
            return False

    except Exception as e:
        print(f"✗ Custom config test failed: {str(e)}")
        return False

    finally:
        # Clean up
        if Path(test_image_path).exists():
            Path(test_image_path).unlink()


def test_error_handling():
    """Test error handling."""
    print("\n=== Testing Error Handling ===")

    try:
        processor = PerspectraProcessor()

        # Test with non-existent file
        success, error_msg, result_image, duration = processor.process_image_from_file("non_existent_file.jpg")

        if not success and "Failed to read image file" in error_msg:
            print("✓ Non-existent file error handling works correctly")
        else:
            print("✗ Non-existent file error handling failed")
            return False

        # Test with invalid bytes
        try:
            success, error_msg, result_image, duration = processor.process_image(b"invalid image data")
            if not success:
                print("✓ Invalid image data error handling works correctly")
            else:
                print("✗ Invalid image data should have failed")
                return False
        except Exception:
            print("✓ Invalid image data properly raises exception")

        return True

    except Exception as e:
        print(f"✗ Error handling test failed: {str(e)}")
        return False


def run_all_tests():
    """Run all tests."""
    print("Starting Perspectra Library Tests\n")

    tests = [
        test_basic_functionality,
        test_custom_configuration,
        test_error_handling
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {str(e)}")

    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
