"""
AppFolio Automation Script using browser-use
Automates login, report downloads, and document monitoring
"""

import os
import sys
from datetime import datetime
from pathlib import Path
import asyncio
from loguru import logger

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from browser_use import Agent, Browser
from config.settings import (
    APPFOLIO_CONFIG, BROWSER_CONFIG, PATHS, AI_CONFIG
)

class AppFolioAutomator:
    def __init__(self):
        """Initialize the AppFolio automation system"""
        self.setup_logging()
        self.browser = None
        self.agent = None
        
    def setup_logging(self):
        """Configure logging for the automation system"""
        log_file = PATHS["logs"] / f"appfolio_automation_{datetime.now().strftime('%Y%m%d')}.log"
        logger.add(
            log_file,
            rotation="1 day",
            retention="30 days",
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
        )
        logger.info("AppFolio Automation System initialized")

    async def initialize_browser(self):
        """Initialize browser-use with configuration to use existing Chrome"""
        try:
            # Try to connect to existing Chrome instance first
            if BROWSER_CONFIG.get("connect_to_existing"):
                debug_port = BROWSER_CONFIG.get("remote_debugging_port", 9222)
                cdp_url = f"http://localhost:{debug_port}"
                
                try:
                    # Test if Chrome is running with remote debugging
                    import aiohttp
                    async with aiohttp.ClientSession() as session:
                        async with session.get(f"{cdp_url}/json/version", timeout=2) as response:
                            if response.status == 200:
                                logger.info(f"✅ Found existing Chrome with remote debugging on port {debug_port}")
                                # Connect to existing Chrome using cdp_url
                                self.browser = Browser(cdp_url=cdp_url)
                                return True
                except Exception as connect_error:
                    logger.warning(f"Could not connect to existing Chrome: {connect_error}")
                    logger.info("💡 Starting Chrome with remote debugging enabled...")
                    
                    # Start Chrome with remote debugging if not already running
                    import subprocess
                    chrome_path = BROWSER_CONFIG.get("chrome_executable_path", "google-chrome")
                    profile_directory = BROWSER_CONFIG.get("profile_directory", "Profile 1")
                    user_data_dir = BROWSER_CONFIG.get("user_data_dir", "~/Library/Application Support/Google/Chrome")
                    # Expand the user directory path
                    user_data_dir = str(Path(user_data_dir).expanduser())
                    
                    try:
                        subprocess.Popen([
                            chrome_path,
                            f"--remote-debugging-port={debug_port}",
                            f"--user-data-dir={user_data_dir}",
                            f"--profile-directory={profile_directory}",
                            "--no-first-run",
                            "--no-default-browser-check",
                            "--disable-web-security",
                            "--disable-features=VizDisplayCompositor"
                        ])
                        logger.info(f"🚀 Started Chrome with debugging on port {debug_port}")
                        
                        # Wait a moment for Chrome to start
                        await asyncio.sleep(5)
                        
                        # Try connecting again
                        try:
                            async with aiohttp.ClientSession() as session:
                                async with session.get(f"{cdp_url}/json/version", timeout=5) as response:
                                    if response.status == 200:
                                        logger.info("✅ Successfully connected to newly started Chrome")
                                        self.browser = Browser(cdp_url=cdp_url)
                                        return True
                        except Exception as retry_error:
                            logger.warning(f"Still could not connect after starting Chrome: {retry_error}")
                    
                    except Exception as start_error:
                        logger.warning(f"Could not start Chrome with debugging: {start_error}")
            
            # Fallback: Launch new browser instance
            logger.info("🔄 Falling back to launching new browser instance")
            browser_config = {
                "headless": BROWSER_CONFIG["headless"],
                "viewport": BROWSER_CONFIG["viewport"],
                "downloads_path": str(BROWSER_CONFIG["downloads_path"])
            }
            
            if BROWSER_CONFIG.get("chrome_executable_path"):
                browser_config["executable_path"] = BROWSER_CONFIG["chrome_executable_path"]
            
            self.browser = Browser(**browser_config)
            logger.info("✅ Browser initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            logger.info("Tip: Make sure Chrome is installed and accessible")
            return False

    async def create_agent(self, task_description):
        """Create a browser-use agent for the specific task"""
        try:
            # Choose AI model based on configuration
            if AI_CONFIG["gemini_api_key"]:
                from browser_use import ChatGoogle
                llm = ChatGoogle(
                    model=AI_CONFIG["model"],
                    api_key=AI_CONFIG["gemini_api_key"]
                )
            elif AI_CONFIG["openai_api_key"]:
                from browser_use import ChatOpenAI
                llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    api_key=AI_CONFIG["openai_api_key"]
                )
            else:
                raise ValueError("No AI API key configured. Please set GEMINI_API_KEY or OPENAI_API_KEY")

            self.agent = Agent(
                task=task_description,
                llm=llm,
                browser=self.browser
            )
            logger.info(f"Agent created for task: {task_description}")
            return True
        except Exception as e:
            logger.error(f"Failed to create agent: {e}")
            return False

    async def login_to_appfolio(self):
        """Automate login to AppFolio"""
        if not APPFOLIO_CONFIG["username"] or not APPFOLIO_CONFIG["password"]:
            logger.error("AppFolio credentials not configured. Please check .env file")
            return False

        task = f"""
        Navigate to {APPFOLIO_CONFIG["base_url"]} and log in with the following credentials:
        - Username: {APPFOLIO_CONFIG["username"]}
        - Password: {APPFOLIO_CONFIG["password"]}
        
        After clicking the login button, if Chrome shows a popup asking to save the password, click "Never" to dismiss it.
        
        STOP immediately after handling any password save popup. Do NOT attempt to handle 2FA or any additional authentication steps.
        The task is complete once you have submitted the login form and dismissed any password save prompts.
        """
        
        try:
            if await self.create_agent(task):
                result = await self.agent.run()
                logger.info("AppFolio login completed")
                return True
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False

    async def handle_password_save_popup(self):
        """Handle Chrome's password save popup by clicking 'Never'"""
        task = """
        Look for any Chrome password save popup or notification that asks to save the password.
        If you see a popup with options like "Save", "Never", or "Not now", click "Never".
        If no password save popup is visible, do nothing.
        This task is complete once any password save popup has been dismissed or if no popup exists.
        """
        
        try:
            if await self.create_agent(task):
                result = await self.agent.run()
                logger.info("Password save popup handling completed")
                return True
        except Exception as e:
            logger.info(f"No password save popup found or already handled: {e}")
            return True  # Return True since this is not a critical failure

    async def handle_2fa_manually(self):
        """Handle 2FA manually with user input"""
        logger.info("🔐 2FA detected - Manual intervention required")
        
        print("\n" + "="*60)
        print("🔐 TWO-FACTOR AUTHENTICATION REQUIRED")
        print("="*60)
        print("Please complete the 2FA process in the browser window:")
        print("1. Check your phone/email for the 2FA code")
        print("2. Enter the code in the browser")
        print("3. Complete any additional security steps")
        print("4. Wait until you reach the main dashboard")
        print("="*60)
        
        # Wait for user confirmation
        input("Press ENTER when you have completed 2FA and are on the main dashboard...")
        
        logger.info("✅ 2FA completed by user, continuing automation")
        print("✅ 2FA completed! Continuing with automation...\n")
        
        # Verify we're on the dashboard
        task = """
        Verify that we are successfully logged into AppFolio and on the main dashboard.
        Look for typical dashboard elements like navigation menu, property listings, or dashboard widgets.
        If we're not on the dashboard yet, wait a moment and check again.
        """
        
        try:
            if await self.create_agent(task):
                result = await self.agent.run()
                logger.info("Dashboard verification completed")
                return True
        except Exception as e:
            logger.error(f"Dashboard verification failed: {e}")
            return False

    async def download_ledger_report(self):
        """Download the latest ledger report"""
        today = datetime.now().strftime("%Y-%m-%d")
        current_month = datetime.now().strftime("%B %Y")
        ledger_folder = PATHS["ledgers"] / today
        ledger_folder.mkdir(exist_ok=True)
        
        task = f"""
        You are now on the AppFolio dashboard. Navigate to download the General Ledger report for {current_month}.
        
        SPECIFIC STEPS:
        1. Look for "Reports" in the main navigation menu and click it
        2. Find "General Ledger" or "Accounting Reports" section
        3. Click on "General Ledger" report
        4. Set the date range to the current month ({current_month})
        5. Choose Excel (.xlsx) format if available, otherwise CSV
        6. Click "Generate Report" or "Download" button
        7. Wait for the download to complete
        
        IMPORTANT: The browser's default download folder is configured, so the file will be saved automatically.
        If you encounter any popups or confirmations, accept them to proceed with the download.
        
        Complete this task step by step and confirm when the download has finished.
        """
        
        try:
            if await self.create_agent(task):
                result = await self.agent.run()
                logger.info(f"Ledger report download initiated for {current_month}")
                return True
        except Exception as e:
            logger.error(f"Ledger download failed: {e}")
            return False

    async def download_documents(self):
        """Download new leases, PMAs, and work order receipts"""
        task = """
        Navigate to the Documents section in AppFolio and check for new documents:
        
        1. Go to Documents or Files section
        2. Look for new leases, PMAs (Property Management Agreements), and work order receipts
        3. Download any new documents that haven't been downloaded before
        4. Organize them into appropriate folders
        
        Focus on documents created in the last 7 days.
        """
        
        try:
            if await self.create_agent(task):
                result = await self.agent.run()
                logger.info("Document download completed")
                return True
        except Exception as e:
            logger.error(f"Document download failed: {e}")
            return False

    async def run_daily_automation(self):
        """Run the complete daily automation workflow"""
        logger.info("Starting daily AppFolio automation")
        
        # Initialize browser
        if not await self.initialize_browser():
            return False
        
        try:
            # Step 1: Login to AppFolio
            logger.info("Step 1: Logging into AppFolio")
            if not await self.login_to_appfolio():
                logger.error("Login failed, stopping automation")
                return False
            
            # Step 1.5: Handle password save popup
            logger.info("Step 1.5: Handling password save popup")
            await self.handle_password_save_popup()
            
            # Step 2: Handle 2FA manually
            logger.info("Step 2: Handling 2FA authentication")
            if not await self.handle_2fa_manually():
                logger.error("2FA handling failed, stopping automation")
                return False
            
            # Step 3: Download ledger report
            logger.info("Step 3: Downloading ledger report")
            await self.download_ledger_report()
            
            # Step 4: Download new documents
            logger.info("Step 4: Downloading new documents")
            await self.download_documents()
            
            logger.info("Daily automation completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Automation failed: {e}")
            return False
        finally:
            # Browser cleanup is handled automatically by browser-use
            logger.info("🔄 Browser session completed")

    async def test_login_only(self):
        """Test login functionality with 2FA handling"""
        logger.info("Testing AppFolio login with 2FA")
        
        if not await self.initialize_browser():
            return False
        
        try:
            # Step 1: Login to AppFolio
            success = await self.login_to_appfolio()
            if not success:
                logger.error("Login test failed")
                return False
            
            # Step 1.5: Handle password save popup
            await self.handle_password_save_popup()
            
            # Step 2: Handle 2FA manually
            success = await self.handle_2fa_manually()
            if success:
                logger.info("Login and 2FA test successful")
            else:
                logger.error("2FA handling failed")
            return success
        finally:
            # Browser cleanup is handled automatically by browser-use
            logger.info("🔄 Browser session completed")


async def main():
    """Main function to run the automation"""
    automator = AppFolioAutomator()
    
    # Check if this is a test run
    if len(sys.argv) > 1 and sys.argv[1] == "--test-login":
        await automator.test_login_only()
    else:
        await automator.run_daily_automation()


if __name__ == "__main__":
    # Check if required environment variables are set
    if not AI_CONFIG["gemini_api_key"] and not AI_CONFIG["openai_api_key"]:
        print("❌ Error: No AI API key configured.")
        print("Please set either GEMINI_API_KEY or OPENAI_API_KEY in your .env file")
        print("You can get a free Gemini API key at: https://makersuite.google.com/app/apikey")
        sys.exit(1)
    
    if not APPFOLIO_CONFIG["username"] or not APPFOLIO_CONFIG["password"]:
        print("❌ Error: AppFolio credentials not configured.")
        print("Please set APPFOLIO_EMAIL, APPFOLIO_PASSWORD, and APPFOLIO_URL in your .env file")
        sys.exit(1)
    
    print("🚀 Starting AppFolio Automation System")
    print("📝 Check logs folder for detailed execution logs")
    
    asyncio.run(main())