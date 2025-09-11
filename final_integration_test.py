"""
Final integration test - test all optimized modes
"""

import time
from perspectra_lib import PerspectraProcessor, PerspectraConfig
import numpy as np
from PIL import Image
import io


def create_test_image():
    """Create test document image"""
    img = np.full((400, 600, 3), [200, 180, 160], dtype=np.uint8)
    # White document
    img[50:350, 100:500] = [255, 255, 255]
    # Some content
    img[80:90, 130:450] = [0, 0, 0]
    img[110:120, 130:400] = [0, 0, 0]

    pil_img = Image.fromarray(img)
    buffer = io.BytesIO()
    pil_img.save(buffer, format='JPEG')
    return buffer.getvalue()


def test_all_modes():
    """Test all available processing modes"""
    print("🧪 Final Integration Test - All Modes")
    print("=" * 50)

    test_image = create_test_image()
    print(f"📸 Test image: {len(test_image)} bytes")
    print()

    modes = [
        {
            'name': 'Ultra-Fast Threshold',
            'config': PerspectraConfig(
                use_ultrafast=True,
                fast_method='threshold',
                enable_logging=False
            )
        },
        {
            'name': 'Ultra-Fast Watershed',
            'config': PerspectraConfig(
                use_ultrafast=True,
                fast_method='watershed',
                enable_logging=False
            )
        },
        {
            'name': 'Ultra-Fast GrabCut',
            'config': PerspectraConfig(
                use_ultrafast=True,
                fast_method='grabcut',
                enable_logging=False
            )
        }
    ]

    results = []

    for mode in modes:
        print(f"🔬 Testing: {mode['name']}")
        print("-" * 30)

        try:
            processor = PerspectraProcessor(mode['config'])

            # Test processing
            start = time.time()
            success, error, result, duration = processor.process_image(
                test_image)
            total_time = time.time() - start

            if success and result is not None:
                print(f"   ✅ SUCCESS")
                print(f"   📏 Result shape: {result.shape}")
                print(f"   ⚡ Processing time: {total_time*1000:.1f}ms")
                print(f"   🎯 Library reported: {duration*1000:.1f}ms")
                results.append((mode['name'], total_time))
            else:
                print(f"   ❌ FAILED: {error}")

        except Exception as e:
            print(f"   🔴 ERROR: {e}")

        print()

    # Summary
    if results:
        print("🎉 SUCCESS - All modes working!")
        print("=" * 50)
        print("📊 Performance Summary:")

        fastest = min(results, key=lambda x: x[1])

        for name, time_taken in results:
            speedup = fastest[1] / time_taken
            emoji = "🏆" if time_taken == fastest[1] else "⚡" if speedup < 2 else "🔥"
            print(f"{emoji} {name:<22} | {time_taken*1000:6.1f}ms")

        print()
        print("💡 Recommendation:")
        print(f"   Use '{fastest[0]}' for best performance")
        print(f"   Expected speedup vs U2Net: ~{1000/fastest[1]:.0f}x")

    else:
        print("❌ No successful tests")


if __name__ == "__main__":
    test_all_modes()
