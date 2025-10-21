#!/usr/bin/env python3
"""
Git Repository Fix - Quick fix for common Git repository issues
"""

import subprocess
import sys
import os

def run_command(cmd, capture_output=True):
    """Run a command and return exit code, stdout, stderr"""
    try:
        result = subprocess.run(cmd, capture_output=capture_output, text=True, shell=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def check_git_repo():
    """Check if current directory is a Git repository"""
    exit_code, stdout, stderr = run_command("git rev-parse --git-dir")
    return exit_code == 0

def list_remotes():
    """List current remotes"""
    exit_code, stdout, stderr = run_command("git remote -v")
    return stdout.strip()

def fix_repository_issue():
    """Fix common repository issues"""
    print("🔧 Git Repository Fix Tool")
    print("=" * 40)
    
    if not check_git_repo():
        print("❌ Not in a Git repository")
        print("\n💡 Solutions:")
        print("1. Navigate to a Git repository directory")
        print("2. Initialize a new repository:")
        print("   git init")
        return False
    
    print("✅ In a Git repository")
    
    # Check remotes
    remotes = list_remotes()
    if not remotes:
        print("❌ No remote repositories configured")
        print("\n💡 To fix this:")
        print("1. Create a repository on GitHub/GitLab")
        print("2. Add remote:")
        print("   git remote add origin <repository-url>")
        return False
    
    print("🌐 Current remotes:")
    print(remotes)
    
    # Test remote connection
    print("\n🔍 Testing remote connections...")
    exit_code, stdout, stderr = run_command("git ls-remote origin")
    
    if exit_code == 0:
        print("✅ Remote connection successful!")
        print("Available branches:")
        print(stdout)
        return True
    else:
        print(f"❌ Remote connection failed: {stderr}")
        
        if "Repository not found" in stderr:
            print("\n💡 Repository not found. Solutions:")
            print("1. Check if the repository URL is correct")
            print("2. Verify the repository exists on GitHub/GitLab")
            print("3. Create a new repository:")
            print("   - Go to GitHub/GitLab")
            print("   - Create new repository")
            print("   - Update remote URL:")
            print("   git remote set-url origin <new-repository-url>")
        
        elif "Authentication failed" in stderr:
            print("\n💡 Authentication failed. Solutions:")
            print("1. Use personal access token instead of password")
            print("2. Configure SSH keys")
            print("3. Update Git credentials")
        
        elif "Permission denied" in stderr:
            print("\n💡 Permission denied. Solutions:")
            print("1. Check if you have write access")
            print("2. Verify you're using the correct account")
            print("3. Contact repository owner for access")
        
        return False

def main():
    try:
        success = fix_repository_issue()
        
        if not success:
            print("\n🛠️ Quick Fix Options:")
            print("1. Create new repository on GitHub")
            print("2. Update remote URL")
            print("3. Use Git Helper Dialogue to manage remotes")
            
            choice = input("\n👉 Enter your choice (1-3) or 'q' to quit: ").strip()
            
            if choice == "1":
                print("\n📝 Steps to create new repository:")
                print("1. Go to https://github.com/new")
                print("2. Enter repository name")
                print("3. Choose public/private")
                print("4. Don't initialize with README (since you have local files)")
                print("5. Copy the repository URL")
                print("6. Run: git remote add origin <repository-url>")
                print("7. Run: git push -u origin main")
            
            elif choice == "2":
                new_url = input("Enter new repository URL: ").strip()
                if new_url:
                    exit_code, stdout, stderr = run_command(f"git remote set-url origin {new_url}")
                    if exit_code == 0:
                        print("✅ Remote URL updated!")
                        print("Test connection:")
                        exit_code, stdout, stderr = run_command("git ls-remote origin")
                        if exit_code == 0:
                            print("✅ Connection successful!")
                        else:
                            print(f"❌ Still having issues: {stderr}")
                    else:
                        print(f"❌ Failed to update URL: {stderr}")
            
            elif choice == "3":
                print("\n🚀 Starting Git Helper Dialogue...")
                run_command("python git_helper_dialogue.py", capture_output=False)
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
