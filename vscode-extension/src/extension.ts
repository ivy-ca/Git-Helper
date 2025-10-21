import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { exec } from 'child_process';

interface GitHubProfile {
    name: string;
    username: string;
    email: string;
    default_branch: string;
    ssh_key?: string;
    auto_push?: boolean;
    sign_commits?: boolean;
}

interface ProfileConfig {
    profiles: { [key: string]: GitHubProfile };
    current_profile?: string;
}

export function activate(context: vscode.ExtensionContext) {
    console.log('GitHub Profile Switcher extension is now active!');

    // Register commands
    const switchProfileCommand = vscode.commands.registerCommand('github-profile-switcher.switchProfile', () => {
        switchProfile();
    });

    const addProfileCommand = vscode.commands.registerCommand('github-profile-switcher.addProfile', () => {
        addProfile();
    });

    const listProfilesCommand = vscode.commands.registerCommand('github-profile-switcher.listProfiles', () => {
        listProfiles();
    });

    const testSSHCommand = vscode.commands.registerCommand('github-profile-switcher.testSSH', () => {
        testSSH();
    });

    // Add commands to context
    context.subscriptions.push(switchProfileCommand);
    context.subscriptions.push(addProfileCommand);
    context.subscriptions.push(listProfilesCommand);
    context.subscriptions.push(testSSHCommand);

    // Create status bar item
    const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.command = 'github-profile-switcher.switchProfile';
    statusBarItem.tooltip = 'Click to switch GitHub profile';
    
    // Update status bar
    updateStatusBar(statusBarItem);
    
    // Watch for configuration changes
    const configWatcher = vscode.workspace.createFileSystemWatcher('**/.github-profiles/profiles.json');
    configWatcher.onDidChange(() => {
        updateStatusBar(statusBarItem);
    });

    context.subscriptions.push(statusBarItem);
    context.subscriptions.push(configWatcher);
}

function getConfigPath(): string {
    const config = vscode.workspace.getConfiguration('github-profile-switcher');
    const configPath = config.get<string>('configPath');
    
    if (configPath) {
        return configPath;
    }
    
    // Default path
    const homeDir = require('os').homedir();
    return path.join(homeDir, '.github-profiles', 'profiles.json');
}

function loadProfiles(): ProfileConfig {
    const configPath = getConfigPath();
    
    try {
        if (fs.existsSync(configPath)) {
            const data = fs.readFileSync(configPath, 'utf8');
            return JSON.parse(data);
        }
    } catch (error) {
        console.error('Error loading profiles:', error);
    }
    
    return { profiles: {} };
}

function saveProfiles(config: ProfileConfig): void {
    const configPath = getConfigPath();
    const configDir = path.dirname(configPath);
    
    // Create directory if it doesn't exist
    if (!fs.existsSync(configDir)) {
        fs.mkdirSync(configDir, { recursive: true });
    }
    
    try {
        fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
    } catch (error) {
        console.error('Error saving profiles:', error);
        vscode.window.showErrorMessage('Failed to save profiles');
    }
}

function updateStatusBar(statusBarItem: vscode.StatusBarItem): void {
    const config = loadProfiles();
    const showInStatusBar = vscode.workspace.getConfiguration('github-profile-switcher').get<boolean>('showInStatusBar');
    
    if (showInStatusBar && config.current_profile) {
        const profile = config.profiles[config.current_profile];
        if (profile) {
            statusBarItem.text = `$(github) ${profile.username || config.current_profile}`;
            statusBarItem.show();
        } else {
            statusBarItem.hide();
        }
    } else {
        statusBarItem.hide();
    }
}

async function switchProfile(): Promise<void> {
    const config = loadProfiles();
    const profiles = Object.keys(config.profiles);
    
    if (profiles.length === 0) {
        vscode.window.showInformationMessage('No profiles configured. Use "Add GitHub Profile" to create one.');
        return;
    }
    
    const selectedProfile = await vscode.window.showQuickPick(profiles, {
        placeHolder: 'Select a GitHub profile to switch to',
        title: 'Switch GitHub Profile'
    });
    
    if (selectedProfile) {
        const profile = config.profiles[selectedProfile];
        
        try {
            // Update Git configuration
            await updateGitConfig(profile);
            
            // Update SSH configuration if needed
            if (profile.ssh_key) {
                await updateSSHConfig(profile);
            }
            
            // Set current profile
            config.current_profile = selectedProfile;
            saveProfiles(config);
            
            vscode.window.showInformationMessage(`Switched to profile: ${selectedProfile}`);
            
            // Refresh status bar
            updateStatusBar(vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100));
            
        } catch (error) {
            vscode.window.showErrorMessage(`Failed to switch to profile: ${error}`);
        }
    }
}

