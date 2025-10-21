#!/usr/bin/env python3
"""
GitHub Profile Switcher CLI - Command-line interface for profile management
Version: 1.0.0
"""

import argparse
import json
import subprocess
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional

class GitHubProfileSwitcherCLI:
    def __init__(self):
        self.config_dir = Path.home() / ".github-profiles"
        self.config_file = self.config_dir / "profiles.json"
        self.current_profile_file = self.config_dir / "current_profile.json"
        
        # Initialize configuration
        self.profiles = {}
        self.current_profile = None
        self.load_configuration()
    
    def load_configuration(self):
        """Load profiles and current profile from configuration files"""
        self.config_dir.mkdir(exist_ok=True)
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.profiles = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.profiles = {}
        else:
            self.profiles = {}
        
        if self.current_profile_file.exists():
            try:
                with open(self.current_profile_file, 'r') as f:
                    current_data = json.load(f)
                    self.current_profile = current_data.get('current_profile')
            except (json.JSONDecodeError, FileNotFoundError):
                self.current_profile = None
        else:
            self.current_profile = None
    
    def save_configuration(self):
        """Save profiles and current profile to configuration files"""
        with open(self.config_file, 'w') as f:
            json.dump(self.profiles, f, indent=2)
        
        with open(self.current_profile_file, 'w') as f:
            json.dump({'current_profile': self.current_profile}, f, indent=2)
    
    def list_profiles(self):
        """List all profiles"""
        if not self.profiles:
            print("No profiles configured.")
            return
        
        print("Available profiles:")
        print("=" * 50)
        for name, data in self.profiles.items():
            status = "✓ Active" if name == self.current_profile else "  Inactive"
            print(f"{status} {name}")
            print(f"    Username: {data.get('username', 'Not set')}")
            print(f"    Email: {data.get('email', 'Not set')}")
            print(f"    Branch: {data.get('default_branch', 'main')}")
            if data.get('ssh_key'):
                print(f"    SSH Key: {data['ssh_key']}")
            print()
    
    def add_profile(self, name: str, username: str = "", email: str = "", 
                   branch: str = "main", ssh_key: str = ""):
        """Add a new profile"""
        if name in self.profiles:
            print(f"Error: Profile '{name}' already exists!")
            return False
        
        self.profiles[name] = {
            'name': name,
            'username': username,
            'email': email,
            'default_branch': branch,
            'ssh_key': ssh_key,
            'auto_push': False,
            'sign_commits': False
        }
        
        self.save_configuration()
        print(f"✓ Added profile: {name}")
        return True
    
    def remove_profile(self, name: str):
        """Remove a profile"""
        if name not in self.profiles:
            print(f"Error: Profile '{name}' does not exist!")
            return False
        
        del self.profiles[name]
        
        if self.current_profile == name:
            self.current_profile = None
            self.save_configuration()
            print(f"✓ Removed profile '{name}' and cleared current profile")
        else:
            self.save_configuration()
            print(f"✓ Removed profile: {name}")
        
        return True
    
    def switch_profile(self, name: str):
        """Switch to a profile"""
        if name not in self.profiles:
            print(f"Error: Profile '{name}' does not exist!")
            return False
        
        profile_data = self.profiles[name]
        
        try:
            # Update Git configuration
            self.update_git_config(profile_data)
            
            # Update SSH configuration if needed
            if profile_data.get('ssh_key'):
                self.update_ssh_config(profile_data)
            
            # Set current profile
            self.current_profile = name
            self.save_configuration()
            
            print(f"✓ Switched to profile: {name}")
            print(f"  Username: {profile_data.get('username', 'Not set')}")
            print(f"  Email: {profile_data.get('email', 'Not set')}")
            return True
            
        except Exception as e:
            print(f"Error switching to profile '{name}': {e}")
            return False
    
    def update_git_config(self, profile_data):
        """Update Git configuration for the profile"""
        username = profile_data.get('username', '')
        email = profile_data.get('email', '')
        
        if username:
            subprocess.run(['git', 'config', '--global', 'user.name', username], check=True)
        
        if email:
            subprocess.run(['git', 'config', '--global', 'user.email', email], check=True)
        
        if profile_data.get('default_branch'):
            subprocess.run(['git', 'config', '--global', 'init.defaultBranch', 
                          profile_data['default_branch']], check=True)
    
    def update_ssh_config(self, profile_data):
        """Update SSH configuration for the profile"""
        ssh_key = profile_data.get('ssh_key', '')
        if ssh_key and Path(ssh_key).exists():
            try:
                subprocess.run(['ssh-add', ssh_key], check=True)
            except subprocess.CalledProcessError:
                pass  # SSH agent might not be running
    
    def get_current_profile(self):
        """Get current profile information"""
        if self.current_profile and self.current_profile in self.profiles:
            profile_data = self.profiles[self.current_profile]
            print(f"Current profile: {self.current_profile}")
            print(f"Username: {profile_data.get('username', 'Not set')}")
            print(f"Email: {profile_data.get('email', 'Not set')}")
            print(f"Branch: {profile_data.get('default_branch', 'main')}")
        else:
            print("No active profile")
    
    def test_ssh(self):
        """Test SSH connection to GitHub"""
        try:
            result = subprocess.run(['ssh', '-T', 'git@github.com'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0 or "successfully authenticated" in result.stderr:
                print("✓ SSH connection to GitHub successful!")
            else:
                print(f"✗ SSH connection failed: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("✗ SSH connection timed out")
        except Exception as e:
            print(f"✗ SSH test failed: {e}")
    
    def export_config(self, filename: str):
        """Export configuration to file"""
        try:
            with open(filename, 'w') as f:
                json.dump({
                    'profiles': self.profiles,
                    'current_profile': self.current_profile
                }, f, indent=2)
            print(f"✓ Configuration exported to {filename}")
        except Exception as e:
            print(f"✗ Failed to export: {e}")
    
    def import_config(self, filename: str):
        """Import configuration from file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            if 'profiles' in data:
                self.profiles = data['profiles']
                self.current_profile = data.get('current_profile')
                self.save_configuration()
                print(f"✓ Configuration imported from {filename}")
            else:
                print("✗ Invalid configuration file format")
        except Exception as e:
            print(f"✗ Failed to import: {e}")
    
    def create_vscode_settings(self):
        """Create VS Code settings for profile switching"""
        vscode_settings = {
            "github-profile-switcher.profiles": self.profiles,
            "github-profile-switcher.currentProfile": self.current_profile
        }
        
        settings_file = self.config_dir / "vscode_settings.json"
        with open(settings_file, 'w') as f:
            json.dump(vscode_settings, f, indent=2)
        
        print(f"✓ VS Code settings created: {settings_file}")
        print("Add this to your VS Code settings.json:")
        print(f'  "github-profile-switcher.configPath": "{settings_file}"')

def main():
    parser = argparse.ArgumentParser(description='GitHub Profile Switcher CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List profiles
    subparsers.add_parser('list', help='List all profiles')
    
    # Add profile
    add_parser = subparsers.add_parser('add', help='Add a new profile')
    add_parser.add_argument('name', help='Profile name')
    add_parser.add_argument('--username', help='GitHub username')
    add_parser.add_argument('--email', help='Email address')
    add_parser.add_argument('--branch', default='main', help='Default branch')
    add_parser.add_argument('--ssh-key', help='SSH key path')
    
    # Remove profile
    remove_parser = subparsers.add_parser('remove', help='Remove a profile')
    remove_parser.add_argument('name', help='Profile name')
    
    # Switch profile
    switch_parser = subparsers.add_parser('switch', help='Switch to a profile')
    switch_parser.add_argument('name', help='Profile name')
    
    # Current profile
    subparsers.add_parser('current', help='Show current profile')
    
    # Test SSH
    subparsers.add_parser('test-ssh', help='Test SSH connection')
    
    # Export/Import
    export_parser = subparsers.add_parser('export', help='Export configuration')
    export_parser.add_argument('filename', help='Export filename')
    
    import_parser = subparsers.add_parser('import', help='Import configuration')
    import_parser.add_argument('filename', help='Import filename')
    
    # VS Code integration
    subparsers.add_parser('vscode', help='Create VS Code settings')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    switcher = GitHubProfileSwitcherCLI()
    
    if args.command == 'list':
        switcher.list_profiles()
    elif args.command == 'add':
        switcher.add_profile(args.name, args.username, args.email, args.branch, args.ssh_key)
    elif args.command == 'remove':
        switcher.remove_profile(args.name)
    elif args.command == 'switch':
        switcher.switch_profile(args.name)
    elif args.command == 'current':
        switcher.get_current_profile()
    elif args.command == 'test-ssh':
        switcher.test_ssh()
    elif args.command == 'export':
        switcher.export_config(args.filename)
    elif args.command == 'import':
        switcher.import_config(args.filename)
    elif args.command == 'vscode':
        switcher.create_vscode_settings()

if __name__ == '__main__':
    main()
