#!/usr/bin/env python3
"""
Example usage of the Image Encryption Tool

This script demonstrates how to use the ImageEncryptor class directly
for various encryption and decryption operations.
"""

import os
import numpy as np
from PIL import Image
from image_encryptor import ImageEncryptor


def create_sample_image(filename="example_input.jpg", size=(300, 300)):
    """Create a sample image for testing"""
    print(f"Creating sample image: {filename}")
    
    width, height = size
    image_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Create a more interesting pattern
    for i in range(height):
        for j in range(width):
            # Create geometric patterns
            r = int(128 + 127 * np.sin(i * 0.1) * np.cos(j * 0.1))
            g = int(128 + 127 * np.sin((i + j) * 0.05))
            b = int(128 + 127 * np.cos(i * 0.08) * np.sin(j * 0.08))
            
            image_array[i, j] = [r, g, b]
    
    # Add some geometric shapes
    # Add a circle
    center_x, center_y = width // 2, height // 2
    radius = min(width, height) // 4
    
    for i in range(height):
        for j in range(width):
            distance = np.sqrt((i - center_y)**2 + (j - center_x)**2)
            if distance < radius:
                image_array[i, j] = [255, 255, 255]  # White circle
            elif distance < radius + 10:
                image_array[i, j] = [0, 0, 0]  # Black border
    
    # Save image
    sample_image = Image.fromarray(image_array, 'RGB')
    sample_image.save(filename)
    print(f"Sample image saved: {filename}")
    return filename


def demonstrate_encryption_methods():
    """Demonstrate different encryption methods"""
    
    # Create sample image
    input_image = create_sample_image()
    
    # Initialize encryptor with a seed for reproducible results
    encryptor = ImageEncryptor(seed=12345)
    
    print("\n" + "="*60)
    print("DEMONSTRATING DIFFERENT ENCRYPTION METHODS")
    print("="*60)
    
    # 1. XOR Encryption
    print("\n1. XOR ENCRYPTION")
    print("-" * 20)
    
    xor_encrypted = "example_xor_encrypted.jpg"
    xor_decrypted = "example_xor_decrypted.jpg"
    
    encryptor.encrypt_image(input_image, xor_encrypted, method='xor', key=200)
    encryptor.decrypt_image(xor_encrypted, xor_decrypted, method='xor', key=200)
    
    print("✓ XOR encryption and decryption completed")
    
    # 2. Arithmetic Operations
    print("\n2. ARITHMETIC OPERATIONS")
    print("-" * 25)
    
    for operation in ['add', 'subtract', 'multiply']:
        encrypted_file = f"example_arithmetic_{operation}_encrypted.jpg"
        decrypted_file = f"example_arithmetic_{operation}_decrypted.jpg"
        
        value = 50 if operation in ['add', 'subtract'] else 2
        
        encryptor.encrypt_image(input_image, encrypted_file, 
                              method='arithmetic', operation=operation, value=value)
        encryptor.decrypt_image(encrypted_file, decrypted_file, 
                              method='arithmetic', operation=operation, value=value)
        
        print(f"✓ Arithmetic {operation} encryption and decryption completed")
    
    # 3. Bit Shifting
    print("\n3. BIT SHIFTING")
    print("-" * 15)
    
    for direction in ['left', 'right']:
        encrypted_file = f"example_bitshift_{direction}_encrypted.jpg"
        decrypted_file = f"example_bitshift_{direction}_decrypted.jpg"
        
        encryptor.encrypt_image(input_image, encrypted_file, 
                              method='bit_shift', shift_amount=3, direction=direction)
        encryptor.decrypt_image(encrypted_file, decrypted_file, 
                              method='bit_shift', shift_amount=3, direction=direction)
        
        print(f"✓ Bit shift {direction} encryption and decryption completed")
    
    # 4. Pixel Swapping Methods
    print("\n4. PIXEL SWAPPING METHODS")
    print("-" * 25)
    
    # Adjacent swap
    adj_encrypted = "example_adjacent_encrypted.jpg"
    adj_decrypted = "example_adjacent_decrypted.jpg"
    
    encryptor.encrypt_image(input_image, adj_encrypted, method='adjacent_swap')
    encryptor.decrypt_image(adj_encrypted, adj_decrypted, method='adjacent_swap')
    print("✓ Adjacent pixel swap encryption and decryption completed")
    
    # Random swap
    random_encrypted = "example_random_encrypted.jpg"
    random_decrypted = "example_random_decrypted.jpg"
    
    encryptor.encrypt_image(input_image, random_encrypted, 
                          method='random_swap', swap_percentage=0.4)
    encryptor.decrypt_image(random_encrypted, random_decrypted, 
                          method='random_swap', swap_percentage=0.4)
    print("✓ Random pixel swap encryption and decryption completed")
    
    # Block swap
    block_encrypted = "example_block_encrypted.jpg"
    block_decrypted = "example_block_decrypted.jpg"
    
    encryptor.encrypt_image(input_image, block_encrypted, 
                          method='block_swap', block_size=5)
    encryptor.decrypt_image(block_encrypted, block_decrypted, 
                          method='block_swap', block_size=5)
    print("✓ Block pixel swap encryption and decryption completed")
    
    # 5. Color Channel Shifting
    print("\n5. COLOR CHANNEL SHIFTING")
    print("-" * 25)
    
    channel_encrypted = "example_channel_encrypted.jpg"
    channel_decrypted = "example_channel_decrypted.jpg"
    
    encryptor.encrypt_image(input_image, channel_encrypted, method='channel_shift')
    encryptor.decrypt_image(channel_encrypted, channel_decrypted, method='channel_shift')
    print("✓ Color channel shift encryption and decryption completed")
    
    print(f"\n" + "="*60)
    print("DEMONSTRATION COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nGenerated files:")
    print(f"📁 Original image: {input_image}")
    print("📁 Encrypted images: example_*_encrypted.jpg")
    print("📁 Decrypted images: example_*_decrypted.jpg")
    print("\nYou can open these images to see the effects of different encryption methods.")


