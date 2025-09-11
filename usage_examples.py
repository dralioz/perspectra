"""
Practical usage examples for different background removal methods
"""

from perspectra_lib import PerspectraProcessor, PerspectraConfig
import cv2


def real_time_mobile_app():
    """Example: Real-time mobile app processing"""
    print("📱 Real-time Mobile App Example")
    print("-" * 40)

    # Ultra-fast for real-time performance
    config = PerspectraConfig(
        background_method="watershed",  # 9ms processing
        enable_logging=False           # No logging overhead
    )

    processor = PerspectraProcessor(config)

    # Simulate camera capture processing
    print("Simulating real-time camera processing...")
    success, error, result, duration = processor.process_image_from_file(
        "test_image.jpg")

    if success:
        print(f"✅ Frame processed in {duration*1000:.1f}ms")
        print(f"   FPS capability: ~{1/duration:.0f} fps")
        return True
    else:
        print(f"❌ Processing failed: {error}")
        return False


def document_scanner():
    """Example: Document scanning application"""
    print("📄 Document Scanner Example")
    print("-" * 40)

    # Optimized for clean document backgrounds
    config = PerspectraConfig(
        background_method="threshold",  # 104ms, perfect for documents
        preserve_aspect_ratio=True,     # Keep document proportions
        enable_logging=False
    )

    processor = PerspectraProcessor(config)

    # Process scanned document
    success, error, result, duration = processor.process_image_from_file(
        "document.jpg")

    if success:
        print(f"✅ Document processed in {duration*1000:.1f}ms")
        print("   Perfect for: office documents, receipts, notes")
        return True
    else:
        print(f"❌ Processing failed: {error}")
        return False


def ecommerce_product_photos():
    """Example: E-commerce product photo processing"""
    print("🛒 E-commerce Product Photos")
    print("-" * 40)

    # High quality for product photos
    config = PerspectraConfig(
        background_method="grabcut",    # 236ms, excellent edge detection
        background_color="white",       # White background for products
        enable_logging=False
    )

    processor = PerspectraProcessor(config)

    # Process product photo
    success, error, result, duration = processor.process_image_from_file(
        "product.jpg")

    if success:
        print(f"✅ Product photo processed in {duration*1000:.1f}ms")
        print("   Perfect for: clothing, electronics, furniture")
        return True
    else:
        print(f"❌ Processing failed: {error}")
        return False


def research_high_accuracy():
    """Example: Research/academic high accuracy processing"""
    print("🧪 Research High Accuracy")
    print("-" * 40)

    # Maximum accuracy for research
    config = PerspectraConfig(
        background_method="u2net",      # 971ms, highest accuracy
        model_type="u2net",            # Full model
        enable_logging=True,           # Detailed logging
        log_level="DEBUG"
    )

    processor = PerspectraProcessor(config)

    # Process research image
    success, error, result, duration = processor.process_image_from_file(
        "research_sample.jpg")

    if success:
        print(f"✅ Research image processed in {duration*1000:.1f}ms")
        print("   Perfect for: scientific analysis, detailed segmentation")
        return True
    else:
        print(f"❌ Processing failed: {error}")
        return False


def batch_processing_example():
    """Example: Batch processing multiple images"""
    print("⚡ Batch Processing Example")
    print("-" * 40)

    # Balanced speed/quality for batch work
    config = PerspectraConfig(
        background_method="u2net_lite",  # 831ms, good balance
        enable_logging=False           # Faster processing
    )

    processor = PerspectraProcessor(config)

    # Simulate batch processing
    image_files = ["image1.jpg", "image2.jpg", "image3.jpg"]  # Example files

    total_time = 0
    processed_count = 0

    for img_file in image_files:
        try:
            success, error, result, duration = processor.process_image_from_file(
                img_file)
            if success:
                # Save processed image
                output_file = f"processed_{img_file}"
                processor.save_processed_image(img_file, output_file)

                total_time += duration
                processed_count += 1
                print(f"✅ {img_file}: {duration*1000:.1f}ms")
            else:
                print(f"❌ {img_file}: {error}")
        except Exception as e:
            print(f"🔴 {img_file}: {e}")

    if processed_count > 0:
        avg_time = total_time / processed_count
        print(f"\n📊 Batch Results:")
        print(f"   Processed: {processed_count}/{len(image_files)} images")
        print(f"   Average time: {avg_time*1000:.1f}ms per image")
        print(f"   Total time: {total_time:.2f}s")


def adaptive_method_selection():
    """Example: Automatically choose method based on image characteristics"""
    print("🎯 Adaptive Method Selection")
    print("-" * 40)

    def choose_optimal_method(image_path):
        """Choose best method based on image analysis"""
        # This is a simplified example - you could add actual image analysis
        img = cv2.imread(image_path)
        if img is None:
            return "threshold"  # Default fallback

        height, width = img.shape[:2]
        total_pixels = height * width

        # Simple heuristics (you can make this more sophisticated)
        if total_pixels < 500000:  # Small images
            return "watershed"      # Ultra-fast
        elif total_pixels < 2000000:  # Medium images
            return "threshold"      # Fast
        else:  # Large images
            return "u2net_lite"     # Better quality for large images

    # Example usage
    test_images = ["small_doc.jpg", "medium_photo.jpg", "large_image.jpg"]

    for img_path in test_images:
        optimal_method = choose_optimal_method(img_path)

        config = PerspectraConfig(
            background_method=optimal_method,
            enable_logging=False
        )

        processor = PerspectraProcessor(config)
        print(f"📸 {img_path} → Using {optimal_method} method")


def main():
    """Run all examples"""
    print("🎯 PERSPECTRA USAGE EXAMPLES")
    print("=" * 50)
    print()

    examples = [
        real_time_mobile_app,
        document_scanner,
        ecommerce_product_photos,
        research_high_accuracy,
        batch_processing_example,
        adaptive_method_selection
    ]

    for example in examples:
        try:
            example()
            print()
        except Exception as e:
            print(f"❌ Example failed: {e}")
            print()


if __name__ == "__main__":
    main()
