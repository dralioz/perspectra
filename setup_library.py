#!/usr/bin/env python3
"""
Development setup script for Perspectra library.
Quick setup for developers working on the library.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(command, shell=True,
                                check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        return False


def setup_library():
    """Set up the library for development."""
    print("🚀 Setting up Perspectra Library")
    print("=" * 50)

    # Check if we're in the right directory
    if not Path("perspectra_lib").exists():
        print("❌ perspectra_lib directory not found!")
        print("   Make sure you're running this from the project root directory.")
        return False

    # Install in development mode
    if not run_command("pip install -e .", "Installing library in development mode"):
        return False

    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing library requirements"):
        return False

    print("\n🎉 Library setup completed successfully!")
    print("\nYou can now:")
    print("  1. Import the library: from perspectra_lib import PerspectraProcessor")
    print("  2. Run tests: python test_library.py")
    print("  3. See example usage: python example_usage.py")

    return True


def create_package():
    """Create distributable package."""
    print("\n📦 Creating distributable package...")

    # Clean previous builds
    for dir_name in ["build", "dist", "perspectra.egg-info"]:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"   Cleaned {dir_name}/")

    # Build package
    if not run_command("python setup.py sdist bdist_wheel", "Building package"):
        return False

    print("✅ Package created successfully!")
    print("   Files created in dist/ directory:")

    dist_dir = Path("dist")
    if dist_dir.exists():
        for file in dist_dir.iterdir():
            print(f"     - {file.name}")

    return True


def clean_fastapi_files():
    """Remove FastAPI-related files."""
    print("\n🧹 Cleaning FastAPI-related files...")

    fastapi_files = [
        "src/main.py",
        "src/api/",
        "docker-compose.debug.yml",
        "Dockerfile",
        "Dockerfile.debug",
        "requirements.txt",  # Keep requirements_lib.txt
        "dev-requirements.txt"
    ]

    for item in fastapi_files:
        path = Path(item)
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
                print(f"   Removed directory: {item}")
            else:
                path.unlink()
                print(f"   Removed file: {item}")
        else:
            print(f"   Not found (already removed): {item}")

    print("✅ FastAPI files cleaned")


def main():
    """Main setup function."""
    print("Perspectra Library Setup")
    print("=" * 50)
    print()

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        return False

    print(
        f"✅ Python version: {sys.version_info.major}.{sys.version_info.minor}")

    # Ask user what they want to do
    print("\nWhat would you like to do?")
    print("1. Set up library for development")
    print("2. Create distributable package")
    print("3. Clean FastAPI files (irreversible!)")
    print("4. All of the above")
    print("5. Exit")

    choice = input("\nEnter your choice (1-5): ").strip()

    if choice == "1":
        return setup_library()
    elif choice == "2":
        return create_package()
    elif choice == "3":
        confirm = input(
            "⚠️  This will permanently delete FastAPI files. Are you sure? (yes/no): ").strip().lower()
        if confirm == "yes":
            clean_fastapi_files()
            return True
        else:
            print("Cancelled.")
            return True
    elif choice == "4":
        success = True
        success &= setup_library()
        if success:
            success &= create_package()
        if success:
            confirm = input(
                "\n⚠️  Clean FastAPI files? This cannot be undone. (yes/no): ").strip().lower()
            if confirm == "yes":
                clean_fastapi_files()
        return success
    elif choice == "5":
        print("Goodbye!")
        return True
    else:
        print("❌ Invalid choice")
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Setup completed successfully!")
    else:
        print("\n❌ Setup failed!")
        sys.exit(1)