async function addProfile(): Promise<void> {
    const name = await vscode.window.showInputBox({
        prompt: 'Enter profile name',
        placeHolder: 'e.g., work, personal'
    });
    
    if (!name) return;
    
    const username = await vscode.window.showInputBox({
        prompt: 'Enter GitHub username',
        placeHolder: 'e.g., john-doe'
    });
    
    if (!username) return;
    
    const email = await vscode.window.showInputBox({
        prompt: 'Enter email address',
        placeHolder: 'e.g., john@example.com'
    });
    
    if (!email) return;
    
    const branch = await vscode.window.showInputBox({
        prompt: 'Enter default branch',
        placeHolder: 'main',
        value: 'main'
    }) || 'main';
    
    const sshKey = await vscode.window.showInputBox({
        prompt: 'Enter SSH key path (optional)',
        placeHolder: '/path/to/ssh/key'
    });
    
    const config = loadProfiles();
    
    if (config.profiles[name]) {
        vscode.window.showErrorMessage(`Profile '${name}' already exists!`);
        return;
    }
    
    config.profiles[name] = {
        name,
        username,
        email,
        default_branch: branch,
        ssh_key: sshKey,
        auto_push: false,
        sign_commits: false
    };
    
    saveProfiles(config);
    vscode.window.showInformationMessage(`Added profile: ${name}`);
}

function listProfiles(): void {
    const config = loadProfiles();
    const profiles = Object.keys(config.profiles);
    
    if (profiles.length === 0) {
        vscode.window.showInformationMessage('No profiles configured.');
        return;
    }
    
    let message = 'GitHub Profiles:\n\n';
    for (const profileName of profiles) {
        const profile = config.profiles[profileName];
        const status = profileName === config.current_profile ? ' (Active)' : '';
        message += `${profileName}${status}\n`;
        message += `  Username: ${profile.username}\n`;
        message += `  Email: ${profile.email}\n`;
        message += `  Branch: ${profile.default_branch}\n\n`;
    }
    
    vscode.window.showInformationMessage(message);
}

async function testSSH(): Promise<void> {
    vscode.window.showInformationMessage('Testing SSH connection to GitHub...');
    
    return new Promise((resolve) => {
        exec('ssh -T git@github.com', (error, stdout, stderr) => {
            if (error && error.code !== 1) {
                vscode.window.showErrorMessage(`SSH test failed: ${error.message}`);
            } else if (stderr.includes('successfully authenticated')) {
                vscode.window.showInformationMessage('SSH connection to GitHub successful!');
            } else {
                vscode.window.showWarningMessage(`SSH connection failed: ${stderr}`);
            }
            resolve();
        });
    });
}

async function updateGitConfig(profile: GitHubProfile): Promise<void> {
    return new Promise((resolve, reject) => {
        const commands = [
            `git config --global user.name "${profile.username}"`,
            `git config --global user.email "${profile.email}"`,
            `git config --global init.defaultBranch "${profile.default_branch}"`
        ];
        
        let completed = 0;
        const total = commands.length;
        
        commands.forEach(command => {
            exec(command, (error) => {
                completed++;
                if (error) {
                    reject(new Error(`Failed to update Git config: ${error.message}`));
                    return;
                }
                
                if (completed === total) {
                    resolve();
                }
            });
        });
    });
}

async function updateSSHConfig(profile: GitHubProfile): Promise<void> {
    if (!profile.ssh_key || !fs.existsSync(profile.ssh_key)) {
        return;
    }
    
    return new Promise((resolve, reject) => {
        exec(`ssh-add "${profile.ssh_key}"`, (error) => {
            if (error) {
                // SSH agent might not be running, which is not critical
                console.warn('SSH agent not running or key already added');
            }
            resolve();
        });
    });
}

export function deactivate() {}
