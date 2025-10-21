#!/usr/bin/env python3
"""
Git Helper Setup - Initialize Git repository and run Git Helper
"""

import subprocess
import sys
import os

def check_git_installed():
    """Check if Git is installed"""
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def is_git_repo():
    """Check if current directory is a Git repository"""
    try:
        subprocess.run(['git', 'rev-parse', '--git-dir'], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def init_git_repo():
    """Initialize a new Git repository"""
    print("🔧 Initializing new Git repository...")
    try:
        subprocess.run(['git', 'init'], check=True)
        print("✅ Git repository initialized successfully!")
        
        # Create initial commit if there are files
        try:
            subprocess.run(['git', 'add', '.'], check=True)
            subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
            print("✅ Initial commit created!")
        except subprocess.CalledProcessError:
            print("ℹ️ No files to commit yet")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to initialize Git repository: {e}")
        return False

def main():
    print("🔧 Git Helper Setup")
    print("=" * 30)
    
    # Check if Git is installed
    if not check_git_installed():
        print("❌ Git is not installed or not in PATH")
        print("\n💡 Please install Git first:")
        print("- Windows: https://git-scm.com/download/win")
        print("- macOS: brew install git")
        print("- Linux: sudo apt install git")
        sys.exit(1)
    
    print("✅ Git is installed")
    
    # Check if we're in a Git repository
    if is_git_repo():
        print("✅ Already in a Git repository")
        print(f"📁 Repository: {os.getcwd()}")
    else:
        print("❌ Not in a Git repository")
        print(f"📁 Current directory: {os.getcwd()}")
        
        response = input("\n❓ Would you like to initialize a Git repository here? (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            if init_git_repo():
                print("✅ Ready to use Git Helper!")
            else:
                print("❌ Failed to initialize repository")
                sys.exit(1)
        else:
            print("\n💡 To use Git Helper:")
            print("1. Navigate to a Git repository directory")
            print("2. Or run this setup script in a directory where you want to initialize Git")
            print("3. Or clone an existing repository:")
            print("   git clone <repository-url>")
            sys.exit(1)
    
    # Ask which Git Helper to run
    print("\n🎯 Choose Git Helper version:")
    print("1. Command-line version (git_helper.py)")
    print("2. Interactive dialogue version (git_helper_dialogue.py)")
    
    while True:
        try:
            choice = int(input("👉 Enter your choice (1 or 2): "))
            if choice == 1:
                print("\n🚀 Starting command-line Git Helper...")
                os.system(f"python {os.path.join(os.path.dirname(__file__), 'git_helper.py')} status")
                break
            elif choice == 2:
                print("\n🚀 Starting interactive Git Helper...")
                os.system(f"python {os.path.join(os.path.dirname(__file__), 'git_helper_dialogue.py')}")
                break
            else:
                print("❌ Please enter 1 or 2")
        except ValueError:
            print("❌ Please enter a valid number")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
