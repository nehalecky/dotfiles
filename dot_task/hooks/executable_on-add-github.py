#!/usr/bin/env python3
"""
GitHub Integration Hook for Taskwarrior

Automatically converts GitHub issue/PR references in task descriptions to clickable URLs.
Supports multiple patterns:
- tw-123, TW-123 → Taskwarrior issues
- #123 → Current repo issues (if github.default_repo is set in .taskrc)
- org/repo#123 → Specific repo issues
- gh-123, GH-123 → Generic GitHub pattern (requires default repo)
"""

import sys
import json
import re
import subprocess

def get_taskrc_value(key):
    """Get a value from taskrc configuration"""
    try:
        result = subprocess.run(['task', '_get', f'rc.{key}'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def process_github_references(description):
    """Convert GitHub references to URLs"""
    if not description:
        return description
    
    # Get default repository from config (format: owner/repo)
    default_repo = get_taskrc_value('github.default_repo')
    
    # Pattern replacements
    patterns = [
        # Taskwarrior issues: tw-123, TW-123
        (r'\b(tw|TW)-(\d+)\b', 
         r'https://github.com/GothenburgBitFactory/taskwarrior/issues/\2'),
        
        # Specific repository: owner/repo#123
        (r'\b([a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+)#(\d+)\b', 
         r'https://github.com/\1/issues/\2'),
        
        # Generic GitHub patterns: gh-123, GH-123 (requires default repo)
        (r'\b(gh|GH)-(\d+)\b', 
         f'https://github.com/{default_repo}/issues/\\2' if default_repo else r'\1-\2'),
        
        # Simple #123 pattern (requires default repo)
        (r'(?<!/)#(\d+)\b', 
         f'https://github.com/{default_repo}/issues/\\1' if default_repo else r'#\1'),
    ]
    
    result = description
    for pattern, replacement in patterns:
        result = re.sub(pattern, replacement, result)
    
    return result

def main():
    """Main hook function"""
    try:
        # Read the task from stdin
        original = sys.stdin.readline().strip()
        if not original:
            return
        
        # Parse the task
        task = json.loads(original)
        
        # Process description for GitHub references
        if 'description' in task:
            new_description = process_github_references(task['description'])
            if new_description != task['description']:
                task['description'] = new_description
        
        # Output the modified task
        print(json.dumps(task, separators=(',', ':')))
        
    except Exception as e:
        # Log error but don't fail the task creation
        with open('/tmp/taskwarrior-github-hook.log', 'a') as f:
            f.write(f"Error in GitHub hook: {e}\n")
        # Output original task unchanged
        print(original)

if __name__ == '__main__':
    main()