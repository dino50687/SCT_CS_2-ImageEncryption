#!/usr/bin/env python3
"""
Image Encryption Tool - Command Line Interface
"""

import argparse
import sys
import os
from image_encryptor import ImageEncryptor
from PIL import Image
import numpy as np


def create_sample_image(output_path, width=200, height=200):
    """Create a colorful sample image for testing"""
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Create colorful pattern
    for y in range(height):
        for x in range(width):
            img_array[y, x] = [
                (x * 255 // width),
                (y * 255 // height),
                ((x + y) * 255 // (width + height))
            ]
    
    img = Image.fromarray(img_array, 'RGB')
    img.save(output_path)
    print(f"Sample image created: {output_path}")


def demo_mode(input_image=None):
    """Run demonstration of all encryption methods"""
    encryptor = ImageEncryptor()
    
    # Create or use provided sample image
    if input_image is None:
        input_image = "sample_image.jpg"
        create_sample_image(input_image)
    
    print("\n" + "="*50)
    print("IMAGE ENCRYPTION TOOL - DEMO MODE")
    print("="*50)
    
    methods = [
        ('xor', {'key': 150}, 'XOR Encryption'),
        ('arithmetic', {'operation': 'add', 'value': 75}, 'Arithmetic (Add)'),
        ('bit_shift', {'shift_amount': 3, 'direction': 'left'}, 'Bit Shift'),
        ('adjacent_swap', {}, 'Adjacent Pixel Swap'),
        ('random_swap', {'swap_percentage': 0.3, 'seed': 42}, 'Random Pixel Swap'),
        ('block_swap', {'block_size': 4, 'seed': 42}, 'Block Pixel Swap'),
        ('channel_shift', {'shift': 1}, 'Color Channel Shift'),
    ]
    
    for method, params, description in methods:
        print(f"\n{description}:")
        encrypted_path = f"demo_encrypted_{method}.jpg"
        decrypted_path = f"demo_decrypted_{method}.jpg"
        
        try:
            # Encrypt
            encryptor.encrypt(input_image, encrypted_path, method, **params)
            print(f"  ✓ Encrypted: {encrypted_path}")
            
            # Decrypt
            encryptor.decrypt(encrypted_path, decrypted_path, method, **params)
            print(f"  ✓ Decrypted: {decrypted_path}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("\n" + "="*50)
    print("Demo complete! Check the generated files.")
    print("="*50 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Image Encryption Tool - Encrypt and decrypt images using pixel manipulation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s encrypt input.jpg encrypted.jpg
  %(prog)s decrypt encrypted.jpg decrypted.jpg
  %(prog)s encrypt input.jpg encrypted.jpg --method xor --key 200
  %(prog)s encrypt input.jpg encrypted.jpg --method arithmetic --operation add --value 75
  %(prog)s demo
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt an image')
    encrypt_parser.add_argument('input', help='Input image path')
    encrypt_parser.add_argument('output', help='Output encrypted image path')
    encrypt_parser.add_argument('--method', default='xor', 
                                choices=['xor', 'arithmetic', 'bit_shift', 'adjacent_swap', 
                                        'random_swap', 'block_swap', 'channel_shift'],
                                help='Encryption method (default: xor)')
    
    # XOR parameters
    encrypt_parser.add_argument('--key', type=int, default=123, 
                                help='XOR key (0-255, default: 123)')
    
    # Arithmetic parameters
    encrypt_parser.add_argument('--operation', default='add',
                                choices=['add', 'subtract', 'multiply', 'divide'],
                                help='Arithmetic operation (default: add)')
    encrypt_parser.add_argument('--value', type=int, default=50,
                                help='Value for arithmetic operation (default: 50)')
    
    # Bit shift parameters
    encrypt_parser.add_argument('--shift-amount', type=int, default=2,
                                help='Number of bits to shift (default: 2)')
    encrypt_parser.add_argument('--direction', default='left',
                                choices=['left', 'right'],
                                help='Shift direction (default: left)')
    
    # Random swap parameters
    encrypt_parser.add_argument('--swap-percentage', type=float, default=0.5,
                                help='Percentage of pixels to swap (0.0-1.0, default: 0.5)')
    encrypt_parser.add_argument('--seed', type=int, default=42,
                                help='Random seed for reproducible results (default: 42)')
    
    # Block swap parameters
    encrypt_parser.add_argument('--block-size', type=int, default=4,
                                help='Size of blocks for block swap (default: 4)')
    
    # Channel shift parameters
    encrypt_parser.add_argument('--shift', type=int, default=1,
                                choices=[1, 2],
                                help='Channel shift amount (default: 1)')
    
    # Decrypt command
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt an image')
    decrypt_parser.add_argument('input', help='Input encrypted image path')
    decrypt_parser.add_argument('output', help='Output decrypted image path')
    decrypt_parser.add_argument('--method', default='xor',
                                choices=['xor', 'arithmetic', 'bit_shift', 'adjacent_swap',
                                        'random_swap', 'block_swap', 'channel_shift'],
                                help='Decryption method (default: xor)')
    
    # Add same parameters for decrypt
    decrypt_parser.add_argument('--key', type=int, default=123)
    decrypt_parser.add_argument('--operation', default='add',
                                choices=['add', 'subtract', 'multiply', 'divide'])
    decrypt_parser.add_argument('--value', type=int, default=50)
    decrypt_parser.add_argument('--shift-amount', type=int, default=2)
    decrypt_parser.add_argument('--direction', default='left',
                                choices=['left', 'right'])
    decrypt_parser.add_argument('--swap-percentage', type=float, default=0.5)
    decrypt_parser.add_argument('--seed', type=int, default=42)
    decrypt_parser.add_argument('--block-size', type=int, default=4)
    decrypt_parser.add_argument('--shift', type=int, default=1, choices=[1, 2])
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run demonstration with all methods')
    demo_parser.add_argument('--input', help='Input image for demo (optional)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'demo':
        demo_mode(args.input)
        return
    
    # Validate input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found")
        sys.exit(1)
    
    # Prepare parameters
    params = {
        'key': args.key,
        'operation': args.operation,
        'value': args.value,
        'shift_amount': args.shift_amount,
        'direction': args.direction,
        'swap_percentage': args.swap_percentage,
        'seed': args.seed,
        'block_size': args.block_size,
        'shift': args.shift,
    }
    
    # Execute command
    encryptor = ImageEncryptor()
    
    try:
        if args.command == 'encrypt':
            print(f"Encrypting '{args.input}' -> '{args.output}' using {args.method} method...")
            encryptor.encrypt(args.input, args.output, args.method, **params)
            print(f"✓ Encryption successful! Output saved to: {args.output}")
        
        elif args.command == 'decrypt':
            print(f"Decrypting '{args.input}' -> '{args.output}' using {args.method} method...")
            encryptor.decrypt(args.input, args.output, args.method, **params)
            print(f"✓ Decryption successful! Output saved to: {args.output}")
    
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
