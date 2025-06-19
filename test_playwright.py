#!/usr/bin/env python3
"""
Test script to verify Playwright is working in container environment
"""
import asyncio
from playwright.async_api import async_playwright

async def test_playwright():
    """Test Playwright browser launch"""
    try:
        print("🔧 Testing Playwright browser launch...")
        
        async with async_playwright() as p:
            print("✅ Playwright context created successfully")
            
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu'
                ]
            )
            print("✅ Browser launched successfully")
            
            context = await browser.new_context(
                viewport={'width': 850, 'height': 800},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
            print("✅ Browser context created successfully")
            
            page = await context.new_page()
            print("✅ New page created successfully")
            
            # Test a simple page load
            await page.goto("https://www.google.com")
            title = await page.title()
            print(f"✅ Page loaded successfully. Title: {title}")
            
            await browser.close()
            print("✅ Browser closed successfully")
            
        print("✅ All Playwright tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Playwright test failed: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    asyncio.run(test_playwright()) 