#!/usr/bin/env python3
"""
PyPI publishing script for Perspectra library.
This script helps you publish the library to PyPI.
"""

import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        return False


def check_requirements():
    """Check if all requirements are met."""
    print("🔍 Checking requirements...")
    
    # Check if required files exist
    required_files = ["setup.py", "README.md", "LICENSE", "requirements.txt"]
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ Required file missing: {file}")
            return False
        print(f"✅ Found: {file}")
    
    # Check if perspectra_lib exists
    if not Path("perspectra_lib").exists():
        print("❌ perspectra_lib directory not found!")
        return False
    print("✅ Found: perspectra_lib/")
    
    return True


def install_build_tools():
    """Install required build tools."""
    tools = ["build", "twine"]
    for tool in tools:
        if not run_command(f"pip show {tool}", f"Checking {tool}"):
            if not run_command(f"pip install {tool}", f"Installing {tool}"):
                return False
    return True


def clean_build():
    """Clean previous build artifacts."""
    print("🧹 Cleaning previous builds...")
    
    dirs_to_clean = ["build", "dist", "perspectra.egg-info"]
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            import shutil
            shutil.rmtree(dir_path)
            print(f"   Removed: {dir_name}/")
    
    print("✅ Clean completed")
    return True


def build_package():
    """Build the package."""
    return run_command("python -m build", "Building package")


def check_package():
    """Check the built package."""
    return run_command("python -m twine check dist/*", "Checking package")


def upload_to_test_pypi():
    """Upload to Test PyPI."""
    print("\n📤 Uploading to Test PyPI...")
    print("   You'll need to enter your Test PyPI credentials.")
    return run_command(
        "python -m twine upload --repository testpypi dist/*",
        "Uploading to Test PyPI"
    )


def upload_to_pypi():
    """Upload to PyPI."""
    print("\n📤 Uploading to PyPI...")
    print("   You'll need to enter your PyPI credentials.")
    return run_command(
        "python -m twine upload dist/*",
        "Uploading to PyPI"
    )


def main():
    """Main publishing function."""
    print("🚀 Perspectra PyPI Publishing Script")
    print("=" * 50)
    
    if not check_requirements():
        print("❌ Requirements check failed!")
        return False
    
    print("\nWhat would you like to do?")
    print("1. Build package only")
    print("2. Build and upload to Test PyPI")
    print("3. Build and upload to PyPI (production)")
    print("4. Install build tools only")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        success = True
        success &= install_build_tools()
        success &= clean_build()
        success &= build_package()
        success &= check_package()
        
        if success:
            print("\n🎉 Package built successfully!")
            print("   Check the dist/ directory for the built files.")
            print("   You can now manually upload using:")
            print("     python -m twine upload --repository testpypi dist/*  # Test")
            print("     python -m twine upload dist/*                       # Production")
        
        return success
    
    elif choice == "2":
        success = True
        success &= install_build_tools()
        success &= clean_build()
        success &= build_package()
        success &= check_package()
        
        if success:
            success &= upload_to_test_pypi()
            
        if success:
            print("\n🎉 Package uploaded to Test PyPI!")
            print("   You can test install with:")
            print("     pip install -i https://test.pypi.org/simple/ perspectra")
        
        return success
    
    elif choice == "3":
        print("\n⚠️  WARNING: This will upload to production PyPI!")
        confirm = input("Are you sure? Type 'yes' to continue: ").strip().lower()
        
        if confirm != "yes":
            print("Cancelled.")
            return True
        
        success = True
        success &= install_build_tools()
        success &= clean_build()
        success &= build_package()
        success &= check_package()
        
        if success:
            success &= upload_to_pypi()
            
        if success:
            print("\n🎉 Package uploaded to PyPI!")
            print("   Users can now install with:")
            print("     pip install perspectra")
        
        return success
    
    elif choice == "4":
        return install_build_tools()
    
    elif choice == "5":
        print("Goodbye!")
        return True
    
    else:
        print("❌ Invalid choice")
        return False


if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Publishing failed!")
        sys.exit(1)
    else:
        print("\n✅ All done!")
