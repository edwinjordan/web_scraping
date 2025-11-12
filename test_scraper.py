"""
Test script for tokopedia_scraper.py
Verifies that all functions are properly defined and can be imported.
"""

import sys
import inspect

# Import the scraper module
import tokopedia_scraper

def test_functions_exist():
    """Test that all required functions are defined"""
    required_functions = ['init_driver', 'scrape_data', 'save_to_csv', 'main']
    
    print("Testing function definitions...")
    for func_name in required_functions:
        if hasattr(tokopedia_scraper, func_name):
            func = getattr(tokopedia_scraper, func_name)
            if callable(func):
                print(f"✓ {func_name} is defined and callable")
            else:
                print(f"✗ {func_name} exists but is not callable")
                sys.exit(1)
        else:
            print(f"✗ {func_name} is not defined")
            sys.exit(1)
    
    print("\nAll required functions are properly defined!")

def test_function_signatures():
    """Test that functions have correct parameters"""
    print("\nTesting function signatures...")
    
    # Test init_driver
    sig = inspect.signature(tokopedia_scraper.init_driver)
    print(f"✓ init_driver() signature: {sig}")
    
    # Test scrape_data
    sig = inspect.signature(tokopedia_scraper.scrape_data)
    params = list(sig.parameters.keys())
    assert 'driver' in params, "scrape_data must have 'driver' parameter"
    assert 'url' in params, "scrape_data must have 'url' parameter"
    print(f"✓ scrape_data() signature: {sig}")
    
    # Test save_to_csv
    sig = inspect.signature(tokopedia_scraper.save_to_csv)
    params = list(sig.parameters.keys())
    assert 'data' in params, "save_to_csv must have 'data' parameter"
    print(f"✓ save_to_csv() signature: {sig}")
    
    # Test main
    sig = inspect.signature(tokopedia_scraper.main)
    print(f"✓ main() signature: {sig}")
    
    print("\nAll function signatures are correct!")

def test_imports():
    """Test that all required imports are present"""
    print("\nTesting imports...")
    
    required_imports = [
        ('time', 'time'),
        ('csv', 'csv'),
        ('selenium.webdriver', 'webdriver'),
        ('selenium.webdriver.chrome.service', 'Service'),
        ('selenium.webdriver.chrome.options', 'Options'),
    ]
    
    for module_name, obj_name in required_imports:
        try:
            __import__(module_name)
            print(f"✓ {module_name} can be imported")
        except ImportError as e:
            print(f"✗ Failed to import {module_name}: {e}")
            sys.exit(1)
    
    print("\nAll required imports are available!")

if __name__ == "__main__":
    print("=" * 60)
    print("Tokopedia Scraper - Unit Tests")
    print("=" * 60)
    
    try:
        test_imports()
        test_functions_exist()
        test_function_signatures()
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
    
    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        sys.exit(1)
