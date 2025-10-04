"""
Test script to verify browser-use setup and basic functionality
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_browser_use():
    """Test basic browser-use functionality"""
    print("🧪 Testing browser-use setup...")
    
    try:
        from browser_use import Agent, Browser
        print("✅ browser-use imported successfully")
        
        # Check if we have an API key
        gemini_key = os.getenv("GEMINI_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if not gemini_key and not openai_key:
            print("❌ No AI API key found. Please add GEMINI_API_KEY or OPENAI_API_KEY to your .env file")
            print("💡 You can get a free Gemini API key at: https://makersuite.google.com/app/apikey")
            return False
        
        # Test browser initialization
        print("🌐 Testing browser initialization...")
        try:
            # Try to connect to existing Chrome first
            browser = Browser(
                headless=False,
                connect_to_browser=True,
                debugging_port=9222
            )
            print("✅ Connected to existing Chrome browser")
        except:
            # Fallback to new browser instance
            browser = Browser(
                headless=False,
                executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            )
            print("✅ Created new browser instance")
        
        # Test AI model initialization
        if gemini_key:
            from browser_use import ChatGoogle
            llm = ChatGoogle(model="gemini-flash-latest", api_key=gemini_key)
            print("✅ Gemini AI model initialized")
        elif openai_key:
            from browser_use import ChatOpenAI
            llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_key)
            print("✅ OpenAI model initialized")
        
        # Create a simple test agent
        agent = Agent(
            task="Navigate to https://example.com and get the page title",
            llm=llm,
            browser=browser
        )
        print("✅ Agent created successfully")
        
        # Run a simple test
        print("🚀 Running simple navigation test...")
        result = await agent.run()
        print("✅ Test completed successfully!")
        
        await browser.close()
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🔧 AppFolio Automation Setup Test")
    print("=" * 40)
    
    # Test browser-use
    success = await test_browser_use()
    
    if success:
        print("\n🎉 Setup test completed successfully!")
        print("📝 Next steps:")
        print("1. Copy .env.example to .env and add your credentials")
        print("2. Run: python3 scripts/appfolio_automation.py --test-login")
        print("3. If login test works, run full automation")
    else:
        print("\n❌ Setup test failed. Please check the errors above.")

if __name__ == "__main__":
    asyncio.run(main())