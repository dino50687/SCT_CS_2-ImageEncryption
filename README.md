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
Divides image into blocks and shuffles them.

```bash
python cli.py encrypt input.jpg encrypted.jpg --method block_swap --block-size 8 --seed 42
python cli.py decrypt encrypted.jpg decrypted.jpg --method block_swap --block-size 8 --seed 42
```

**Parameters:**
- `--block-size`: Size of square blocks (default: 4)
- `--seed`: Random seed for reproducible block shuffling

**Reversibility:** ⚠️ Requires exact same parameters and seed

### 7. Color Channel Shifting (`channel_shift`)
Shifts RGB color channels (e.g., R->G, G->B, B->R).

```bash
python cli.py encrypt input.jpg encrypted.jpg --method channel_shift --shift 1
python cli.py decrypt encrypted.jpg decrypted.jpg --method channel_shift --shift 1
```

**Parameters:**
- `--shift`: Shift amount (1 or 2, default: 1)

**Reversibility:** ✅ Fully reversible

## Python API Usage

You can also use the encryption tool directly in your Python code:

```python
from image_encryptor import ImageEncryptor

encryptor = ImageEncryptor()

# XOR encryption
encryptor.encrypt('input.jpg', 'encrypted.jpg', method='xor', key=150)
encryptor.decrypt('encrypted.jpg', 'decrypted.jpg', method='xor', key=150)

# Arithmetic operations
encryptor.encrypt('input.jpg', 'encrypted.jpg', 
                  method='arithmetic', operation='add', value=75)
encryptor.decrypt('encrypted.jpg', 'decrypted.jpg',
                  method='arithmetic', operation='add', value=75)

# Random pixel swapping
encryptor.encrypt('input.jpg', 'encrypted.jpg',
                  method='random_swap', swap_percentage=0.5, seed=42)
encryptor.decrypt('encrypted.jpg', 'decrypted.jpg',
                  method='random_swap', swap_percentage=0.5, seed=42)
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

**"No module named 'PIL'"**
```bash
pip install Pillow
```

**"No module named 'numpy'"**
```bash
pip install numpy
```

**"Input file not found"**
Make sure the input image path is correct and the file exists.

**"Invalid image format"**
Ensure your image is in a supported format (JPEG, PNG, BMP, TIFF).

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new encryption methods
- Improve documentation
- Submit pull requests

## License

This project is provided as-is for educational purposes. Feel free to modify and distribute according to your needs.