"""Model performance comparison script."""

import time
from pathlib import Path

import numpy as np
from PIL import Image

from perspectra_lib import PerspectraProcessor, PerspectraConfig
from perspectra_lib.adapters.optimized_background_removal import OptimizedBackgroundRemovalAdapter


def create_test_image():
    """Create a test image for benchmarking."""
    # Create test document image
    image = np.ones((600, 800, 3), dtype=np.uint8) * 200
    image[150:450, 200:600] = [255, 255, 255]
    image[150:453, 200:203] = [0, 0, 0]
    image[150:453, 597:600] = [0, 0, 0]
    image[150:153, 200:600] = [0, 0, 0]
    image[450:453, 200:600] = [0, 0, 0]

    pil_image = Image.fromarray(image)
    pil_image.save('benchmark_test.jpg', 'JPEG')

    with open('benchmark_test.jpg', 'rb') as f:
        return f.read()


def benchmark_model(config, name, image_bytes, runs=3):
    """Benchmark a specific model configuration."""
    print(f"\n🧪 Testing {name}")
    print("-" * 50)

    try:
        # Test with optimized adapter
        adapter = OptimizedBackgroundRemovalAdapter(config)

        times = []
        for i in range(runs):
            start_time = time.time()
            result = adapter.remove_background_optimized(image_bytes)
            end_time = time.time()

            duration = end_time - start_time
            times.append(duration)
            print(f"   Run {i+1}: {duration:.3f}s")

        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        print(f"   Average: {avg_time:.3f}s")
        print(f"   Min: {min_time:.3f}s, Max: {max_time:.3f}s")
        print(f"   Result shape: {result.shape}")

        return avg_time, result

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return None, None


def main():
    """Run performance comparison."""
    print("🚀 Perspectra Model Performance Benchmark")
    print("=" * 60)

    # Create test image
    print("📸 Creating test image...")
    image_bytes = create_test_image()
    print(f"   Image size: {len(image_bytes)} bytes")

    # Test configurations
    configs = [
        {
            "name": "U2-Net Full (Current)",
            "config": PerspectraConfig(
                model_type="u2net",
                log_level="ERROR"
            )
        },
        {
            "name": "U2-Net Lite (Recommended)",
            "config": PerspectraConfig(
                model_type="u2net_lite",
                log_level="ERROR"
            )
        },
        {
            "name": "Silueta (Object Focused)",
            "config": PerspectraConfig(
                model_type="silueta",
                log_level="ERROR"
            )
        },
        {
            "name": "U2-Net with GPU (if available)",
            "config": PerspectraConfig(
                model_type="u2net",
                use_gpu=True,
                log_level="ERROR"
            )
        },
        {
            "name": "U2-Net Lite Optimized",
            "config": PerspectraConfig(
                model_type="u2net_lite",
                image_size=(224, 224),  # Smaller input
                ort_intra_op_num_threads=2,
                ort_inter_op_num_threads=1,
                log_level="ERROR"
            )
        }
    ]

    results = []

    for test_config in configs:
        avg_time, result = benchmark_model(
            test_config["config"],
            test_config["name"],
            image_bytes,
            runs=3
        )

        if avg_time is not None:
            results.append({
                "name": test_config["name"],
                "time": avg_time,
                "result": result
            })

    # Summary
    print("\n" + "=" * 60)
    print("📊 PERFORMANCE SUMMARY")
    print("=" * 60)

    if results:
        # Sort by performance
        results.sort(key=lambda x: x["time"])

        print(f"{'Model':<30} {'Avg Time':<12} {'Speedup':<10}")
        print("-" * 52)

        baseline = results[0]["time"]

        for i, result in enumerate(results):
            speedup = f"{baseline/result['time']:.1f}x" if result["time"] > 0 else "N/A"
            status = "🏆" if i == 0 else "⚡" if i == 1 else ""

            print(
                f"{result['name']:<30} {result['time']:.3f}s     {speedup:<10} {status}")

    print("\n💡 RECOMMENDATIONS:")
    print("-" * 60)
    if results:
        fastest = results[0]
        print(f"✅ Fastest: {fastest['name']} ({fastest['time']:.3f}s)")

        if len(results) > 1:
            speedup = results[-1]["time"] / fastest["time"]
            print(f"🚀 Speedup vs slowest: {speedup:.1f}x faster")

    print("\n🎯 NEXT STEPS:")
    print("- Consider using u2net_lite for 10-20x speedup")
    print("- Fine-tune model on your specific data")
    print("- Use smaller input sizes (224x224 vs 320x320)")
    print("- Enable GPU if available")
    print("- Consider model quantization for production")

    # Cleanup
    Path('benchmark_test.jpg').unlink(missing_ok=True)


if __name__ == "__main__":
    main()
