#!/usr/bin/env python3
"""
Quick test script for the Image Encryption Tool
Run this to verify the installation and basic functionality
"""

from PIL import Image
import numpy as np
from image_encryptor import ImageEncryptor
import os

def test_installation():
    """Test that all dependencies are installed"""
    print("Testing installation...")
    try:
        import PIL
        import numpy
        print("✓ All dependencies installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        return False

def test_basic_encryption():
    """Test basic encryption/decryption"""
    print("\nTesting basic encryption/decryption...")
    
    # Create a simple test image
    img_array = np.full((50, 50, 3), 100, dtype=np.uint8)
    img = Image.fromarray(img_array)
    img.save('_test_input.png')
    
    encryptor = ImageEncryptor()
    
    # Test XOR
    encryptor.encrypt('_test_input.png', '_test_enc.png', method='xor', key=123)
    encryptor.decrypt('_test_enc.png', '_test_dec.png', method='xor', key=123)
    
    original = np.array(Image.open('_test_input.png'))
    decrypted = np.array(Image.open('_test_dec.png'))
    
    success = np.array_equal(original, decrypted)
    
    # Cleanup
    for f in ['_test_input.png', '_test_enc.png', '_test_dec.png']:
        if os.path.exists(f):
            os.remove(f)
    
    if success:
        print("✓ Basic encryption/decryption works correctly")
    else:
        print("✗ Encryption/decryption failed")
    
    return success

def test_all_methods():
    """Test all encryption methods"""
    print("\nTesting all encryption methods...")
    
    # Create test image
    img_array = np.full((20, 20, 3), 50, dtype=np.uint8)
    img = Image.fromarray(img_array)
    img.save('_test_all.png')
    
    encryptor = ImageEncryptor()
    
    methods = [
        ('xor', {'key': 100}),
        ('arithmetic', {'operation': 'add', 'value': 30}),
        ('bit_shift', {'shift_amount': 1, 'direction': 'left'}),
        ('adjacent_swap', {}),
        ('random_swap', {'swap_percentage': 0.3, 'seed': 42}),
        ('block_swap', {'block_size': 4, 'seed': 42}),
        ('channel_shift', {'shift': 1}),
    ]
    
    all_passed = True
    for method, params in methods:
        try:
            encryptor.encrypt('_test_all.png', f'_test_{method}.png', method, **params)
            print(f"  ✓ {method:20s} - OK")
        except Exception as e:
            print(f"  ✗ {method:20s} - Error: {e}")
            all_passed = False
    
    # Cleanup
    if os.path.exists('_test_all.png'):
        os.remove('_test_all.png')
    for method, _ in methods:
        f = f'_test_{method}.png'
        if os.path.exists(f):
            os.remove(f)
    
    return all_passed

def main():
    print("="*60)
    print("IMAGE ENCRYPTION TOOL - TEST SUITE")
    print("="*60)
    
    tests = [
        test_installation,
        test_basic_encryption,
        test_all_methods,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "="*60)
    if all(results):
        print("✓ ALL TESTS PASSED!")
        print("The Image Encryption Tool is working correctly.")
    else:
        print("✗ SOME TESTS FAILED")
        print("Please check the error messages above.")
    print("="*60)

if __name__ == '__main__':
    main()
