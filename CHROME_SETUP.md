# Chrome Browser Setup for AppFolio Automation

## 🌐 Using Your Existing Chrome Browser

The automation system is now configured to use your existing Chrome browser instead of a headless browser. This provides several advantages:

### ✅ Benefits:
- **Visual Feedback**: See exactly what the automation is doing
- **Better Debugging**: Watch the process in real-time
- **Easier Troubleshooting**: Identify issues immediately
- **Manual Intervention**: Take control if needed

### 🔧 Configuration Applied:

1. **Browser Settings Updated**: 
   - `headless: false` - Browser will be visible
   - Chrome executable path configured for macOS
   - Download path set to your project data folder

2. **Chrome Path**: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`

### 🚀 How It Works:

When you run the automation:
1. A new Chrome window will open automatically
2. The AI agent will control this browser window
3. You can watch the automation process in real-time
4. Downloads will go to your project's `data/appfolio/` folders

### 📋 Before Running:

1. **Close Unnecessary Chrome Windows**: For best performance
2. **Ensure Chrome is Updated**: Latest version recommended
3. **Check Download Settings**: Chrome should allow downloads

### 🧪 Test the Setup:

```bash
# Test with your existing Chrome browser
python3 test_setup.py
```

### 🔍 What You'll See:

- Chrome window opens automatically
- Browser navigates to test page
- AI agent performs actions
- Real-time feedback in terminal

### 💡 Tips:

- **Don't close the automation window** while it's running
- **Let the AI complete its tasks** before manual intervention
- **Check the logs folder** for detailed execution logs
- **Use `--test-login` flag** to test AppFolio login only

### 🛠 Troubleshooting:

If Chrome doesn't open:
1. Verify Chrome is installed in `/Applications/`
2. Check Chrome permissions in System Preferences
3. Try running with `sudo` if permission issues occur

The automation will now use your familiar Chrome browser interface!