"""
Test all background methods with new unified configuration
"""

import time
import numpy as np
from PIL import Image
import cv2
import io

from perspectra_lib import PerspectraProcessor, PerspectraConfig


def create_test_image():
    """Create test document image"""
    img = np.full((400, 600, 3), [200, 180, 160], dtype=np.uint8)
    # White document
    cv2.rectangle(img, (100, 50), (500, 350), (255, 255, 255), -1)
    # Some content
    cv2.rectangle(img, (130, 80), (450, 90), (0, 0, 0), -1)
    cv2.rectangle(img, (130, 110), (400, 120), (0, 0, 0), -1)

    pil_img = Image.fromarray(img)
    buffer = io.BytesIO()
    pil_img.save(buffer, format='JPEG')
    return buffer.getvalue()


def test_all_background_methods():
    """Test all available background removal methods"""
    print("🧪 Testing All Background Methods")
    print("=" * 60)

    test_image = create_test_image()
    print(f"📸 Test image: {len(test_image)} bytes")
    print()

    # Test configurations
    methods = [
        # Ultra-fast OpenCV methods
        {
            'name': 'Threshold (Ultra-fast)',
            'config': PerspectraConfig(
                background_method="threshold",
                enable_logging=False
            ),
            'expected_time': '5-100ms'
        },
        {
            'name': 'Watershed (Ultra-fast)',
            'config': PerspectraConfig(
                background_method="watershed",
                enable_logging=False
            ),
            'expected_time': '5-20ms'
        },
        {
            'name': 'GrabCut (Ultra-fast)',
            'config': PerspectraConfig(
                background_method="grabcut",
                enable_logging=False
            ),
            'expected_time': '100-500ms'
        },
        # Deep learning methods
        {
            'name': 'U2Net (Standard)',
            'config': PerspectraConfig(
                background_method="u2net",
                enable_logging=False
            ),
            'expected_time': '1000-3000ms'
        },
        {
            'name': 'U2Net Lite (Faster)',
            'config': PerspectraConfig(
                background_method="u2net_lite",
                enable_logging=False
            ),
            'expected_time': '200-800ms'
        },
        {
            'name': 'Silueta (Object-focused)',
            'config': PerspectraConfig(
                background_method="silueta",
                enable_logging=False
            ),
            'expected_time': '500-1500ms'
        }
    ]

    results = []

    for method in methods:
        print(f"🔬 Testing: {method['name']}")
        print(f"   Expected: {method['expected_time']}")
        print("-" * 40)

        try:
            processor = PerspectraProcessor(method['config'])

            # Test processing
            start = time.time()
            success, error, result, duration = processor.process_image(
                test_image)
            total_time = time.time() - start

            if success and result is not None:
                print(f"   ✅ SUCCESS")
                print(f"   📏 Result shape: {result.shape}")
                print(f"   ⚡ Total time: {total_time*1000:.1f}ms")
                print(f"   🎯 Processing time: {duration*1000:.1f}ms")
                results.append({
                    'name': method['name'],
                    'time': total_time,
                    'processing_time': duration,
                    'success': True
                })
            else:
                print(f"   ❌ FAILED: {error}")
                results.append({
                    'name': method['name'],
                    'time': 999.0,
                    'processing_time': 999.0,
                    'success': False
                })

        except Exception as e:
            print(f"   🔴 ERROR: {e}")
            results.append({
                'name': method['name'],
                'time': 999.0,
                'processing_time': 999.0,
                'success': False
            })

        print()

    # Performance summary
    print("📊 PERFORMANCE SUMMARY")
    print("=" * 60)

    successful_results = [r for r in results if r['success']]

    if successful_results:
        # Sort by processing time
        successful_results.sort(key=lambda x: x['processing_time'])

        print(f"{'Method':<25} {'Time':<10} {'Category':<12} {'Status'}")
        print("-" * 60)

        for result in successful_results:
            time_ms = result['processing_time'] * 1000

            if time_ms < 50:
                category = "Ultra-fast"
                emoji = "🏆"
            elif time_ms < 200:
                category = "Fast"
                emoji = "⚡"
            elif time_ms < 1000:
                category = "Medium"
                emoji = "🔥"
            else:
                category = "Slow"
                emoji = "🐌"

            print(
                f"{emoji} {result['name']:<23} {time_ms:7.1f}ms {category:<12} ✅")

        # Show failed ones
        failed_results = [r for r in results if not r['success']]
        for result in failed_results:
            print(f"❌ {result['name']:<23} {'FAILED':<10} {'N/A':<12} ❌")

    print("\n💡 USAGE RECOMMENDATIONS")
    print("-" * 30)
    print("🏃‍♂️ Real-time apps    → threshold/watershed")
    print("📄 Document scanning → threshold")
    print("🛒 E-commerce photos → grabcut")
    print("🧪 Research quality  → u2net")
    print("⚖️  Balanced option  → u2net_lite")


if __name__ == "__main__":
    test_all_background_methods()
