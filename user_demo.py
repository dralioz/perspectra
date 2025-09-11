"""
Final user experience test - easy method selection
"""

from perspectra_lib import PerspectraProcessor, PerspectraConfig


def user_friendly_demo():
    """Demonstrate how easy it is for users to choose methods"""

    print("👤 USER-FRIENDLY DEMO")
    print("=" * 40)
    print()

    print("🎯 Method Selection Guide:")
    print("-" * 25)
    print("📱 Need real-time processing?     → watershed")
    print("📄 Processing documents?          → threshold")
    print("🛒 E-commerce product photos?     → grabcut")
    print("🧪 Research/maximum accuracy?     → u2net")
    print("⚖️  Want balanced speed/quality?  → u2net_lite")
    print()

    # Simulate user choices
    scenarios = [
        {
            'use_case': 'Mobile camera app',
            'method': 'watershed',
            'reason': 'Need <10ms processing for real-time'
        },
        {
            'use_case': 'Office document scanner',
            'method': 'threshold',
            'reason': 'Documents have clean backgrounds'
        },
        {
            'use_case': 'Online store product photos',
            'method': 'grabcut',
            'reason': 'Need high quality edge detection'
        },
        {
            'use_case': 'Academic research project',
            'method': 'u2net',
            'reason': 'Accuracy more important than speed'
        },
        {
            'use_case': 'Photo editing app',
            'method': 'u2net_lite',
            'reason': 'Good balance of speed and quality'
        }
    ]

    for scenario in scenarios:
        print(f"🎬 Scenario: {scenario['use_case']}")
        print(f"   💡 Recommended: {scenario['method']}")
        print(f"   📝 Why: {scenario['reason']}")

        # Show how simple the code is
        print(f"   💻 Code:")
        print(
            f"      config = PerspectraConfig(background_method='{scenario['method']}')")
        print(f"      processor = PerspectraProcessor(config)")
        print()

    print("✨ That's it! Just change one parameter to switch methods!")
    print()

    # Show backward compatibility
    print("🔄 BACKWARD COMPATIBILITY")
    print("-" * 25)
    print("Old way (still works):")
    print("   config = PerspectraConfig(use_ultrafast=True, fast_method='threshold')")
    print()
    print("New way (recommended):")
    print("   config = PerspectraConfig(background_method='threshold')")
    print()
    print("Both give the same result! 🎉")


if __name__ == "__main__":
    user_friendly_demo()
