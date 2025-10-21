# Git Helper - Usage Guide

A comprehensive Python script for common Git operations with a user-friendly interface.

## Installation

1. Make sure Python 3.6+ is installed
2. The script is ready to use - no additional dependencies required

## Usage

```bash
python git_helper.py <command> [arguments]
```

## Available Commands

### Basic Operations
- `status` - Show repository status and current branch info
- `add [files]` - Add files to staging area (default: all files)
- `commit <message>` - Create a commit with the given message
- `push [remote] [branch]` - Push changes to remote repository
- `pull [remote] [branch]` - Pull changes from remote repository

### Branch Management
- `branch` - List all branches
- `branch <name>` - Switch to specified branch
- `branch create <name>` - Create and switch to new branch
- `branch delete <name>` - Delete specified branch

### History & Differences
- `log [limit]` - Show commit history (default: 10 commits)
- `diff` - Show unstaged changes
- `diff --staged` - Show staged changes

### Stash Operations
- `stash` - List all stashes
- `stash save [message]` - Save current changes to stash
- `stash pop` - Apply and remove the latest stash

### Reset Operations
- `reset [mode] [commit]` - Reset repository state
  - `mode`: soft, mixed, hard (default: soft)
  - `commit`: commit hash or reference (default: HEAD~1)

### Remote Management
- `remote` - List all remotes
- `remote add <name> <url>` - Add new remote repository

### Quick Workflows
- `quick [message]` - Quick commit: add all → commit → push
- `sync` - Sync with remote: pull → add all → commit → push

## Examples

```bash
# Check repository status
python git_helper.py status

# Add all changes and commit
python git_helper.py add
python git_helper.py commit "Fix bug in user authentication"

# Quick commit workflow
python git_helper.py quick "Update documentation"

# Create and switch to new branch
python git_helper.py branch create feature/new-feature

# Sync with remote repository
python git_helper.py sync

# Show last 20 commits
python git_helper.py log 20

# Save current work to stash
python git_helper.py stash save "Work in progress"

# Reset last commit (soft reset)
python git_helper.py reset soft HEAD~1
```

## Features

- ✅ User-friendly interface with emojis and clear messages
- ✅ Error handling and validation
- ✅ Works in any Git repository
- ✅ Cross-platform compatibility
- ✅ No external dependencies
- ✅ Comprehensive command coverage
- ✅ Quick workflow shortcuts

## Error Handling

The script includes comprehensive error handling:
- Validates Git repository status
- Checks for Git installation
- Provides clear error messages
- Handles keyboard interrupts gracefully

## Tips

1. Use `quick` command for simple commits when you want to add all changes
2. Use `sync` when you want to pull latest changes and push your work
3. The script automatically detects your current branch for push/pull operations
4. All commands provide visual feedback with emojis and status messages

