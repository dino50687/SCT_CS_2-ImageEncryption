# Image Encryption Tool

A simple yet powerful image encryption tool that uses pixel manipulation techniques to encrypt and decrypt images. This tool supports various encryption methods including mathematical operations and pixel swapping algorithms.

## Features

- **Multiple Encryption Methods:**
  - XOR encryption with customizable keys
  - Arithmetic operations (add, subtract, multiply, divide)
  - Bit shifting (left/right)
  - Pixel swapping (adjacent, random, block-based)
  - Color channel shifting

- **Easy-to-Use CLI:** Command-line interface with comprehensive options
- **Reversible Operations:** Most methods support decryption to recover original images
- **Customizable Parameters:** Fine-tune encryption strength and behavior
- **Demo Mode:** Built-in demonstration with sample images

## Installation

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install Pillow numpy
```

## Quick Start

### Basic Usage

```bash
# Encrypt an image using XOR (default method)
python cli.py encrypt input.jpg encrypted.jpg

# Decrypt the image
python cli.py decrypt encrypted.jpg decrypted.jpg

# Run demonstration with all methods
python cli.py demo
```

### Advanced Usage

```bash
# XOR encryption with custom key
python cli.py encrypt input.jpg encrypted.jpg --method xor --key 200

# Arithmetic encryption (add 75 to each pixel)
python cli.py encrypt input.jpg encrypted.jpg --method arithmetic --operation add --value 75

# Random pixel swapping (30% of pixels)
python cli.py encrypt input.jpg encrypted.jpg --method random_swap --swap-percentage 0.3 --seed 42

# Block-based pixel swapping with 4x4 blocks
python cli.py encrypt input.jpg encrypted.jpg --method block_swap --block-size 4

# Bit shifting (left shift by 3 bits)
python cli.py encrypt input.jpg encrypted.jpg --method bit_shift --shift-amount 3 --direction left
```

## Encryption Methods

### 1. XOR Encryption (`xor`)
Applies XOR operation to each pixel value using a secret key.

```bash
python cli.py encrypt input.jpg encrypted.jpg --method xor --key 150
python cli.py decrypt encrypted.jpg decrypted.jpg --method xor --key 150
```

**Parameters:**
- `--key`: XOR key (0-255, default: 123)

**Reversibility:** ✅ Fully reversible

### 2. Arithmetic Operations (`arithmetic`)
Applies mathematical operations to pixel values.

```bash
# Addition
python cli.py encrypt input.jpg encrypted.jpg --method arithmetic --operation add --value 50

# Subtraction  
python cli.py encrypt input.jpg encrypted.jpg --method arithmetic --operation subtract --value 30

# Multiplication
python cli.py encrypt input.jpg encrypted.jpg --method arithmetic --operation multiply --value 2
```

**Parameters:**
- `--operation`: add, subtract, multiply, divide (default: add)
- `--value`: Value for the operation (default: 50)

**Reversibility:** ✅ Fully reversible (automatically reverses the operation)

### 3. Bit Shifting (`bit_shift`)
Shifts bits of pixel values left or right.

```bash
python cli.py encrypt input.jpg encrypted.jpg --method bit_shift --shift-amount 2 --direction left
python cli.py decrypt encrypted.jpg decrypted.jpg --method bit_shift --shift-amount 2 --direction left
```

**Parameters:**
- `--shift-amount`: Number of bits to shift (default: 2)
- `--direction`: left or right (default: left)

**Reversibility:** ✅ Fully reversible

### 4. Adjacent Pixel Swapping (`adjacent_swap`)
Swaps adjacent pixels horizontally in pairs.

```bash
python cli.py encrypt input.jpg encrypted.jpg --method adjacent_swap
python cli.py decrypt encrypted.jpg decrypted.jpg --method adjacent_swap
```

**Parameters:** None

**Reversibility:** ✅ Fully reversible (operation is its own inverse)

### 5. Random Pixel Swapping (`random_swap`)
Randomly swaps pixel positions in the image.

```bash
python cli.py encrypt input.jpg encrypted.jpg --method random_swap --swap-percentage 0.5 --seed 42
python cli.py decrypt encrypted.jpg decrypted.jpg --method random_swap --swap-percentage 0.5 --seed 42
```

**Parameters:**
- `--swap-percentage`: Percentage of pixels to swap (0.0-1.0, default: 0.5)
- `--seed`: Random seed for reproducible results (important for decryption)

**Reversibility:** ⚠️ Requires exact same parameters and seed

### 6. Block Pixel Swapping (`block_swap`)
Shuffles pixels within blocks of specified size.

```bash
python cli.py encrypt input.jpg encrypted.jpg --method block_swap --block-size 4 --seed 42
python cli.py decrypt encrypted.jpg decrypted.jpg --method block_swap --block-size 4 --seed 42
```

**Parameters:**
- `--block-size`: Size of blocks (default: 2)
- `--seed`: Random seed for reproducible results

**Reversibility:** ⚠️ Requires exact same parameters and seed

### 7. Color Channel Shifting (`channel_shift`)
Shifts RGB color channels (R→G, G→B, B→R).

```bash
python cli.py encrypt input.jpg encrypted.jpg --method channel_shift
python cli.py decrypt encrypted.jpg decrypted.jpg --method channel_shift
```

**Parameters:** None

**Reversibility:** ✅ Fully reversible

## Python API Usage

You can also use the tool programmatically:

```python
from image_encryptor import ImageEncryptor

