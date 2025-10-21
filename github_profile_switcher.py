#!/usr/bin/env python3
"""
GitHub Profile Switcher - Multi-account management tool
Allows switching between multiple GitHub accounts with separate configurations
Version: 1.0.0
"""

import os
import sys
import json
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, List, Optional
import shutil
from pathlib import Path
import webbrowser

class GitHubProfileSwitcher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GitHub Profile Switcher")
        self.root.geometry("800x600")
        
        # Configuration paths
        self.config_dir = Path.home() / ".github-profiles"
        self.config_file = self.config_dir / "profiles.json"
        self.current_profile_file = self.config_dir / "current_profile.json"
        
        # Git configuration paths
        self.git_config_dir = Path.home() / ".gitconfig"
        self.git_ssh_dir = Path.home() / ".ssh"
        
        # Initialize configuration
        self.profiles = {}
        self.current_profile = None
        self.load_configuration()
        
        # Create GUI
        self.create_gui()
        
    def load_configuration(self):
        """Load profiles and current profile from configuration files"""
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(exist_ok=True)
        
        # Load profiles
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.profiles = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.profiles = {}
        else:
            self.profiles = {}
        
        # Load current profile
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
        # Save profiles
        with open(self.config_file, 'w') as f:
            json.dump(self.profiles, f, indent=2)
        
        # Save current profile
        with open(self.current_profile_file, 'w') as f:
            json.dump({'current_profile': self.current_profile}, f, indent=2)
    
    def create_gui(self):
        """Create the main GUI interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="GitHub Profile Switcher", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Current profile section
        current_frame = ttk.LabelFrame(main_frame, text="Current Profile", padding="10")
        current_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        current_frame.columnconfigure(1, weight=1)
        
        ttk.Label(current_frame, text="Active Profile:").grid(row=0, column=0, sticky=tk.W)
        self.current_profile_var = tk.StringVar()
        self.current_profile_label = ttk.Label(current_frame, textvariable=self.current_profile_var,
                                             font=('Arial', 10, 'bold'), foreground='blue')
        self.current_profile_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Profile management section
        profile_frame = ttk.LabelFrame(main_frame, text="Profile Management", padding="10")
        profile_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        profile_frame.columnconfigure(1, weight=1)
        
        # Profile list
        ttk.Label(profile_frame, text="Profiles:").grid(row=0, column=0, sticky=tk.W)
        
        # Create treeview for profiles
        tree_frame = ttk.Frame(profile_frame)
        tree_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        tree_frame.columnconfigure(0, weight=1)
        
        self.profile_tree = ttk.Treeview(tree_frame, columns=('username', 'email', 'status'), 
                                       show='tree headings', height=8)
        self.profile_tree.heading('#0', text='Profile Name')
        self.profile_tree.heading('username', text='GitHub Username')
        self.profile_tree.heading('email', text='Email')
        self.profile_tree.heading('status', text='Status')
        
        self.profile_tree.column('#0', width=150)
        self.profile_tree.column('username', width=150)
        self.profile_tree.column('email', width=200)
        self.profile_tree.column('status', width=100)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.profile_tree.yview)
        self.profile_tree.configure(yscrollcommand=scrollbar.set)
        
        self.profile_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Buttons frame
        buttons_frame = ttk.Frame(profile_frame)
        buttons_frame.grid(row=2, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(buttons_frame, text="Add Profile", command=self.add_profile).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Edit Profile", command=self.edit_profile).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Delete Profile", command=self.delete_profile).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Switch To", command=self.switch_to_profile).pack(side=tk.LEFT, padx=(0, 5))
        
        # Quick actions section
        actions_frame = ttk.LabelFrame(main_frame, text="Quick Actions", padding="10")
        actions_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(actions_frame, text="Open GitHub", command=self.open_github).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(actions_frame, text="Test SSH Connection", command=self.test_ssh).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(actions_frame, text="Refresh Profiles", command=self.refresh_profiles).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(actions_frame, text="Export Config", command=self.export_config).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(actions_frame, text="Import Config", command=self.import_config).pack(side=tk.LEFT, padx=(0, 5))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Bind events
        self.profile_tree.bind('<Double-1>', lambda e: self.switch_to_profile())
        
        # Initial load
        self.refresh_profiles()
        self.update_current_profile_display()
    
    def refresh_profiles(self):
        """Refresh the profile list display"""
        # Clear existing items
        for item in self.profile_tree.get_children():
            self.profile_tree.delete(item)
        
        # Add profiles
        for profile_name, profile_data in self.profiles.items():
            status = "Active" if profile_name == self.current_profile else "Inactive"
            self.profile_tree.insert('', 'end', text=profile_name,
                                   values=(profile_data.get('username', ''),
                                          profile_data.get('email', ''),
                                          status))
    
    def update_current_profile_display(self):
        """Update the current profile display"""
        if self.current_profile and self.current_profile in self.profiles:
            profile_data = self.profiles[self.current_profile]
            display_text = f"{self.current_profile} ({profile_data.get('username', 'Unknown')})"
        else:
            display_text = "No active profile"
        
        self.current_profile_var.set(display_text)
        self.refresh_profiles()
    
    def add_profile(self):
        """Add a new profile"""
        dialog = ProfileDialog(self.root, "Add Profile")
        if dialog.result:
            profile_name = dialog.result['name']
            if profile_name in self.profiles:
                messagebox.showerror("Error", f"Profile '{profile_name}' already exists!")
                return
            
            self.profiles[profile_name] = dialog.result
            self.save_configuration()
            self.refresh_profiles()
            self.status_var.set(f"Added profile: {profile_name}")
    
    def edit_profile(self):
        """Edit an existing profile"""
        selection = self.profile_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to edit")
            return
        
        profile_name = self.profile_tree.item(selection[0])['text']
        profile_data = self.profiles[profile_name]
        
        dialog = ProfileDialog(self.root, "Edit Profile", profile_data)
        if dialog.result:
            self.profiles[profile_name] = dialog.result
            self.save_configuration()
            self.refresh_profiles()
            self.update_current_profile_display()
            self.status_var.set(f"Updated profile: {profile_name}")
    
    def delete_profile(self):
        """Delete a profile"""
        selection = self.profile_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to delete")
            return
        
        profile_name = self.profile_tree.item(selection[0])['text']
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete profile '{profile_name}'?"):
            del self.profiles[profile_name]
            
            # If this was the current profile, clear it
            if self.current_profile == profile_name:
                self.current_profile = None
                self.save_configuration()
                self.update_current_profile_display()
            
            self.save_configuration()
            self.refresh_profiles()
            self.status_var.set(f"Deleted profile: {profile_name}")
    
    def switch_to_profile(self):
        """Switch to the selected profile"""
        selection = self.profile_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to switch to")
            return
        
        profile_name = self.profile_tree.item(selection[0])['text']
        profile_data = self.profiles[profile_name]
        
        try:
            # Update Git configuration
            self.update_git_config(profile_data)
            
            # Update SSH configuration if needed
            if profile_data.get('ssh_key'):
                self.update_ssh_config(profile_data)
            
            # Set current profile
            self.current_profile = profile_name
            self.save_configuration()
            self.update_current_profile_display()
            
            self.status_var.set(f"Switched to profile: {profile_name}")
            messagebox.showinfo("Success", f"Successfully switched to profile: {profile_name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to switch profile: {str(e)}")
            self.status_var.set(f"Error switching to profile: {profile_name}")
    
    def update_git_config(self, profile_data):
        """Update Git configuration for the profile"""
        username = profile_data.get('username', '')
        email = profile_data.get('email', '')
        
        if username:
            subprocess.run(['git', 'config', '--global', 'user.name', username], check=True)
        
        if email:
            subprocess.run(['git', 'config', '--global', 'user.email', email], check=True)
        
        # Set other Git configurations
        if profile_data.get('default_branch'):
            subprocess.run(['git', 'config', '--global', 'init.defaultBranch', 
                          profile_data['default_branch']], check=True)
    
    def update_ssh_config(self, profile_data):
        """Update SSH configuration for the profile"""
        ssh_key = profile_data.get('ssh_key', '')
        if ssh_key and Path(ssh_key).exists():
            # Add SSH key to SSH agent
            try:
                subprocess.run(['ssh-add', ssh_key], check=True)
            except subprocess.CalledProcessError:
                pass  # SSH agent might not be running
    
    def open_github(self):
        """Open GitHub in browser"""
        if self.current_profile and self.current_profile in self.profiles:
            username = self.profiles[self.current_profile].get('username', '')
            if username:
                webbrowser.open(f"https://github.com/{username}")
            else:
                webbrowser.open("https://github.com")
        else:
            webbrowser.open("https://github.com")
    
    def test_ssh(self):
        """Test SSH connection to GitHub"""
        try:
            result = subprocess.run(['ssh', '-T', 'git@github.com'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0 or "successfully authenticated" in result.stderr:
                messagebox.showinfo("SSH Test", "SSH connection to GitHub successful!")
            else:
                messagebox.showwarning("SSH Test", f"SSH connection failed:\n{result.stderr}")
        except subprocess.TimeoutExpired:
            messagebox.showerror("SSH Test", "SSH connection timed out")
        except Exception as e:
            messagebox.showerror("SSH Test", f"SSH test failed: {str(e)}")
    
    def export_config(self):
        """Export configuration to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump({
                        'profiles': self.profiles,
                        'current_profile': self.current_profile
                    }, f, indent=2)
                messagebox.showinfo("Export", f"Configuration exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
    
    def import_config(self):
        """Import configuration from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                
                if 'profiles' in data:
                    self.profiles = data['profiles']
                    self.current_profile = data.get('current_profile')
                    self.save_configuration()
                    self.refresh_profiles()
                    self.update_current_profile_display()
                    messagebox.showinfo("Import", f"Configuration imported from {filename}")
                else:
                    messagebox.showerror("Import Error", "Invalid configuration file format")
            except Exception as e:
                messagebox.showerror("Import Error", f"Failed to import: {str(e)}")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

class ProfileDialog:
    def __init__(self, parent, title, profile_data=None):
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Create form
        self.create_form(profile_data)
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def create_form(self, profile_data):
        """Create the profile form"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Profile name
        ttk.Label(main_frame, text="Profile Name:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.name_var = tk.StringVar(value=profile_data.get('name', '') if profile_data else '')
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=40)
        name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # GitHub username
        ttk.Label(main_frame, text="GitHub Username:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.username_var = tk.StringVar(value=profile_data.get('username', '') if profile_data else '')
        username_entry = ttk.Entry(main_frame, textvariable=self.username_var, width=40)
        username_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Email
        ttk.Label(main_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.email_var = tk.StringVar(value=profile_data.get('email', '') if profile_data else '')
        email_entry = ttk.Entry(main_frame, textvariable=self.email_var, width=40)
        email_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Default branch
        ttk.Label(main_frame, text="Default Branch:").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        self.branch_var = tk.StringVar(value=profile_data.get('default_branch', 'main') if profile_data else 'main')
        branch_entry = ttk.Entry(main_frame, textvariable=self.branch_var, width=40)
        branch_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # SSH Key path
        ttk.Label(main_frame, text="SSH Key Path:").grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        ssh_frame = ttk.Frame(main_frame)
        ssh_frame.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        ssh_frame.columnconfigure(0, weight=1)
        
        self.ssh_var = tk.StringVar(value=profile_data.get('ssh_key', '') if profile_data else '')
        ssh_entry = ttk.Entry(ssh_frame, textvariable=self.ssh_var)
        ssh_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(ssh_frame, text="Browse", command=self.browse_ssh_key).grid(row=0, column=1)
        
        # Additional settings
        settings_frame = ttk.LabelFrame(main_frame, text="Additional Settings", padding="10")
        settings_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.auto_push_var = tk.BooleanVar(value=profile_data.get('auto_push', False) if profile_data else False)
        ttk.Checkbutton(settings_frame, text="Auto-push after commit", 
                       variable=self.auto_push_var).pack(anchor=tk.W)
        
        self.sign_commits_var = tk.BooleanVar(value=profile_data.get('sign_commits', False) if profile_data else False)
        ttk.Checkbutton(settings_frame, text="Sign commits", 
                       variable=self.sign_commits_var).pack(anchor=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="Save", command=self.save_profile).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
    
    def browse_ssh_key(self):
        """Browse for SSH key file"""
        filename = filedialog.askopenfilename(
            title="Select SSH Key",
            filetypes=[("All files", "*.*"), ("SSH keys", "*.pem")]
        )
        if filename:
            self.ssh_var.set(filename)
    
    def save_profile(self):
        """Save the profile"""
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Profile name is required")
            return
        
        self.result = {
            'name': name,
            'username': self.username_var.get().strip(),
            'email': self.email_var.get().strip(),
            'default_branch': self.branch_var.get().strip() or 'main',
            'ssh_key': self.ssh_var.get().strip(),
            'auto_push': self.auto_push_var.get(),
            'sign_commits': self.sign_commits_var.get()
        }
        
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel the dialog"""
        self.dialog.destroy()

def main():
    """Main function"""
    try:
        app = GitHubProfileSwitcher()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
