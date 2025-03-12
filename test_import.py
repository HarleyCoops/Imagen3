"""
Test script to check the import of the google-generativeai package.
"""

print("Testing imports...")

try:
    import google.generativeai
    print("✓ import google.generativeai works")
except ImportError as e:
    print(f"✗ import google.generativeai failed: {e}")

try:
    from google import generativeai
    print("✓ from google import generativeai works")
except ImportError as e:
    print(f"✗ from google import generativeai failed: {e}")

try:
    from google import genai
    print("✓ from google import genai works")
except ImportError as e:
    print(f"✗ from google import genai failed: {e}")

print("\nDone testing imports.")
