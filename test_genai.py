"""
Test script to check the available attributes in the google.generativeai module.
"""

import google.generativeai as genai

print("Available attributes in google.generativeai:")
for attr in dir(genai):
    if not attr.startswith('_'):  # Skip private attributes
        print(f"- {attr}")

print("\nChecking for configure method:")
if hasattr(genai, 'configure'):
    print("✓ genai.configure exists")
else:
    print("✗ genai.configure does not exist")

print("\nChecking for Client class:")
if hasattr(genai, 'Client'):
    print("✓ genai.Client exists")
else:
    print("✗ genai.Client does not exist")

print("\nChecking genai version:")
if hasattr(genai, '__version__'):
    print(f"genai version: {genai.__version__}")
else:
    print("genai version not available")
