# GitHub Profile Switcher

A comprehensive tool for managing multiple GitHub accounts with separate configurations, similar to VS Code or Chrome profile switching.

## 🚀 Features

- **Easy Profile Switching**: Switch between multiple GitHub accounts with a single click
- **Separate Configurations**: Each profile maintains its own Git settings, SSH keys, and preferences
- **Multiple Interfaces**: GUI, CLI, and VS Code extension support
- **Quick Access**: Command palette and status bar integration
- **SSH Key Management**: Automatic SSH key switching for each profile
- **Configuration Export/Import**: Backup and share your profile configurations
- **VS Code Integration**: Native VS Code extension with status bar display

## 📦 Installation

### GUI Application
```bash
# Download and run the GUI version
python github_profile_switcher.py
```

### CLI Tool
```bash
# Use the command-line interface
python github_profile_switcher_cli.py --help
```

### VS Code Extension
1. Copy the `vscode-extension` folder to your VS Code extensions directory
2. Reload VS Code
3. The extension will appear in your command palette

## 🎯 Quick Start

### 1. GUI Version
```bash
python github_profile_switcher.py
```

1. Click "Add Profile" to create your first profile
2. Fill in your GitHub username, email, and SSH key path
3. Click "Switch To" to activate the profile
4. Your Git configuration will be updated automatically

### 2. CLI Version
```bash
# Add a profile
python github_profile_switcher_cli.py add work --username work-account --email work@company.com

# List profiles
python github_profile_switcher_cli.py list

# Switch to a profile
python github_profile_switcher_cli.py switch work

# Show current profile
python github_profile_switcher_cli.py current
```

### 3. VS Code Extension
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type "GitHub Profile" to see available commands
3. Select "Switch GitHub Profile" to change profiles
4. Current profile is shown in the status bar

## 📋 Profile Configuration

Each profile can have the following settings:

- **Name**: Unique identifier for the profile
- **GitHub Username**: Your GitHub username
- **Email**: Email address for commits
- **Default Branch**: Default branch name (main/master)
- **SSH Key Path**: Path to SSH private key
- **Auto Push**: Automatically push after commits
- **Sign Commits**: Sign commits with GPG

## 🔧 Advanced Usage

### Multiple SSH Keys
```bash
# Generate separate SSH keys for each account
ssh-keygen -t ed25519 -C "work@company.com" -f ~/.ssh/id_ed25519_work
ssh-keygen -t ed25519 -C "personal@gmail.com" -f ~/.ssh/id_ed25519_personal

# Add profiles with different SSH keys
python github_profile_switcher_cli.py add work --username work-account --email work@company.com --ssh-key ~/.ssh/id_ed25519_work
python github_profile_switcher_cli.py add personal --username personal-account --email personal@gmail.com --ssh-key ~/.ssh/id_ed25519_personal
```

### SSH Config Setup
Create `~/.ssh/config`:
```
# Work account
Host github-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_work

# Personal account
Host github-personal
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_personal
```

Then clone repositories using:
```bash
git clone git@github-work:company/repo.git
git clone git@github-personal:username/repo.git
```

### Configuration Export/Import
```bash
# Export your configuration
python github_profile_switcher_cli.py export profiles.json

# Import configuration on another machine
python github_profile_switcher_cli.py import profiles.json
```

## 🎨 VS Code Integration

### Status Bar
The current GitHub profile is displayed in the VS Code status bar. Click it to switch profiles.

### Command Palette
Access all profile management commands through the command palette:
- `GitHub Profile: Switch Profile`
- `GitHub Profile: Add Profile`
- `GitHub Profile: List Profiles`
- `GitHub Profile: Test SSH Connection`

### Settings
Configure the extension in VS Code settings:
```json
{
    "github-profile-switcher.configPath": "/path/to/profiles.json",
    "github-profile-switcher.showInStatusBar": true,
    "github-profile-switcher.autoSwitch": false
}
```

## 🔍 Troubleshooting

### SSH Connection Issues
```bash
# Test SSH connection
python github_profile_switcher_cli.py test-ssh

# Check SSH agent
ssh-add -l

# Add SSH key manually
ssh-add ~/.ssh/your_private_key
```

### Git Configuration Issues
```bash
# Check current Git configuration
git config --global --list

# Reset Git configuration
git config --global --unset user.name
git config --global --unset user.email
```

### Permission Issues
```bash
# Check repository permissions
git ls-remote origin

# Verify GitHub access
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user
```

## 📁 File Structure

```
Git-Helper/
├── github_profile_switcher.py          # GUI application
├── github_profile_switcher_cli.py      # CLI tool
├── vscode-extension/                  # VS Code extension
│   ├── package.json
│   └── src/extension.ts
└── README.md                          # This file
```

## 🔒 Security Notes

- SSH keys are stored locally and never transmitted
- Profile configurations are stored in `~/.github-profiles/`
- No sensitive data is logged or transmitted
- SSH agent integration is optional and secure

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: Check this README and inline help
- **CLI Help**: Run `python github_profile_switcher_cli.py --help`

## 🎉 Examples

### Workflow Example
```bash
# Morning: Switch to work profile
python github_profile_switcher_cli.py switch work

# Work on company projects
git clone git@github-work:company/project.git
cd project
git commit -m "Work on feature"
git push

# Evening: Switch to personal profile
python github_profile_switcher_cli.py switch personal

# Work on personal projects
git clone git@github-personal:username/personal-project.git
cd personal-project
git commit -m "Personal project update"
git push
```

### VS Code Workflow
1. Open VS Code
2. Click profile in status bar
3. Select "work" profile
4. All Git operations use work account
5. Switch to "personal" profile for personal projects
6. Status bar shows current profile

This tool makes managing multiple GitHub accounts seamless and secure! 🚀
