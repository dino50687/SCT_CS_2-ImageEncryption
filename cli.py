#!/usr/bin/env python3
"""
Command-line interface for the Image Encryption Tool

This script provides an easy-to-use CLI for encrypting and decrypting images
using various pixel manipulation techniques.
"""

import argparse
import sys
import os
from image_encryptor import ImageEncryptor


def main():
    parser = argparse.ArgumentParser(
        description="Image Encryption Tool - Encrypt and decrypt images using pixel manipulation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # XOR encryption with default key (123)
  python cli.py encrypt input.jpg encrypted.jpg --method xor
  
  # XOR encryption with custom key
  python cli.py encrypt input.jpg encrypted.jpg --method xor --key 200
  
  # Arithmetic encryption (add 50 to each pixel)
  python cli.py encrypt input.jpg encrypted.jpg --method arithmetic --operation add --value 50
  
  # Random pixel swapping (50% of pixels)
  python cli.py encrypt input.jpg encrypted.jpg --method random_swap --swap-percentage 0.5
  
  # Block-based pixel swapping
  python cli.py encrypt input.jpg encrypted.jpg --method block_swap --block-size 4
  
  # Bit shifting encryption
  python cli.py encrypt input.jpg encrypted.jpg --method bit_shift --shift-amount 3 --direction left
  
  # Decrypt (use same parameters as encryption)
  python cli.py decrypt encrypted.jpg decrypted.jpg --method xor --key 200
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt an image')
    encrypt_parser.add_argument('input', help='Path to input image')
    encrypt_parser.add_argument('output', help='Path to save encrypted image')
    encrypt_parser.add_argument('--method', choices=[
        'xor', 'arithmetic', 'bit_shift', 'adjacent_swap', 
        'random_swap', 'block_swap', 'channel_shift'
    ], default='xor', help='Encryption method (default: xor)')
    
    # Method-specific arguments
    encrypt_parser.add_argument('--key', type=int, default=123, 
                              help='XOR key (0-255, default: 123)')
    encrypt_parser.add_argument('--operation', choices=['add', 'subtract', 'multiply', 'divide'], 
                              default='add', help='Arithmetic operation (default: add)')
    encrypt_parser.add_argument('--value', type=int, default=50, 
                              help='Value for arithmetic operations (default: 50)')
    encrypt_parser.add_argument('--shift-amount', type=int, default=2, 
                              help='Number of bits to shift (default: 2)')
    encrypt_parser.add_argument('--direction', choices=['left', 'right'], default='left',
                              help='Bit shift direction (default: left)')
    encrypt_parser.add_argument('--swap-percentage', type=float, default=0.5,
                              help='Percentage of pixels to swap (0.0-1.0, default: 0.5)')
    encrypt_parser.add_argument('--block-size', type=int, default=2,
                              help='Block size for block swap (default: 2)')
    encrypt_parser.add_argument('--seed', type=int, help='Random seed for reproducible results')
    
    # Decrypt command
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt an image')
    decrypt_parser.add_argument('input', help='Path to encrypted image')
    decrypt_parser.add_argument('output', help='Path to save decrypted image')
    decrypt_parser.add_argument('--method', choices=[
        'xor', 'arithmetic', 'bit_shift', 'adjacent_swap', 
        'random_swap', 'block_swap', 'channel_shift'
    ], default='xor', help='Decryption method (must match encryption method)')
    
    # Same method-specific arguments for decryption
    decrypt_parser.add_argument('--key', type=int, default=123, 
                              help='XOR key used for encryption (0-255, default: 123)')
    decrypt_parser.add_argument('--operation', choices=['add', 'subtract', 'multiply', 'divide'], 
                              default='add', help='Arithmetic operation used for encryption')
    decrypt_parser.add_argument('--value', type=int, default=50, 
                              help='Value used for arithmetic operations during encryption')
    decrypt_parser.add_argument('--shift-amount', type=int, default=2, 
                              help='Number of bits shifted during encryption')
    decrypt_parser.add_argument('--direction', choices=['left', 'right'], default='left',
                              help='Bit shift direction used during encryption')
    decrypt_parser.add_argument('--swap-percentage', type=float, default=0.5,
                              help='Percentage of pixels swapped during encryption')
    decrypt_parser.add_argument('--block-size', type=int, default=2,
                              help='Block size used during encryption')
    decrypt_parser.add_argument('--seed', type=int, help='Random seed used for encryption')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run demonstration with a sample image')
    demo_parser.add_argument('--input', help='Path to input image (will create sample if not provided)')
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return
    
    try:
        if args.command == 'encrypt':
            encrypt_image(args)
        elif args.command == 'decrypt':
            decrypt_image(args)
        elif args.command == 'demo':
            run_demo(args)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def encrypt_image(args):
    """Handle image encryption"""
    # Check if input file exists
    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Input file not found: {args.input}")
    
    # Create encryptor
    encryptor = ImageEncryptor(seed=args.seed)
    
    # Prepare kwargs based on method
    kwargs = {}
    if args.method == 'xor':
        kwargs['key'] = args.key
    elif args.method == 'arithmetic':
        kwargs['operation'] = args.operation
        kwargs['value'] = args.value
    elif args.method == 'bit_shift':
        kwargs['shift_amount'] = args.shift_amount
        kwargs['direction'] = args.direction
    elif args.method == 'random_swap':
        kwargs['swap_percentage'] = args.swap_percentage
    elif args.method == 'block_swap':
        kwargs['block_size'] = args.block_size
    
    # Encrypt image
    encryptor.encrypt_image(args.input, args.output, args.method, **kwargs)


def decrypt_image(args):
    """Handle image decryption"""
    # Check if input file exists
    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Encrypted file not found: {args.input}")
    
    # Create encryptor
    encryptor = ImageEncryptor(seed=args.seed)
    
    # Prepare kwargs based on method
    kwargs = {}
    if args.method == 'xor':
        kwargs['key'] = args.key
    elif args.method == 'arithmetic':
        kwargs['operation'] = args.operation
        kwargs['value'] = args.value
    elif args.method == 'bit_shift':
        kwargs['shift_amount'] = args.shift_amount
        kwargs['direction'] = args.direction
    elif args.method == 'random_swap':
        kwargs['swap_percentage'] = args.swap_percentage
    elif args.method == 'block_swap':
        kwargs['block_size'] = args.block_size
    
    # Decrypt image
    encryptor.decrypt_image(args.input, args.output, args.method, **kwargs)


def run_demo(args):
    """Run a demonstration with different encryption methods"""
    import numpy as np
    from PIL import Image
    
    # Create or use provided input image
    if args.input and os.path.exists(args.input):
        input_image = args.input
        print(f"Using provided image: {input_image}")
    else:
        # Create a simple test image
        input_image = "sample_input.jpg"
        print("Creating sample image for demonstration...")
        
        # Create a colorful test image
        width, height = 200, 200
        image_array = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Create gradient patterns
        for i in range(height):
            for j in range(width):
                image_array[i, j] = [
                    (i * 255) // height,  # Red gradient
                    (j * 255) // width,   # Green gradient  
                    ((i + j) * 255) // (height + width)  # Blue gradient
                ]
        
        # Save sample image
        sample_image = Image.fromarray(image_array, 'RGB')
        sample_image.save(input_image)
        print(f"Sample image created: {input_image}")
    
    # Demo different encryption methods
    methods_to_demo = [
        ('xor', {'key': 150}),
        ('arithmetic', {'operation': 'add', 'value': 75}),
        ('bit_shift', {'shift_amount': 3, 'direction': 'left'}),
        ('adjacent_swap', {}),
        ('random_swap', {'swap_percentage': 0.3}),
        ('block_swap', {'block_size': 4}),
        ('channel_shift', {})
    ]
    
    encryptor = ImageEncryptor(seed=42)  # Fixed seed for reproducible demo
    
    print(f"\nRunning demonstration with {len(methods_to_demo)} encryption methods:")
    print("=" * 60)
    
    for method, kwargs in methods_to_demo:
        encrypted_file = f"demo_encrypted_{method}.jpg"
        decrypted_file = f"demo_decrypted_{method}.jpg"
        
        print(f"\n{method.upper()} Method:")
        print(f"  Parameters: {kwargs}")
        
        try:
            # Encrypt
            encryptor.encrypt_image(input_image, encrypted_file, method, **kwargs)
            
            # Decrypt (for reversible methods)
            if method in ['xor', 'arithmetic', 'bit_shift', 'adjacent_swap', 'channel_shift']:
                encryptor.decrypt_image(encrypted_file, decrypted_file, method, **kwargs)
                print(f"  Decrypted: {decrypted_file}")
            else:
                print(f"  Note: {method} requires same random seed for exact reversal")
        
        except Exception as e:
            print(f"  Error with {method}: {e}")
    
    print(f"\nDemo complete! Check the generated files in the current directory.")
    print("Original:", input_image)
    print("Encrypted files: demo_encrypted_*.jpg")
    print("Decrypted files: demo_decrypted_*.jpg")


if __name__ == '__main__':
    main()