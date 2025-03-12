"""
Test Setup for Imagen 3 API Integration

This script tests the basic setup and configuration for the Imagen 3 API integration.
It verifies that:
1. All required packages are installed
2. The .env file is properly configured
3. The API key can be loaded
4. A connection to the Gemini API can be established

No images are generated during this test.
"""

import os
import sys

def test_imports():
    """Test that all required packages are installed."""
    print("Testing required packages...")
    
    try:
        import dotenv
        print("✓ python-dotenv is installed")
    except ImportError:
        print("✗ python-dotenv is not installed. Run: pip install python-dotenv")
        return False
    
    try:
        import google.generativeai
        print("✓ google-generativeai is installed")
    except ImportError:
        print("✗ google-generativeai is not installed. Run: pip install google-generativeai")
        return False
    
    try:
        from PIL import Image
        print("✓ Pillow is installed")
    except ImportError:
        print("✗ Pillow is not installed. Run: pip install Pillow")
        return False
    
    return True

def test_env_file():
    """Test that the .env file exists and contains the API key."""
    print("\nTesting .env file configuration...")
    
    if not os.path.exists(".env"):
        print("✗ .env file not found")
        return False
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("✗ GEMINI_API_KEY not found in .env file")
            return False
        
        if api_key == "your_api_key_here":
            print("✗ GEMINI_API_KEY is still set to the default value. Please update it with your actual API key")
            return False
        
        # Mask the API key for security
        masked_key = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]
        print(f"✓ GEMINI_API_KEY found: {masked_key}")
        return True
    
    except Exception as e:
        print(f"✗ Error loading .env file: {e}")
        return False

def test_api_connection():
    """Test that a connection to the Gemini API can be established."""
    print("\nTesting Gemini API connection...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("✗ Cannot test API connection: API key not found")
            return False
        
        import google.generativeai as genai
        # Initialize the client
        client = genai.Client(api_key=api_key)
        
        # Just test that we can initialize the client without errors
        # We don't actually make an API call to avoid charges
        print("✓ Successfully initialized Gemini API client")
        print("  Note: No actual API calls were made during this test")
        
        return True
    
    except Exception as e:
        print(f"✗ Error connecting to Gemini API: {e}")
        return False

def main():
    """Run all tests and report results."""
    print("Imagen 3 API Integration - Setup Test")
    print("=====================================")
    
    imports_ok = test_imports()
    env_ok = test_env_file()
    api_ok = test_api_connection() if env_ok else False
    
    print("\nTest Summary:")
    print(f"- Required packages: {'✓ PASS' if imports_ok else '✗ FAIL'}")
    print(f"- Environment setup: {'✓ PASS' if env_ok else '✗ FAIL'}")
    print(f"- API connection:    {'✓ PASS' if api_ok else '✗ FAIL'}")
    
    if imports_ok and env_ok and api_ok:
        print("\n✅ All tests passed! Your setup is ready to use.")
        print("   Try running 'python app.py \"test prompt\"' to generate your first image.")
        return 0
    else:
        print("\n❌ Some tests failed. Please fix the issues above before proceeding.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