def demonstrate_api_usage():
    """Demonstrate direct API usage"""
    
    print("\n" + "="*60)
    print("DEMONSTRATING DIRECT API USAGE")
    print("="*60)
    
    # Create encryptor
    encryptor = ImageEncryptor(seed=54321)
    
    # Load an image manually
    input_image = "example_input.jpg"
    if not os.path.exists(input_image):
        input_image = create_sample_image()
    
    print(f"\nLoading image: {input_image}")
    image_array = encryptor.load_image(input_image)
    print(f"Image shape: {image_array.shape}")
    print(f"Image data type: {image_array.dtype}")
    
    # Apply individual transformations
    print("\nApplying individual transformations:")
    
    # XOR transformation
    xor_result = encryptor.xor_encrypt(image_array, key=128)
    encryptor.save_image(xor_result, "api_xor_result.jpg")
    print("✓ XOR transformation applied")
    
    # Arithmetic transformation
    add_result = encryptor.arithmetic_encrypt(image_array, operation='add', value=80)
    encryptor.save_image(add_result, "api_arithmetic_result.jpg")
    print("✓ Arithmetic transformation applied")
    
    # Pixel swap transformation
    swap_result = encryptor.swap_random_pixels(image_array, swap_percentage=0.6)
    encryptor.save_image(swap_result, "api_pixel_swap_result.jpg")
    print("✓ Pixel swap transformation applied")
    
    # Chain multiple transformations
    print("\nChaining multiple transformations:")
    
    # Start with original image
    chained_result = image_array.copy()
    
    # Apply XOR
    chained_result = encryptor.xor_encrypt(chained_result, key=100)
    print("  → Applied XOR encryption")
    
    # Apply bit shifting
    chained_result = encryptor.bit_shift_encrypt(chained_result, shift_amount=2, direction='left')
    print("  → Applied bit shifting")
    
    # Apply pixel swapping
    chained_result = encryptor.swap_adjacent_pixels(chained_result)
    print("  → Applied adjacent pixel swapping")
    
    # Save result
    encryptor.save_image(chained_result, "api_chained_result.jpg")
    print("✓ Chained transformations completed")
    
    # Reverse the transformations
    print("\nReversing transformations:")
    
    # Reverse adjacent pixel swapping
    reversed_result = encryptor.swap_adjacent_pixels(chained_result)
    print("  → Reversed adjacent pixel swapping")
    
    # Reverse bit shifting
    reversed_result = encryptor.bit_shift_encrypt(reversed_result, shift_amount=2, direction='right')
    print("  → Reversed bit shifting")
    
    # Reverse XOR
    reversed_result = encryptor.xor_encrypt(reversed_result, key=100)
    print("  → Reversed XOR encryption")
    
    # Save final result
    encryptor.save_image(reversed_result, "api_reversed_result.jpg")
    print("✓ Transformation reversal completed")
    
    print("\nAPI demonstration completed!")
    print("Generated files:")
    print("📁 api_xor_result.jpg - XOR transformation")
    print("📁 api_arithmetic_result.jpg - Arithmetic transformation")
    print("📁 api_pixel_swap_result.jpg - Pixel swap transformation")
    print("📁 api_chained_result.jpg - Multiple chained transformations")
    print("📁 api_reversed_result.jpg - Reversed transformations")


def main():
    """Run all demonstrations"""
    
    print("🖼️  IMAGE ENCRYPTION TOOL - EXAMPLES AND DEMONSTRATIONS")
    print("=" * 70)
    
    try:
        # Run method demonstrations
        demonstrate_encryption_methods()
        
        # Run API usage demonstrations
        demonstrate_api_usage()
        
        print(f"\n🎉 All demonstrations completed successfully!")
        print("\nNext steps:")
        print("1. Examine the generated encrypted and decrypted images")
        print("2. Try the CLI tool: python cli.py --help")
        print("3. Run the demo: python cli.py demo")
        print("4. Experiment with your own images!")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())