#!/usr/bin/env python3
"""
Helper script to start Chrome with remote debugging enabled.
This allows the automation to connect to your existing Chrome browser.
"""

import subprocess
import sys
import time
import requests
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from config.settings import BROWSER_CONFIG

def check_chrome_debug_running(port=9222):
    """Check if Chrome is already running with debugging enabled"""
    try:
        response = requests.get(f"http://localhost:{port}/json/version", timeout=2)
        return response.status_code == 200
    except:
        return False

def start_chrome_with_debug():
    """Start Chrome with remote debugging enabled"""
    chrome_path = BROWSER_CONFIG.get("chrome_executable_path", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    debug_port = BROWSER_CONFIG.get("remote_debugging_port", 9222)
    
    print(f"🔍 Checking if Chrome is already running with debugging on port {debug_port}...")
    
    if check_chrome_debug_running(debug_port):
        print(f"✅ Chrome is already running with debugging enabled on port {debug_port}")
        print(f"🌐 Debug interface: http://localhost:{debug_port}")
        return True
    
    print(f"🚀 Starting Chrome with remote debugging on port {debug_port}...")
    
    try:
        # Get profile configuration
        profile_directory = BROWSER_CONFIG.get("profile_directory", "Profile 1")
        user_data_dir = BROWSER_CONFIG.get("user_data_dir", "~/Library/Application Support/Google/Chrome")
        # Expand the user directory path
        user_data_dir = str(Path(user_data_dir).expanduser())
        
        print(f"👤 Using Chrome profile: {profile_directory} (Tom Hashimoto)")
        print(f"📁 User data directory: {user_data_dir}")
        
        # Start Chrome with debugging enabled and specific profile
        subprocess.Popen([
            chrome_path,
            f"--remote-debugging-port={debug_port}",
            f"--user-data-dir={user_data_dir}",
            f"--profile-directory={profile_directory}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-web-security",  # Helps with automation
            "--disable-features=VizDisplayCompositor"  # Helps with stability
        ])
        
        # Wait for Chrome to start
        print("⏳ Waiting for Chrome to start...")
        for i in range(10):
            time.sleep(1)
            if check_chrome_debug_running(debug_port):
                print(f"✅ Chrome started successfully with debugging enabled!")
                print(f"🌐 Debug interface: http://localhost:{debug_port}")
                print(f"📱 You can now run the automation - it will connect to this Chrome instance")
                return True
            print(f"   Waiting... ({i+1}/10)")
        
        print("❌ Chrome didn't start with debugging in time")
        return False
        
    except Exception as e:
        print(f"❌ Failed to start Chrome: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Chrome Debug Starter for AppFolio Automation")
    print("=" * 50)
    
    success = start_chrome_with_debug()
    
    if success:
        print("\n🎉 Setup complete!")
        print("💡 Tips:")
        print("   - Keep this Chrome window open")
        print("   - Run your automation scripts normally")
        print("   - They will connect to this Chrome instance")
        print("   - No more new browser windows!")
    else:
        print("\n❌ Setup failed!")
        print("💡 Try:")
        print("   - Close all Chrome windows first")
        print("   - Run this script again")
        print("   - Check Chrome installation path")