import subprocess
import json

def check_for_updates(tool_name):
    """Check for updates of the external tool."""
    try:
        result = subprocess.run([tool_name, '--version'], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

def update_tool(tool_name):
    """Update the external tool."""
    try:
        subprocess.run(['pip', 'install', '--upgrade', tool_name], check=True)
        return f"{tool_name} updated successfully."
    except subprocess.CalledProcessError as e:
        return str(e)

def main():
    tools = ["androguard", "jadx", "apktool"]
    updates = {}
    
    for tool in tools:
        current_version = check_for_updates(tool)
        updates[tool] = current_version
        
        # Check if update is needed (pseudo code)
        if "outdated" in current_version:
            update_status = update_tool(tool)
            updates[tool] += f" | Update Status: {update_status}"
    
    with open('update_status.json', 'w') as f:
        json.dump(updates, f, indent=4)

if __name__ == "__main__":
    main()
