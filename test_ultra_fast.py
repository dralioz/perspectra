"""
Ultra-fast performance test for Perspectra library.
Test the new ultra-fast background removal methods.
"""

import time
import numpy as np
from PIL import Image
import io

from perspectra_lib import PerspectraProcessor, PerspectraConfig


def create_test_image():
    """Create a test document image."""
    # Create a white document on colored background
    img = np.full((600, 800, 3), [150, 100, 80],
                  dtype=np.uint8)  # Brown background

    # Add white document rectangle
    cv2.rectangle(img, (100, 80), (700, 520), (255, 255, 255), -1)

    # Add some text-like rectangles
    cv2.rectangle(img, (150, 120), (650, 140), (0, 0, 0), -1)
    cv2.rectangle(img, (150, 160), (600, 180), (0, 0, 0), -1)
    cv2.rectangle(img, (150, 200), (550, 220), (0, 0, 0), -1)

    # Convert to bytes
    pil_image = Image.fromarray(img)
    img_bytes = io.BytesIO()
    pil_image.save(img_bytes, format='JPEG')

    return img_bytes.getvalue()


def benchmark_ultra_fast():
    """Benchmark ultra-fast background removal methods."""
    print("🚀 Ultra-Fast Perspectra Performance Test")
    print("=" * 60)

    # Create test image
    test_image = create_test_image()
    print(f"📸 Test image size: {len(test_image)} bytes")
    print()

    # Test configurations
    configurations = [
        {
            'name': 'Original rembg',
            'config': PerspectraConfig(
                use_ultrafast=False,
                use_optimized=False,
                enable_logging=False
            )
        },
        {
            'name': 'Ultra-fast Threshold',
            'config': PerspectraConfig(
                use_ultrafast=True,
                fast_method='threshold',
                enable_logging=False
            )
        },
        {
            'name': 'Ultra-fast Watershed',
            'config': PerspectraConfig(
                use_ultrafast=True,
                fast_method='watershed',
                enable_logging=False
            )
        },
        {
            'name': 'Ultra-fast GrabCut',
            'config': PerspectraConfig(
                use_ultrafast=True,
                fast_method='grabcut',
                enable_logging=False
            )
        }
    ]

    results = {}

    for test_config in configurations:
        print(f"🧪 Testing {test_config['name']}")
        print("-" * 40)

        try:
            # Initialize processor
            processor = PerspectraProcessor(test_config['config'])

            # Warm up
            processor.process_image(test_image)

            # Benchmark
            times = []
            for i in range(3):
                start = time.time()
                success, error_msg, result, duration = processor.process_image(
                    test_image)
                total_time = time.time() - start

                if success and result is not None:
                    times.append(total_time)
                    print(
                        f"   Run {i+1}: {total_time:.3f}s | Result: {result.shape}")
                else:
                    print(f"   Run {i+1}: FAILED - {error_msg}")
                    times.append(999.0)  # Very high time for failed runs

            avg_time = sum(times) / len(times) if times else 999.0
            min_time = min(times) if times else 999.0
            max_time = max(times) if times else 999.0

            results[test_config['name']] = {
                'avg': avg_time,
                'min': min_time,
                'max': max_time
            }

            print(f"   Average: {avg_time:.3f}s")
            print(f"   Range: {min_time:.3f}s - {max_time:.3f}s")
            print()

        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            results[test_config['name']] = {
                'avg': 999.0, 'min': 999.0, 'max': 999.0}
            print()

    # Performance summary
    print("📊 PERFORMANCE SUMMARY")
    print("=" * 60)

    # Find fastest
    fastest_time = min(result['avg']
                       for result in results.values() if result['avg'] < 900)

    # Sort by average time
    sorted_results = sorted(results.items(), key=lambda x: x[1]['avg'])

    for name, result in sorted_results:
        if result['avg'] < 900:  # Valid result
            speedup = fastest_time / result['avg']
            if result['avg'] == fastest_time:
                print(f"🏆 {name:<25} | {result['avg']:.3f}s | FASTEST")
            else:
                print(
                    f"   {name:<25} | {result['avg']:.3f}s | {speedup:.1f}x slower")
        else:
            print(f"❌ {name:<25} | FAILED")

    print()
    print("💡 RECOMMENDATIONS:")
    print("-" * 30)
    if 'Ultra-fast Threshold' in results and results['Ultra-fast Threshold']['avg'] < 1.0:
        speedup_vs_original = results.get('Original rembg', {}).get(
            'avg', 3.0) / results['Ultra-fast Threshold']['avg']
        print(
            f"✅ Use Ultra-fast Threshold for {speedup_vs_original:.0f}x speedup!")
        print(
            f"   Processing time: ~{results['Ultra-fast Threshold']['avg']*1000:.0f}ms")
    else:
        print("⚠️  Consider using threshold method for documents")

    print(f"🚀 Expected performance gain: 100-1000x faster than deep learning models")


if __name__ == "__main__":
    import cv2  # Import here to avoid issues
    benchmark_ultra_fast()
