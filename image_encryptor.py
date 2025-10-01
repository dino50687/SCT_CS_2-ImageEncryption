"""
Image Encryption Tool - Core Module
Provides various pixel manipulation methods for image encryption/decryption
"""

import numpy as np
from PIL import Image
import random


class ImageEncryptor:
    """Main class for image encryption and decryption operations"""
    
    def __init__(self):
        pass
    
    def load_image(self, image_path):
        """Load an image and convert to RGB numpy array"""
        img = Image.open(image_path)
        img = img.convert('RGB')
        return np.array(img)
    
    def save_image(self, pixel_array, output_path):
        """Save numpy array as an image"""
        pixel_array = np.clip(pixel_array, 0, 255).astype(np.uint8)
        img = Image.fromarray(pixel_array, 'RGB')
        img.save(output_path)
    
    # Method 1: XOR Encryption
    def xor_encrypt(self, pixel_array, key=123):
        """Apply XOR operation to each pixel value"""
        return np.bitwise_xor(pixel_array, key)
    
    def xor_decrypt(self, pixel_array, key=123):
        """XOR is its own inverse"""
        return self.xor_encrypt(pixel_array, key)
    
    # Method 2: Arithmetic Operations
    def arithmetic_encrypt(self, pixel_array, operation='add', value=50):
        """Apply arithmetic operations to pixel values"""
        if operation == 'add':
            result = pixel_array.astype(np.int32) + value
        elif operation == 'subtract':
            result = pixel_array.astype(np.int32) - value
        elif operation == 'multiply':
            result = pixel_array.astype(np.int32) * value
        elif operation == 'divide':
            result = pixel_array.astype(np.int32) // value
        else:
            raise ValueError(f"Unknown operation: {operation}")
        
        return np.clip(result, 0, 255).astype(np.uint8)
    
    def arithmetic_decrypt(self, pixel_array, operation='add', value=50):
        """Reverse arithmetic operations"""
        if operation == 'add':
            return self.arithmetic_encrypt(pixel_array, 'subtract', value)
        elif operation == 'subtract':
            return self.arithmetic_encrypt(pixel_array, 'add', value)
        elif operation == 'multiply':
            return self.arithmetic_encrypt(pixel_array, 'divide', value)
        elif operation == 'divide':
            return self.arithmetic_encrypt(pixel_array, 'multiply', value)
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    # Method 3: Bit Shifting
    def bit_shift_encrypt(self, pixel_array, shift_amount=2, direction='left'):
        """Shift bits of pixel values"""
        if direction == 'left':
            result = np.left_shift(pixel_array.astype(np.int32), shift_amount)
        elif direction == 'right':
            result = np.right_shift(pixel_array.astype(np.int32), shift_amount)
        else:
            raise ValueError(f"Unknown direction: {direction}")
        
        return np.clip(result, 0, 255).astype(np.uint8)
    
    def bit_shift_decrypt(self, pixel_array, shift_amount=2, direction='left'):
        """Reverse bit shifting"""
        if direction == 'left':
            return self.bit_shift_encrypt(pixel_array, shift_amount, 'right')
        elif direction == 'right':
            return self.bit_shift_encrypt(pixel_array, shift_amount, 'left')
        else:
            raise ValueError(f"Unknown direction: {direction}")
    
    # Method 4: Adjacent Pixel Swapping
    def adjacent_swap_encrypt(self, pixel_array):
        """Swap adjacent pixels horizontally"""
        result = pixel_array.copy()
        height, width, channels = result.shape
        
        for i in range(0, width - 1, 2):
            result[:, i], result[:, i + 1] = result[:, i + 1].copy(), result[:, i].copy()
        
        return result
    
    def adjacent_swap_decrypt(self, pixel_array):
        """Adjacent swap is its own inverse"""
        return self.adjacent_swap_encrypt(pixel_array)
    
    # Method 5: Random Pixel Swapping
    def random_swap_encrypt(self, pixel_array, swap_percentage=0.5, seed=42):
        """Randomly swap pixel positions"""
        random.seed(seed)
        np.random.seed(seed)
        
        result = pixel_array.copy()
        height, width, channels = result.shape
        total_pixels = height * width
        num_swaps = int(total_pixels * swap_percentage)
        
        # Store swap pairs for reversibility
        swap_pairs = []
        for _ in range(num_swaps):
            y1, x1 = random.randint(0, height - 1), random.randint(0, width - 1)
            y2, x2 = random.randint(0, height - 1), random.randint(0, width - 1)
            swap_pairs.append(((y1, x1), (y2, x2)))
        
        # Apply swaps
        for (y1, x1), (y2, x2) in swap_pairs:
            result[y1, x1], result[y2, x2] = result[y2, x2].copy(), result[y1, x1].copy()
        
        return result
    
    def random_swap_decrypt(self, pixel_array, swap_percentage=0.5, seed=42):
        """Random swap with same seed reverses the operation by applying swaps in reverse order"""
        random.seed(seed)
        np.random.seed(seed)
        
        result = pixel_array.copy()
        height, width, channels = result.shape
        total_pixels = height * width
        num_swaps = int(total_pixels * swap_percentage)
        
        # Generate same swap pairs
        swap_pairs = []
        for _ in range(num_swaps):
            y1, x1 = random.randint(0, height - 1), random.randint(0, width - 1)
            y2, x2 = random.randint(0, height - 1), random.randint(0, width - 1)
            swap_pairs.append(((y1, x1), (y2, x2)))
        
        # Apply swaps in reverse order to undo
        for (y1, x1), (y2, x2) in reversed(swap_pairs):
            result[y1, x1], result[y2, x2] = result[y2, x2].copy(), result[y1, x1].copy()
        
        return result
    
    # Method 6: Block-based Pixel Swapping
    def block_swap_encrypt(self, pixel_array, block_size=4):
        """Swap blocks of pixels"""
        result = pixel_array.copy()
        height, width, channels = result.shape
        
        # Calculate number of blocks
        h_blocks = height // block_size
        w_blocks = width // block_size
        
        # Create list of block positions
        blocks = [(i, j) for i in range(h_blocks) for j in range(w_blocks)]
        
        # Shuffle blocks
        shuffled_blocks = blocks.copy()
        random.shuffle(shuffled_blocks)
        
        # Create mapping and swap blocks
        temp_array = result.copy()
        for orig_pos, new_pos in zip(blocks, shuffled_blocks):
            orig_y, orig_x = orig_pos[0] * block_size, orig_pos[1] * block_size
            new_y, new_x = new_pos[0] * block_size, new_pos[1] * block_size
            
            result[new_y:new_y + block_size, new_x:new_x + block_size] = \
                temp_array[orig_y:orig_y + block_size, orig_x:orig_x + block_size]
        
        return result
    
    def block_swap_decrypt(self, pixel_array, block_size=4):
        """Block swap with same seed reverses the operation"""
        result = pixel_array.copy()
        height, width, channels = result.shape
        
        # Calculate number of blocks
        h_blocks = height // block_size
        w_blocks = width // block_size
        
        # Create list of block positions
        blocks = [(i, j) for i in range(h_blocks) for j in range(w_blocks)]
        
        # Shuffle blocks (same order as encryption)
        shuffled_blocks = blocks.copy()
        random.shuffle(shuffled_blocks)
        
        # Create reverse mapping and swap blocks
        temp_array = result.copy()
        for orig_pos, new_pos in zip(blocks, shuffled_blocks):
            orig_y, orig_x = orig_pos[0] * block_size, orig_pos[1] * block_size
            new_y, new_x = new_pos[0] * block_size, new_pos[1] * block_size
            
            result[orig_y:orig_y + block_size, orig_x:orig_x + block_size] = \
                temp_array[new_y:new_y + block_size, new_x:new_x + block_size]
        
        return result
    
    # Method 7: Color Channel Shifting
    def channel_shift_encrypt(self, pixel_array, shift=1):
        """Shift color channels (R->G->B->R)"""
        result = pixel_array.copy()
        
        if shift == 1:
            # R->G, G->B, B->R
            result[:, :, 0], result[:, :, 1], result[:, :, 2] = \
                pixel_array[:, :, 2].copy(), pixel_array[:, :, 0].copy(), pixel_array[:, :, 1].copy()
        elif shift == 2:
            # R->B, G->R, B->G
            result[:, :, 0], result[:, :, 1], result[:, :, 2] = \
                pixel_array[:, :, 1].copy(), pixel_array[:, :, 2].copy(), pixel_array[:, :, 0].copy()
        
        return result
    
    def channel_shift_decrypt(self, pixel_array, shift=1):
        """Reverse channel shifting"""
        if shift == 1:
            return self.channel_shift_encrypt(pixel_array, 2)
        elif shift == 2:
            return self.channel_shift_encrypt(pixel_array, 1)
        
        return pixel_array
    
    # Main encryption/decryption interface
    def encrypt(self, image_path, output_path, method='xor', **kwargs):
        """Encrypt an image using specified method"""
        pixel_array = self.load_image(image_path)
        
        if method == 'xor':
            encrypted = self.xor_encrypt(pixel_array, kwargs.get('key', 123))
        elif method == 'arithmetic':
            encrypted = self.arithmetic_encrypt(
                pixel_array, 
                kwargs.get('operation', 'add'),
                kwargs.get('value', 50)
            )
        elif method == 'bit_shift':
            encrypted = self.bit_shift_encrypt(
                pixel_array,
                kwargs.get('shift_amount', 2),
                kwargs.get('direction', 'left')
            )
        elif method == 'adjacent_swap':
            encrypted = self.adjacent_swap_encrypt(pixel_array)
        elif method == 'random_swap':
            encrypted = self.random_swap_encrypt(
                pixel_array,
                kwargs.get('swap_percentage', 0.5),
                kwargs.get('seed', 42)
            )
        elif method == 'block_swap':
            random.seed(kwargs.get('seed', 42))
            encrypted = self.block_swap_encrypt(
                pixel_array,
                kwargs.get('block_size', 4)
            )
        elif method == 'channel_shift':
            encrypted = self.channel_shift_encrypt(
                pixel_array,
                kwargs.get('shift', 1)
            )
        else:
            raise ValueError(f"Unknown encryption method: {method}")
        
        self.save_image(encrypted, output_path)
        return encrypted
    
    def decrypt(self, image_path, output_path, method='xor', **kwargs):
        """Decrypt an image using specified method"""
        pixel_array = self.load_image(image_path)
        
        if method == 'xor':
            decrypted = self.xor_decrypt(pixel_array, kwargs.get('key', 123))
        elif method == 'arithmetic':
            decrypted = self.arithmetic_decrypt(
                pixel_array,
                kwargs.get('operation', 'add'),
                kwargs.get('value', 50)
            )
        elif method == 'bit_shift':
            decrypted = self.bit_shift_decrypt(
                pixel_array,
                kwargs.get('shift_amount', 2),
                kwargs.get('direction', 'left')
            )
        elif method == 'adjacent_swap':
            decrypted = self.adjacent_swap_decrypt(pixel_array)
        elif method == 'random_swap':
            decrypted = self.random_swap_decrypt(
                pixel_array,
                kwargs.get('swap_percentage', 0.5),
                kwargs.get('seed', 42)
            )
        elif method == 'block_swap':
            random.seed(kwargs.get('seed', 42))
            decrypted = self.block_swap_decrypt(
                pixel_array,
                kwargs.get('block_size', 4)
            )
        elif method == 'channel_shift':
            decrypted = self.channel_shift_decrypt(
                pixel_array,
                kwargs.get('shift', 1)
            )
        else:
            raise ValueError(f"Unknown decryption method: {method}")
        
        self.save_image(decrypted, output_path)
        return decrypted
