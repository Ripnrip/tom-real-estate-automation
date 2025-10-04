# Using Your Existing Chrome Browser 🌐

This guide explains how to use your existing Chrome browser with the AppFolio automation instead of creating new browser windows every time.

## 🎯 Benefits

- **No more new browser windows** - Uses your current Chrome session
- **Faster startup** - No need to launch new browser instances
- **Better debugging** - See exactly what the automation is doing
- **Persistent sessions** - Keep your existing tabs and login states

## 🚀 Quick Start

### Option 1: Automatic Setup (Recommended)
Just run the automation normally - it will automatically:
1. Try to connect to your existing Chrome
2. If not available, start Chrome with debugging enabled
3. Connect to that Chrome instance

```bash
python3 scripts/appfolio_automation.py --test-login
```

### Option 2: Manual Chrome Setup
If you want more control, start Chrome with debugging first:

```bash
# Start Chrome with debugging enabled
python3 scripts/start_chrome_debug.py

# Then run your automation
python3 scripts/appfolio_automation.py --test-login
```

## 🔧 How It Works

### Remote Debugging
The system uses Chrome's remote debugging protocol:
- Chrome runs with `--remote-debugging-port=9222`
- Automation connects to `http://localhost:9222`
- No new browser windows are created

### Configuration
The settings in `config/settings.py`:
```python
BROWSER_CONFIG = {
    "connect_to_existing": True,
    "remote_debugging_port": 9222,
    # ... other settings
}
```

## 📋 Usage Steps

1. **First Time Setup**:
   ```bash
   # Start Chrome with debugging (optional)
   python3 scripts/start_chrome_debug.py
   ```

2. **Run Automation**:
   ```bash
   # The automation will connect to your existing Chrome
   python3 scripts/appfolio_automation.py --test-login
   ```

3. **Watch the Magic** ✨:
   - Your existing Chrome browser will be used
   - New tabs will open for automation tasks
   - You can watch the process in real-time

## 🛠️ Troubleshooting

### Chrome Not Connecting?
```bash
# Check if Chrome is running with debugging
curl http://localhost:9222/json/version

# If not, start it manually
python3 scripts/start_chrome_debug.py
```

### Port Already in Use?
```bash
# Check what's using port 9222
lsof -i :9222

# Kill the process if needed
kill -9 <PID>
```

### Still Creating New Windows?
- Make sure `connect_to_existing: True` in `config/settings.py`
- Check that Chrome is running with `--remote-debugging-port=9222`
- Try closing all Chrome windows and running the debug starter

## 💡 Tips

1. **Keep Chrome Open**: Leave Chrome running between automation runs
2. **Use Separate Profile**: Consider using a dedicated Chrome profile for automation
3. **Monitor Debug Interface**: Visit `http://localhost:9222` to see debug info
4. **Check Logs**: Look at the automation logs for connection status

## 🔍 Debug Interface

When Chrome is running with debugging, you can visit:
- **Debug Interface**: `http://localhost:9222`
- **Available Pages**: `http://localhost:9222/json`
- **Version Info**: `http://localhost:9222/json/version`

## ⚙️ Advanced Configuration

### Custom Debug Port
Edit `config/settings.py`:
```python
BROWSER_CONFIG = {
    "remote_debugging_port": 9223,  # Use different port
    # ...
}
```

### Disable Existing Browser
To go back to creating new browsers:
```python
BROWSER_CONFIG = {
    "connect_to_existing": False,  # Disable existing browser connection
    # ...
}
```

## 🎉 Success Indicators

Look for these log messages:
- ✅ `Connected to existing Chrome browser successfully`
- 🚀 `Started Chrome with debugging on port 9222`
- 💡 `Starting Chrome with remote debugging enabled...`

Now you can enjoy seamless automation without browser window spam! 🎊