#!/usr/bin/env python3
"""
Pantheon Legends Deployment Script

This script handles the complete deployment process for the Pantheon Legends package:
1. Version validation
2. Package building  
3. Quality checks
4. PyPI deployment
5. Git tagging
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n🔧 {description}")
    print(f"   Command: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error: {e}")
        if e.stdout:
            print(f"   Stdout: {e.stdout}")
        if e.stderr:
            print(f"   Stderr: {e.stderr}")
        return False

def validate_environment():
    """Validate that deployment environment is ready."""
    print("🛡️ Validating deployment environment...")
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ pyproject.toml not found. Are you in the project root?")
        return False
    
    # Check if build tools are available
    try:
        subprocess.run([sys.executable, "-m", "build", "--help"], 
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ build package not found. Installing...")
        if not run_command(f"{sys.executable} -m pip install build", "Installing build tools"):
            return False
    
    # Check if twine is available
    try:
        subprocess.run([sys.executable, "-m", "twine", "--help"], 
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ twine package not found. Installing...")
        if not run_command(f"{sys.executable} -m pip install twine", "Installing twine"):
            return False
    
    print("✅ Environment validation passed")
    return True

def run_tests():
    """Run comprehensive tests."""
    print("\n🧪 Running comprehensive tests...")
    
    # Test package import
    if not run_command(f"{sys.executable} -c \"import legends; print('Package import: OK')\"", 
                      "Testing package import"):
        return False
    
    # Test enhanced framework
    if not run_command(f"{sys.executable} test_enhanced_framework.py", 
                      "Testing enhanced framework"):
        return False
    
    # Test consensus analysis
    if not run_command(f"{sys.executable} test_consensus.py", 
                      "Testing consensus analysis"):
        return False
    
    # Test installation
    if not run_command(f"{sys.executable} -c \"import legends; legends.test_installation()\"", 
                      "Testing installation"):
        return False
    
    print("✅ All tests passed")
    return True

def clean_build():
    """Clean previous build artifacts."""
    print("\n🧹 Cleaning previous builds...")
    
    dirs_to_clean = ["build", "dist", "*.egg-info"]
    for dir_pattern in dirs_to_clean:
        if run_command(f"rm -rf {dir_pattern}", f"Cleaning {dir_pattern}"):
            continue
        # Try Windows version
        run_command(f"rmdir /s /q {dir_pattern} 2>nul || del /q /s {dir_pattern} 2>nul || echo OK", 
                   f"Cleaning {dir_pattern} (Windows)")
    
    print("✅ Build cleanup completed")
    return True

def build_package():
    """Build the package."""
    print("\n📦 Building package...")
    
    if not run_command(f"{sys.executable} -m build", "Building wheel and source distribution"):
        return False
    
    # Verify build output
    dist_files = list(Path("dist").glob("*"))
    if len(dist_files) < 2:
        print("❌ Expected both wheel and source distribution")
        return False
    
    print("✅ Package built successfully")
    for file in dist_files:
        print(f"   📄 {file}")
    
    return True

def validate_package():
    """Validate the built package."""
    print("\n🔍 Validating package...")
    
    # Check package with twine
    if not run_command(f"{sys.executable} -m twine check dist/*", "Validating package with twine"):
        return False
    
    print("✅ Package validation passed")
    return True

def deploy_to_test_pypi():
    """Deploy to Test PyPI first."""
    print("\n🚀 Deploying to Test PyPI...")
    
    test_pypi_cmd = f"{sys.executable} -m twine upload --repository testpypi dist/*"
    
    print("   ⚠️  You'll need Test PyPI credentials")
    print("   📝 Create account at: https://test.pypi.org/account/register/")
    print("   🔑 Configure credentials with: python -m twine configure")
    
    if input("   Continue with Test PyPI upload? (y/N): ").lower() != 'y':
        print("   ⏭️  Skipping Test PyPI upload")
        return True
    
    return run_command(test_pypi_cmd, "Uploading to Test PyPI")

def deploy_to_pypi():
    """Deploy to production PyPI."""
    print("\n🚀 Deploying to Production PyPI...")
    
    pypi_cmd = f"{sys.executable} -m twine upload dist/*"
    
    print("   ⚠️  This will publish to PRODUCTION PyPI!")
    print("   🔑 You'll need PyPI credentials")
    
    if input("   Continue with Production PyPI upload? (y/N): ").lower() != 'y':
        print("   ⏭️  Skipping Production PyPI upload")
        return True
    
    return run_command(pypi_cmd, "Uploading to Production PyPI")

def create_git_tag():
    """Create and push git tag for release."""
    print("\n🏷️  Creating git tag...")
    
    # Get version from package
    try:
        result = subprocess.run([sys.executable, "-c", "import legends; print(legends.__version__)"], 
                              capture_output=True, text=True, check=True)
        version = result.stdout.strip()
    except:
        print("❌ Could not determine package version")
        return False
    
    tag_name = f"v{version}"
    
    # Check if tag already exists
    result = subprocess.run(["git", "tag", "-l", tag_name], capture_output=True, text=True)
    if tag_name in result.stdout:
        print(f"   ⚠️  Tag {tag_name} already exists")
        return True
    
    # Create tag
    if not run_command(f"git tag -a {tag_name} -m 'Release {version}'", f"Creating tag {tag_name}"):
        return False
    
    # Push tag
    if input(f"   Push tag {tag_name} to remote? (y/N): ").lower() == 'y':
        return run_command(f"git push origin {tag_name}", f"Pushing tag {tag_name}")
    
    print(f"   ✅ Tag {tag_name} created locally")
    return True

def main():
    """Main deployment process."""
    print("🚀 Pantheon Legends Deployment Script")
    print("=" * 50)
    
    steps = [
        ("Environment Validation", validate_environment),
        ("Test Suite", run_tests),
        ("Build Cleanup", clean_build),
        ("Package Building", build_package),
        ("Package Validation", validate_package),
        ("Test PyPI Deployment", deploy_to_test_pypi),
        ("Production PyPI Deployment", deploy_to_pypi),
        ("Git Tagging", create_git_tag),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        
        if not step_func():
            print(f"\n❌ Deployment failed at: {step_name}")
            print("   Please fix the issues and try again.")
            sys.exit(1)
    
    print("\n" + "="*50)
    print("🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!")
    print("✅ Package built and validated")
    print("✅ Tests passed")
    print("✅ Ready for PyPI distribution")
    print("✅ Git tagged for release")
    print("\n📦 Your Pantheon Legends package is ready!")

if __name__ == "__main__":
    main()
