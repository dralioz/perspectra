"""Example usage of Perspectra library."""

import time
from pathlib import Path

from perspectra_lib import PerspectraProcessor, PerspectraConfig


def main():
    """Demonstrate basic usage of Perspectra library."""

    # Example 1: Basic usage with default configuration
    print("=== Example 1: Basic Usage ===")
    processor = PerspectraProcessor()

    # Check if we have a test image
    input_path = "test_image.jpg"
    if not Path(input_path).exists():
        print(f"Test image '{input_path}' not found. Please add a test image.")
        print("Skipping basic usage example.")
    else:
        success, error_msg, result_image, duration = processor.process_image_from_file(input_path)

        if success:
            print(f"✓ Processing completed successfully in {duration:.2f} seconds")
            print(f"  Result image shape: {result_image.shape}")

            # Save the result
            output_path = "output_basic.jpg"
            success_save, error_save, _ = processor.save_processed_image(input_path, output_path)
            if success_save:
                print(f"✓ Result saved to '{output_path}'")
            else:
                print(f"✗ Error saving result: {error_save}")
        else:
            print(f"✗ Processing failed: {error_msg}")

    print("\n" + "=" * 50 + "\n")

    # Example 2: Advanced configuration with debugging
    print("=== Example 2: Advanced Configuration ===")

    config = PerspectraConfig(
        padding_ratio=0.1,  # 10% padding
        save_transformed=True,  # Save debug images
        save_contours=True,  # Save contour debug images
        contours_path="debug_output",  # Custom debug directory
        log_level="DEBUG"  # Detailed logging
    )

    processor_advanced = PerspectraProcessor(config)

    if Path(input_path).exists():
        print("Processing with advanced configuration...")
        success, error_msg, result_image, duration = processor_advanced.process_image_from_file(input_path)

        if success:
            print(f"✓ Advanced processing completed in {duration:.2f} seconds")
            print(f"  Check 'debug_output' directory for debug images")

            # Save with different name
            output_path = "output_advanced.jpg"
            success_save, error_save, _ = processor_advanced.save_processed_image(input_path, output_path)
            if success_save:
                print(f"✓ Advanced result saved to '{output_path}'")
        else:
            print(f"✗ Advanced processing failed: {error_msg}")

    print("\n" + "=" * 50 + "\n")

    # Example 3: Working with base64
    print("=== Example 3: Base64 Output ===")

    if Path(input_path).exists():
        with open(input_path, 'rb') as f:
            image_bytes = f.read()

        success, error_msg, result_base64, duration = processor.process_image_to_base64(image_bytes)

        if success:
            print(f"✓ Base64 processing completed in {duration:.2f} seconds")
            print(f"  Base64 result length: {len(result_base64)} characters")
            print(f"  First 50 characters: {result_base64[:50]}...")
        else:
            print(f"✗ Base64 processing failed: {error_msg}")

    print("\n" + "=" * 50 + "\n")

    # Example 4: Batch processing
    print("=== Example 4: Batch Processing ===")

    # Create some test files (if they don't exist, this will just skip)
    test_files = ["test1.jpg", "test2.jpg", "test3.png"]
    existing_files = [f for f in test_files if Path(f).exists()]

    if existing_files:
        print(f"Processing {len(existing_files)} test files...")

        total_start = time.time()
        for i, file_path in enumerate(existing_files):
            print(f"  Processing {file_path}... ", end="")

            success, error_msg, _, duration = processor.process_image_from_file(file_path)

            if success:
                output_path = f"batch_output_{i+1}.jpg"
                processor.save_processed_image(file_path, output_path)
                print(f"✓ Done in {duration:.2f}s -> {output_path}")
            else:
                print(f"✗ Failed: {error_msg}")

        total_time = time.time() - total_start
        print(f"\n  Batch processing completed in {total_time:.2f} seconds")
        print(f"  Average time per image: {total_time/len(existing_files):.2f} seconds")
    else:
        print("No test files found for batch processing.")
        print("Create files named 'test1.jpg', 'test2.jpg', 'test3.png' to test batch processing.")

    print("\n" + "=" * 50 + "\n")
    print("Example completed! Check the output files and debug directory.")


if __name__ == "__main__":
    main()