# Create encryptor instance
encryptor = ImageEncryptor(seed=42)

# Encrypt using XOR
encryptor.encrypt_image(
    'input.jpg', 
    'encrypted.jpg', 
    method='xor', 
    key=150
)

# Decrypt
encryptor.decrypt_image(
    'encrypted.jpg', 
    'decrypted.jpg', 
    method='xor', 
    key=150
)

# Use different methods
encryptor.encrypt_image(
    'input.jpg', 
    'encrypted_random.jpg', 
    method='random_swap', 
    swap_percentage=0.3
)
```

## Examples and Demo

Run the built-in demonstration to see all encryption methods in action:

```bash
python cli.py demo
```

This will:
1. Create a sample colorful test image
2. Apply all encryption methods with different parameters
3. Generate encrypted and decrypted versions
4. Show you the results

You can also provide your own image for the demo:

```bash
python cli.py demo --input your_image.jpg
```

## Security Notes

⚠️ **Important:** This tool is designed for educational purposes and basic image obfuscation. It is **not suitable for securing sensitive data** as:

1. The encryption methods are relatively simple and can be reverse-engineered
2. Some methods don't provide cryptographic security
3. Image metadata might not be encrypted
4. Statistical analysis could potentially reveal patterns

For actual security applications, use established cryptographic libraries and methods.

## Technical Details

### Supported Image Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)  
- BMP (.bmp)
- TIFF (.tiff)
- And other formats supported by PIL/Pillow

### Image Processing
- All images are converted to RGB format internally
- Pixel values are kept within valid range [0, 255]
- Output images maintain the same dimensions as input

### Dependencies
- **Pillow (PIL)**: Image loading, saving, and basic operations
- **NumPy**: Efficient array operations for pixel manipulation

## Troubleshooting

### Common Issues

**"Error loading image"**
- Check if the file path is correct
- Ensure the image format is supported
- Verify the file isn't corrupted

**"Decryption doesn't match original"**
- For random-based methods, ensure you use the same `--seed` value
- Verify all parameters match those used during encryption
- Check that the encryption method is correctly reversible

**"Memory issues with large images"**
- The tool loads entire images into memory
- For very large images, consider resizing them first
- Close other applications to free up RAM

### Performance Tips
- Use smaller block sizes for `block_swap` on large images
- Lower `swap_percentage` values process faster
- XOR and arithmetic methods are generally fastest

## Contributing

Feel free to extend this tool with additional encryption methods or improvements:

1. Add new methods to the `ImageEncryptor` class
2. Update the CLI to support new parameters
3. Add appropriate documentation
4. Test with various image types and sizes

## License

This project is provided as-is for educational purposes. Feel free to modify and distribute according to your needs.