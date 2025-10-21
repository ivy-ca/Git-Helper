#!/usr/bin/env python3
"""
Git Helper - A comprehensive Git operations tool
Provides easy-to-use commands for common Git operations
"""

import subprocess
import sys
import os
import argparse
from typing import List, Optional, Tuple
import json
from datetime import datetime

class GitHelper:
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
            print("Error: Git is not installed or not in PATH")
            sys.exit(1)
    
    def status(self) -> None:
        """Show repository status"""
        print("📊 Repository Status:")
        print("=" * 50)
        exit_code, stdout, stderr = self._run_git_command(['status', '--porcelain'])
        if stdout.strip():
            print(stdout)
        else:
            print("✅ Working directory clean")
        
        # Show branch info
        exit_code, stdout, stderr = self._run_git_command(['branch', '--show-current'])
        current_branch = stdout.strip()
        print(f"\n🌿 Current branch: {current_branch}")
        
        # Show last commit
        exit_code, stdout, stderr = self._run_git_command(['log', '-1', '--oneline'])
        if stdout.strip():
            print(f"📝 Last commit: {stdout.strip()}")
    
    def add(self, files: List[str] = None) -> None:
        """Add files to staging area"""
        if files is None:
            files = ['.']
        
        for file in files:
            if file == '.':
                print("📁 Adding all changes...")
            else:
                print(f"📄 Adding {file}...")
            
            exit_code, stdout, stderr = self._run_git_command(['add', file])
            if exit_code == 0:
                print(f"✅ Added {file}")
            else:
                print(f"❌ Failed to add {file}: {stderr}")
    
    def commit(self, message: str, amend: bool = False) -> None:
        """Create a commit"""
        args = ['commit']
        if amend:
            args.append('--amend')
            print("🔄 Amending last commit...")
        else:
            print("💾 Creating commit...")
        
        args.extend(['-m', message])
        
        exit_code, stdout, stderr = self._run_git_command(args)
        if exit_code == 0:
            print(f"✅ Commit created: {message}")
        else:
            print(f"❌ Failed to create commit: {stderr}")
    
    def push(self, remote: str = 'origin', branch: str = None, force: bool = False) -> None:
        """Push changes to remote repository"""
        if branch is None:
            exit_code, stdout, stderr = self._run_git_command(['branch', '--show-current'])
            branch = stdout.strip()
        
        args = ['push']
        if force:
            args.append('--force')
            print(f"🚀 Force pushing to {remote}/{branch}...")
        else:
            print(f"🚀 Pushing to {remote}/{branch}...")
        
        args.extend([remote, branch])
        
        exit_code, stdout, stderr = self._run_git_command(args, capture_output=False)
        if exit_code == 0:
            print(f"✅ Successfully pushed to {remote}/{branch}")
        else:
            print(f"❌ Failed to push: {stderr}")
    
    def pull(self, remote: str = 'origin', branch: str = None) -> None:
        """Pull changes from remote repository"""
        if branch is None:
            exit_code, stdout, stderr = self._run_git_command(['branch', '--show-current'])
            branch = stdout.strip()
        
        print(f"📥 Pulling from {remote}/{branch}...")
        
        exit_code, stdout, stderr = self._run_git_command(['pull', remote, branch], capture_output=False)
        if exit_code == 0:
            print(f"✅ Successfully pulled from {remote}/{branch}")
        else:
            print(f"❌ Failed to pull: {stderr}")
    
    def branch(self, name: str = None, create: bool = False, delete: bool = False, list_all: bool = False) -> None:
        """Manage branches"""
        if list_all:
            print("🌿 Available branches:")
            print("=" * 30)
            exit_code, stdout, stderr = self._run_git_command(['branch', '-a'])
            print(stdout)
            return
        
        if delete and name:
            print(f"🗑️ Deleting branch: {name}")
            exit_code, stdout, stderr = self._run_git_command(['branch', '-d', name])
            if exit_code == 0:
                print(f"✅ Deleted branch: {name}")
            else:
                print(f"❌ Failed to delete branch: {stderr}")
            return
        
        if create and name:
            print(f"🌱 Creating branch: {name}")
            exit_code, stdout, stderr = self._run_git_command(['checkout', '-b', name])
            if exit_code == 0:
                print(f"✅ Created and switched to branch: {name}")
            else:
                print(f"❌ Failed to create branch: {stderr}")
            return
        
        if name:
            print(f"🔄 Switching to branch: {name}")
            exit_code, stdout, stderr = self._run_git_command(['checkout', name])
            if exit_code == 0:
                print(f"✅ Switched to branch: {name}")
            else:
                print(f"❌ Failed to switch branch: {stderr}")
    
    def log(self, limit: int = 10, oneline: bool = True) -> None:
        """Show commit history"""
        args = ['log']
        if oneline:
            args.append('--oneline')
        args.extend(['-n', str(limit)])
        
        print(f"📜 Recent commits (last {limit}):")
        print("=" * 50)
        exit_code, stdout, stderr = self._run_git_command(args)
        if stdout.strip():
            print(stdout)
        else:
            print("No commits found")
    
    def diff(self, staged: bool = False) -> None:
        """Show differences"""
        args = ['diff']
        if staged:
            args.append('--cached')
            print("📋 Staged changes:")
        else:
            print("📋 Unstaged changes:")
        
        print("=" * 30)
        exit_code, stdout, stderr = self._run_git_command(args)
        if stdout.strip():
            print(stdout)
        else:
            print("No changes to show")
    
    def stash(self, action: str = 'list', message: str = None) -> None:
        """Manage stashes"""
        if action == 'list':
            print("💾 Stash list:")
            print("=" * 20)
            exit_code, stdout, stderr = self._run_git_command(['stash', 'list'])
            if stdout.strip():
                print(stdout)
            else:
                print("No stashes found")
        
        elif action == 'save':
            args = ['stash', 'push']
            if message:
                args.extend(['-m', message])
            print("💾 Saving to stash...")
            exit_code, stdout, stderr = self._run_git_command(args)
            if exit_code == 0:
                print("✅ Changes stashed")
            else:
                print(f"❌ Failed to stash: {stderr}")
        
        elif action == 'pop':
            print("📤 Applying stash...")
            exit_code, stdout, stderr = self._run_git_command(['stash', 'pop'])
            if exit_code == 0:
                print("✅ Stash applied")
            else:
                print(f"❌ Failed to apply stash: {stderr}")
    
    def reset(self, mode: str = 'soft', commit: str = 'HEAD~1') -> None:
        """Reset repository state"""
        print(f"🔄 Resetting {mode} to {commit}...")
        exit_code, stdout, stderr = self._run_git_command(['reset', f'--{mode}', commit])
        if exit_code == 0:
            print(f"✅ Reset {mode} successful")
        else:
            print(f"❌ Failed to reset: {stderr}")
    
    def remote(self, action: str = 'list') -> None:
        """Manage remotes"""
        if action == 'list':
            print("🌐 Remote repositories:")
            print("=" * 30)
            exit_code, stdout, stderr = self._run_git_command(['remote', '-v'])
            print(stdout)
        
        elif action == 'add' and len(sys.argv) > 3:
            name = sys.argv[3]
            url = sys.argv[4] if len(sys.argv) > 4 else None
            if url:
                print(f"➕ Adding remote: {name} -> {url}")
                exit_code, stdout, stderr = self._run_git_command(['remote', 'add', name, url])
                if exit_code == 0:
                    print(f"✅ Added remote: {name}")
                else:
                    print(f"❌ Failed to add remote: {stderr}")
    
    def quick_commit(self, message: str = None) -> None:
        """Quick commit workflow: add all, commit, push"""
        if not message:
            message = f"Quick commit - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        print("⚡ Quick commit workflow:")
        print("=" * 30)
        
        # Add all changes
        self.add(['.'])
        
        # Commit
        self.commit(message)
        
        # Push
        self.push()
    
    def sync(self) -> None:
        """Sync with remote: pull, add all, commit, push"""
        print("🔄 Syncing with remote:")
        print("=" * 25)
        
        # Pull latest changes
        self.pull()
        
        # Check if there are changes to commit
        exit_code, stdout, stderr = self._run_git_command(['status', '--porcelain'])
        if stdout.strip():
            # Add all changes
            self.add(['.'])
            
            # Commit
            message = f"Sync commit - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            self.commit(message)
            
            # Push
            self.push()
        else:
            print("✅ No changes to sync")

