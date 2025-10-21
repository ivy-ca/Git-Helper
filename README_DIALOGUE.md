# Git Helper Dialogue - Interactive Usage Guide

An interactive, dialogue-style Git helper that provides a user-friendly menu-driven interface for common Git operations.

## Installation

1. Make sure Python 3.6+ is installed
2. The script is ready to use - no additional dependencies required

## Usage

```bash
python git_helper_dialogue.py
```

## Features

### 🎯 Interactive Menu System
- **Main Menu**: Choose from 12 different Git operations
- **Sub-menus**: Each operation has its own guided interface
- **Confirmation prompts**: Safety checks for destructive operations
- **Default values**: Smart defaults for common inputs

### 📊 Repository Information
- Shows current repository name
- Displays current branch
- Real-time status updates

### 🔧 Available Operations

#### 1. **📊 Show Status**
- Current branch information
- Working directory status
- Last commit details
- Clean/unstaged changes overview

#### 2. **📁 Add Files**
- Add all changes
- Add specific files
- Add by pattern (e.g., `*.py`, `src/**/*.js`)
- Visual confirmation of changes

#### 3. **💾 Create Commit**
- Shows staged changes before committing
- Commit message input
- Option to amend last commit
- Validation and error handling

#### 4. **🚀 Push Changes**
- Current branch detection
- Remote selection (default: origin)
- Force push option with warning
- Real-time push feedback

#### 5. **📥 Pull Changes**
- Current branch detection
- Remote selection (default: origin)
- Pull progress and results

#### 6. **🌿 Manage Branches**
- List all branches
- Create new branch
- Switch to existing branch
- Delete branch (with confirmation)

#### 7. **📜 View History**
- Customizable commit limit
- Clean, readable commit log
- One-line commit format

#### 8. **💾 Manage Stash**
- List all stashes
- Save current changes with optional message
- Apply latest stash
- Stash management overview

#### 9. **📋 Show Differences**
- Unstaged changes
- Staged changes
- All changes (vs HEAD)
- Clear diff display

#### 10. **⚡ Quick Workflow**
- Add all changes → Commit → Push
- Optional custom commit message
- Confirmation before execution
- Perfect for quick fixes

#### 11. **🔄 Sync Workflow**
- Pull latest changes → Add all → Commit → Push
- Handles merge conflicts gracefully
- Smart change detection
- Complete sync process

## Example Session

```
============================================================
🔧 Git Helper Dialogue - Interactive Git Operations
============================================================
📁 Repository: my-project
🌿 Current branch: main

==================================================
🔧 Main Menu
==================================================
1. 📊 Show Status
2. 📁 Add Files
3. 💾 Create Commit
4. 🚀 Push Changes
5. 📥 Pull Changes
6. 🌿 Manage Branches
7. 📜 View History
8. 💾 Manage Stash
9. 📋 Show Differences
10. ⚡ Quick Workflow
11. 🔄 Sync Workflow
12. ❌ Exit
==================================================
👉 Enter your choice: 10

⚡ Quick Commit Workflow
==============================
Enter commit message [Quick commit - 2024-01-15 14:30:25]: Fix user authentication bug
❓ This will: Add all changes → Commit → Push. Continue? (y/N): y

🔄 Executing quick workflow...
📁 Adding all changes...
💾 Creating commit...
🚀 Pushing changes...
✅ Quick workflow completed successfully!
```

## Safety Features

- **Confirmation prompts** for destructive operations
- **Default values** to prevent empty inputs
- **Error handling** with clear messages
- **Keyboard interrupt** handling (Ctrl+C)
- **Repository validation** before operations

## Tips

1. **Quick Workflow** is perfect for simple commits
2. **Sync Workflow** handles the complete pull-commit-push cycle
3. All operations show **real-time feedback**
4. Use **confirmation prompts** to avoid mistakes
5. The interface **remembers your current branch** and repository

## Error Handling

The dialogue includes comprehensive error handling:
- Validates Git repository status
- Checks for Git installation
- Provides clear error messages
- Handles keyboard interrupts gracefully
- Shows helpful suggestions for common issues

## Cross-Platform Compatibility

- Works on Windows, macOS, and Linux
- Uses standard Python libraries only
- No external dependencies required
- Consistent behavior across platforms
