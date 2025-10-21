#!/usr/bin/env python3
"""
Git Helper Dialogue - Interactive Git operations tool
Provides a user-friendly dialogue interface for common Git operations
"""

import subprocess
import sys
import os
from typing import List, Optional, Tuple
from datetime import datetime

class GitHelperDialogue:
    def __init__(self):
        self.repo_path = self._get_repo_path()
        
    def _get_repo_path(self) -> str:
        """Get the current repository path"""
        try:
            result = subprocess.run(['git', 'rev-parse', '--show-toplevel'], 
                                 capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            print("❌ Error: Not in a Git repository")
            print("\n💡 To fix this:")
            print("1. Navigate to a Git repository directory")
            print("2. Or initialize a new Git repository:")
            print("   git init")
            print("3. Or clone an existing repository:")
            print("   git clone <repository-url>")
            print("\n📁 Current directory:", os.getcwd())
            sys.exit(1)
    
    def _run_git_command(self, args: List[str], capture_output: bool = True) -> Tuple[int, str, str]:
        """Run a git command and return exit code, stdout, stderr"""
        try:
            result = subprocess.run(['git'] + args, 
                                 capture_output=capture_output, text=True, cwd=self.repo_path)
            return result.returncode, result.stdout, result.stderr
        except FileNotFoundError:
            print("❌ Error: Git is not installed or not in PATH")
            sys.exit(1)
    
    def _get_user_input(self, prompt: str, default: str = None) -> str:
        """Get user input with optional default value"""
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip()
            return user_input if user_input else default
        return input(f"{prompt}: ").strip()
    
    def _show_menu(self, title: str, options: List[str]) -> int:
        """Display a menu and get user selection"""
        print(f"\n{'='*50}")
        print(f"🔧 {title}")
        print(f"{'='*50}")
        
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        print(f"{'='*50}")
        
        while True:
            try:
                choice = int(input("👉 Enter your choice: "))
                if 1 <= choice <= len(options):
                    return choice
                else:
                    print(f"❌ Please enter a number between 1 and {len(options)}")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def _confirm_action(self, message: str) -> bool:
        """Ask user to confirm an action"""
        response = input(f"❓ {message} (y/N): ").strip().lower()
        return response in ['y', 'yes']
    
    def show_status(self) -> None:
        """Show repository status"""
        print("\n📊 Repository Status:")
        print("=" * 50)
        
        # Show current branch
        exit_code, stdout, stderr = self._run_git_command(['branch', '--show-current'])
        current_branch = stdout.strip()
        print(f"🌿 Current branch: {current_branch}")
        
        # Show status
        exit_code, stdout, stderr = self._run_git_command(['status', '--porcelain'])
        if stdout.strip():
            print("\n📋 Changes:")
            print(stdout)
        else:
            print("\n✅ Working directory clean")
        
        # Show last commit
        exit_code, stdout, stderr = self._run_git_command(['log', '-1', '--oneline'])
        if stdout.strip():
            print(f"\n📝 Last commit: {stdout.strip()}")
        
        input("\n⏸️ Press Enter to continue...")
    
    def add_files(self) -> None:
        """Add files to staging area"""
        print("\n📁 Add Files to Staging")
        print("=" * 30)
        
        # Show current status
        exit_code, stdout, stderr = self._run_git_command(['status', '--porcelain'])
        if not stdout.strip():
            print("✅ No changes to add")
            input("\n⏸️ Press Enter to continue...")
            return
        
        print("📋 Available changes:")
        print(stdout)
        
        options = [
            "Add all changes",
            "Add specific files",
            "Add by pattern",
            "Back to main menu"
        ]
        
        choice = self._show_menu("Add Files", options)
        
        if choice == 1:  # Add all
            if self._confirm_action("Add all changes to staging?"):
                exit_code, stdout, stderr = self._run_git_command(['add', '.'])
                if exit_code == 0:
                    print("✅ All changes added to staging")
                else:
                    print(f"❌ Failed to add files: {stderr}")
        
        elif choice == 2:  # Add specific files
            files_input = self._get_user_input("Enter file paths (space-separated)")
            if files_input:
                files = files_input.split()
                for file in files:
                    exit_code, stdout, stderr = self._run_git_command(['add', file])
                    if exit_code == 0:
                        print(f"✅ Added {file}")
                    else:
                        print(f"❌ Failed to add {file}: {stderr}")
        
        elif choice == 3:  # Add by pattern
            pattern = self._get_user_input("Enter file pattern (e.g., *.py, src/**/*.js)")
            if pattern:
                exit_code, stdout, stderr = self._run_git_command(['add', pattern])
                if exit_code == 0:
                    print(f"✅ Added files matching pattern: {pattern}")
                else:
                    print(f"❌ Failed to add files: {stderr}")
        
        input("\n⏸️ Press Enter to continue...")
    
    def create_commit(self) -> None:
        """Create a commit"""
        print("\n💾 Create Commit")
        print("=" * 20)
        
        # Check if there are staged changes
        exit_code, stdout, stderr = self._run_git_command(['diff', '--cached', '--name-only'])
        if not stdout.strip():
            print("❌ No staged changes. Please add files first.")
            input("\n⏸️ Press Enter to continue...")
            return
        
        print("📋 Staged changes:")
        print(stdout)
        
        # Get commit message
        message = self._get_user_input("Enter commit message")
        if not message:
            print("❌ Commit message cannot be empty")
            input("\n⏸️ Press Enter to continue...")
            return
        
        # Ask for additional options
        amend = self._confirm_action("Amend the last commit instead of creating new one?")
        
        # Create commit
        args = ['commit']
        if amend:
            args.append('--amend')
        
        args.extend(['-m', message])
        
        exit_code, stdout, stderr = self._run_git_command(args)
        if exit_code == 0:
            print(f"✅ Commit created: {message}")
        else:
            print(f"❌ Failed to create commit: {stderr}")
        
        input("\n⏸️ Press Enter to continue...")
    
    def push_changes(self) -> None:
        """Push changes to remote"""
        print("\n🚀 Push Changes")
        print("=" * 20)
        
        # Get current branch
        exit_code, stdout, stderr = self._run_git_command(['branch', '--show-current'])
        current_branch = stdout.strip()
        
        # Get remote
        remote = self._get_user_input("Enter remote name", "origin")
        
        # Ask for force push
        force = self._confirm_action("Force push? (Use with caution)")
        
        print(f"🚀 Pushing {current_branch} to {remote}...")
        
        args = ['push']
        if force:
            args.append('--force')
        
        args.extend([remote, current_branch])
        
        exit_code, stdout, stderr = self._run_git_command(args, capture_output=False)
        if exit_code == 0:
            print(f"✅ Successfully pushed to {remote}/{current_branch}")
        else:
            print(f"❌ Failed to push: {stderr}")
        
        input("\n⏸️ Press Enter to continue...")
    
    def pull_changes(self) -> None:
        """Pull changes from remote"""
        print("\n📥 Pull Changes")
        print("=" * 20)
        
        # Get current branch
        exit_code, stdout, stderr = self._run_git_command(['branch', '--show-current'])
        current_branch = stdout.strip()
        
        # Get remote
        remote = self._get_user_input("Enter remote name", "origin")
        
        print(f"📥 Pulling from {remote}/{current_branch}...")
        
        exit_code, stdout, stderr = self._run_git_command(['pull', remote, current_branch], capture_output=False)
        if exit_code == 0:
            print(f"✅ Successfully pulled from {remote}/{current_branch}")
        else:
            print(f"❌ Failed to pull: {stderr}")
        
        input("\n⏸️ Press Enter to continue...")
    
    def manage_branches(self) -> None:
        """Manage branches"""
        print("\n🌿 Branch Management")
        print("=" * 25)
        
        options = [
            "List all branches",
            "Create new branch",
            "Switch to branch",
            "Delete branch",
            "Back to main menu"
        ]
        
        choice = self._show_menu("Branch Management", options)
        
        if choice == 1:  # List branches
            print("\n🌿 Available branches:")
            print("=" * 30)
            exit_code, stdout, stderr = self._run_git_command(['branch', '-a'])
            print(stdout)
        
        elif choice == 2:  # Create branch
            branch_name = self._get_user_input("Enter new branch name")
            if branch_name:
                if self._confirm_action(f"Create and switch to branch '{branch_name}'?"):
                    exit_code, stdout, stderr = self._run_git_command(['checkout', '-b', branch_name])
                    if exit_code == 0:
                        print(f"✅ Created and switched to branch: {branch_name}")
                    else:
                        print(f"❌ Failed to create branch: {stderr}")
        
        elif choice == 3:  # Switch branch
            # Get available branches
            exit_code, stdout, stderr = self._run_git_command(['branch'])
            branches = [line.strip().replace('* ', '') for line in stdout.strip().split('\n')]
            
            print("\n🌿 Available branches:")
            for i, branch in enumerate(branches, 1):
                print(f"{i}. {branch}")
            
            try:
                branch_choice = int(input("👉 Select branch number: "))
                if 1 <= branch_choice <= len(branches):
                    branch_name = branches[branch_choice - 1]
                    exit_code, stdout, stderr = self._run_git_command(['checkout', branch_name])
                    if exit_code == 0:
                        print(f"✅ Switched to branch: {branch_name}")
                    else:
                        print(f"❌ Failed to switch branch: {stderr}")
                else:
                    print("❌ Invalid branch selection")
            except ValueError:
                print("❌ Please enter a valid number")
        
        elif choice == 4:  # Delete branch
            branch_name = self._get_user_input("Enter branch name to delete")
            if branch_name:
                if self._confirm_action(f"Delete branch '{branch_name}'?"):
                    exit_code, stdout, stderr = self._run_git_command(['branch', '-d', branch_name])
                    if exit_code == 0:
                        print(f"✅ Deleted branch: {branch_name}")
                    else:
                        print(f"❌ Failed to delete branch: {stderr}")
        
        input("\n⏸️ Press Enter to continue...")
    
    def view_history(self) -> None:
        """View commit history"""
        print("\n📜 Commit History")
        print("=" * 20)
        
        limit = self._get_user_input("Number of commits to show", "10")
        try:
            limit = int(limit)
        except ValueError:
            limit = 10
        
        print(f"\n📜 Recent commits (last {limit}):")
        print("=" * 50)
        exit_code, stdout, stderr = self._run_git_command(['log', '--oneline', '-n', str(limit)])
        if stdout.strip():
            print(stdout)
        else:
            print("No commits found")
        
        input("\n⏸️ Press Enter to continue...")
    
    def manage_stash(self) -> None:
        """Manage stashes"""
        print("\n💾 Stash Management")
        print("=" * 25)
        
        options = [
            "List stashes",
            "Save to stash",
            "Apply stash",
            "Back to main menu"
        ]
        
        choice = self._show_menu("Stash Management", options)
        
        if choice == 1:  # List stashes
            print("\n💾 Stash list:")
            print("=" * 20)
            exit_code, stdout, stderr = self._run_git_command(['stash', 'list'])
            if stdout.strip():
                print(stdout)
            else:
                print("No stashes found")
        
        elif choice == 2:  # Save to stash
            message = self._get_user_input("Enter stash message (optional)")
            args = ['stash', 'push']
            if message:
                args.extend(['-m', message])
            
            print("💾 Saving to stash...")
            exit_code, stdout, stderr = self._run_git_command(args)
            if exit_code == 0:
                print("✅ Changes stashed")
            else:
                print(f"❌ Failed to stash: {stderr}")
        
        elif choice == 3:  # Apply stash
            print("📤 Applying stash...")
            exit_code, stdout, stderr = self._run_git_command(['stash', 'pop'])
            if exit_code == 0:
                print("✅ Stash applied")
            else:
                print(f"❌ Failed to apply stash: {stderr}")
        
        input("\n⏸️ Press Enter to continue...")
    
    def quick_workflow(self) -> None:
        """Quick commit workflow"""
        print("\n⚡ Quick Commit Workflow")
        print("=" * 30)
        
        message = self._get_user_input("Enter commit message", f"Quick commit - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self._confirm_action("This will: Add all changes → Commit → Push. Continue?"):
            print("\n🔄 Executing quick workflow...")
            
            # Add all changes
            print("📁 Adding all changes...")
            exit_code, stdout, stderr = self._run_git_command(['add', '.'])
            if exit_code != 0:
                print(f"❌ Failed to add files: {stderr}")
                return
            
            # Commit
            print("💾 Creating commit...")
            exit_code, stdout, stderr = self._run_git_command(['commit', '-m', message])
            if exit_code != 0:
                print(f"❌ Failed to create commit: {stderr}")
                return
            
            # Push
            print("🚀 Pushing changes...")
            exit_code, stdout, stderr = self._run_git_command(['push'], capture_output=False)
            if exit_code == 0:
                print("✅ Quick workflow completed successfully!")
            else:
                print(f"❌ Failed to push: {stderr}")
        
        input("\n⏸️ Press Enter to continue...")
    
    def sync_workflow(self) -> None:
        """Sync workflow"""
        print("\n🔄 Sync Workflow")
        print("=" * 20)
        
        if self._confirm_action("This will: Pull → Add all → Commit → Push. Continue?"):
            print("\n🔄 Executing sync workflow...")
            
            # Pull latest changes
            print("📥 Pulling latest changes...")
            exit_code, stdout, stderr = self._run_git_command(['pull'], capture_output=False)
            if exit_code != 0:
                print(f"❌ Failed to pull: {stderr}")
                return
            
            # Check if there are changes to commit
            exit_code, stdout, stderr = self._run_git_command(['status', '--porcelain'])
            if stdout.strip():
                # Add all changes
                print("📁 Adding all changes...")
                exit_code, stdout, stderr = self._run_git_command(['add', '.'])
                if exit_code != 0:
                    print(f"❌ Failed to add files: {stderr}")
                    return
                
                # Commit
                message = f"Sync commit - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                print("💾 Creating commit...")
                exit_code, stdout, stderr = self._run_git_command(['commit', '-m', message])
                if exit_code != 0:
                    print(f"❌ Failed to create commit: {stderr}")
                    return
                
                # Push
                print("🚀 Pushing changes...")
                exit_code, stdout, stderr = self._run_git_command(['push'], capture_output=False)
                if exit_code == 0:
                    print("✅ Sync workflow completed successfully!")
                else:
                    print(f"❌ Failed to push: {stderr}")
            else:
                print("✅ No changes to sync")
        
        input("\n⏸️ Press Enter to continue...")
    
    def show_differences(self) -> None:
        """Show differences"""
        print("\n📋 Show Differences")
        print("=" * 25)
        
        options = [
            "Show unstaged changes",
            "Show staged changes",
            "Show all changes",
            "Back to main menu"
        ]
        
        choice = self._show_menu("Show Differences", options)
        
        if choice == 1:  # Unstaged changes
            print("\n📋 Unstaged changes:")
            print("=" * 30)
            exit_code, stdout, stderr = self._run_git_command(['diff'])
            if stdout.strip():
                print(stdout)
            else:
                print("No unstaged changes")
        
        elif choice == 2:  # Staged changes
            print("\n📋 Staged changes:")
            print("=" * 30)
            exit_code, stdout, stderr = self._run_git_command(['diff', '--cached'])
            if stdout.strip():
                print(stdout)
            else:
                print("No staged changes")
        
        elif choice == 3:  # All changes
            print("\n📋 All changes:")
            print("=" * 30)
            exit_code, stdout, stderr = self._run_git_command(['diff', 'HEAD'])
            if stdout.strip():
                print(stdout)
            else:
                print("No changes")
        
        input("\n⏸️ Press Enter to continue...")
    
    def main_menu(self) -> None:
        """Main menu loop"""
        while True:
            print(f"\n{'='*60}")
            print("🔧 Git Helper Dialogue - Interactive Git Operations")
            print(f"{'='*60}")
            print(f"📁 Repository: {os.path.basename(self.repo_path)}")
            
            # Show current branch
            exit_code, stdout, stderr = self._run_git_command(['branch', '--show-current'])
            current_branch = stdout.strip()
            print(f"🌿 Current branch: {current_branch}")
            
            options = [
                "📊 Show Status",
                "📁 Add Files",
                "💾 Create Commit",
                "🚀 Push Changes",
                "📥 Pull Changes",
                "🌿 Manage Branches",
                "📜 View History",
                "💾 Manage Stash",
                "📋 Show Differences",
                "⚡ Quick Workflow",
                "🔄 Sync Workflow",
                "❌ Exit"
            ]
            
            choice = self._show_menu("Main Menu", options)
            
            if choice == 1:
                self.show_status()
            elif choice == 2:
                self.add_files()
            elif choice == 3:
                self.create_commit()
            elif choice == 4:
                self.push_changes()
            elif choice == 5:
                self.pull_changes()
            elif choice == 6:
                self.manage_branches()
            elif choice == 7:
                self.view_history()
            elif choice == 8:
                self.manage_stash()
            elif choice == 9:
                self.show_differences()
            elif choice == 10:
                self.quick_workflow()
            elif choice == 11:
                self.sync_workflow()
            elif choice == 12:
                print("\n👋 Goodbye!")
                break

def main():
    try:
        git_helper = GitHelperDialogue()
        git_helper.main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