def main():
    parser = argparse.ArgumentParser(description='Git Helper - Easy Git operations')
    parser.add_argument('command', help='Git command to execute')
    parser.add_argument('args', nargs='*', help='Command arguments')
    
    args = parser.parse_args()
    
    git_helper = GitHelper()
    command = args.command.lower()
    
    try:
        if command == 'status':
            git_helper.status()
        
        elif command == 'add':
            files = args.args if args.args else ['.']
            git_helper.add(files)
        
        elif command == 'commit':
            if not args.args:
                print("❌ Please provide a commit message")
                sys.exit(1)
            message = ' '.join(args.args)
            git_helper.commit(message)
        
        elif command == 'push':
            remote = args.args[0] if len(args.args) > 0 else 'origin'
            branch = args.args[1] if len(args.args) > 1 else None
            git_helper.push(remote, branch)
        
        elif command == 'pull':
            remote = args.args[0] if len(args.args) > 0 else 'origin'
            branch = args.args[1] if len(args.args) > 1 else None
            git_helper.pull(remote, branch)
        
        elif command == 'branch':
            if not args.args:
                git_helper.branch(list_all=True)
            elif args.args[0] == 'create' and len(args.args) > 1:
                git_helper.branch(args.args[1], create=True)
            elif args.args[0] == 'delete' and len(args.args) > 1:
                git_helper.branch(args.args[1], delete=True)
            else:
                git_helper.branch(args.args[0])
        
        elif command == 'log':
            limit = int(args.args[0]) if args.args else 10
            git_helper.log(limit)
        
        elif command == 'diff':
            staged = '--staged' in args.args or '--cached' in args.args
            git_helper.diff(staged)
        
        elif command == 'stash':
            action = args.args[0] if args.args else 'list'
            message = args.args[1] if len(args.args) > 1 else None
            git_helper.stash(action, message)
        
        elif command == 'reset':
            mode = args.args[0] if args.args else 'soft'
            commit = args.args[1] if len(args.args) > 1 else 'HEAD~1'
            git_helper.reset(mode, commit)
        
        elif command == 'remote':
            action = args.args[0] if args.args else 'list'
            git_helper.remote(action)
        
        elif command == 'quick':
            message = ' '.join(args.args) if args.args else None
            git_helper.quick_commit(message)
        
        elif command == 'sync':
            git_helper.sync()
        
        else:
            print(f"❌ Unknown command: {command}")
            print("\nAvailable commands:")
            print("  status          - Show repository status")
            print("  add [files]     - Add files to staging")
            print("  commit <msg>    - Create a commit")
            print("  push [remote] [branch] - Push to remote")
            print("  pull [remote] [branch] - Pull from remote")
            print("  branch [name]  - Switch to branch")
            print("  branch create <name> - Create new branch")
            print("  branch delete <name> - Delete branch")
            print("  log [limit]     - Show commit history")
            print("  diff [--staged] - Show differences")
            print("  stash [save|pop|list] - Manage stashes")
            print("  reset [mode] [commit] - Reset repository")
            print("  remote [list|add] - Manage remotes")
            print("  quick [msg]     - Quick commit workflow")
            print("  sync            - Sync with remote")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

