"""
Image Encryption Tool using Pixel Manipulation

This module provides functionality to encrypt and decrypt images using various
pixel manipulation techniques including pixel swapping and mathematical operations.
"""

import random
from PIL import Image
import numpy as np
from typing import Tuple, List, Union
import os


class ImageEncryptor:
    """
    A class for encrypting and decrypting images using pixel manipulation techniques.
    """
    
    def __init__(self, seed: int = None):
        """
        Initialize the ImageEncryptor.
        
        Args:
            seed (int): Random seed for reproducible encryption/decryption
        """
        self.seed = seed
        if seed:
            random.seed(seed)
            np.random.seed(seed)
    
    def load_image(self, image_path: str) -> np.ndarray:
        """
        Load an image and convert it to a numpy array.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            np.ndarray: Image as numpy array
        """
        try:
            image = Image.open(image_path)
            # Convert to RGB if not already
            if image.mode != 'RGB':
                image = image.convert('RGB')
            return np.array(image)
        except Exception as e:
            raise ValueError(f"Error loading image: {e}")
    
    def save_image(self, image_array: np.ndarray, output_path: str) -> None:
        """
        Save a numpy array as an image file.
        
        Args:
            image_array (np.ndarray): Image array to save
            output_path (str): Output file path
        """
        try:
            # Ensure values are in valid range [0, 255]
            image_array = np.clip(image_array, 0, 255).astype(np.uint8)
            image = Image.fromarray(image_array, 'RGB')
            image.save(output_path)
        except Exception as e:
            raise ValueError(f"Error saving image: {e}")
    
    def get_pixel_positions(self, height: int, width: int) -> List[Tuple[int, int]]:
        """
        Get all pixel positions in the image.
        
        Args:
            height (int): Image height
            width (int): Image width
            
        Returns:
            List[Tuple[int, int]]: List of (row, col) positions
        """
        positions = []
        for i in range(height):
            for j in range(width):
                positions.append((i, j))
        return positions
    
    # =========================
    # PIXEL SWAPPING METHODS
    # =========================
    
    def swap_adjacent_pixels(self, image_array: np.ndarray) -> np.ndarray:
        """
        Swap adjacent pixels in pairs (horizontally).
        
        Args:
            image_array (np.ndarray): Input image array
            
        Returns:
            np.ndarray: Image with adjacent pixels swapped
        """
        encrypted_image = image_array.copy()
        height, width = encrypted_image.shape[:2]
        
        # Swap adjacent pixels horizontally
        for i in range(height):
            for j in range(0, width - 1, 2):  # Step by 2 to swap pairs
                # Swap pixels at (i, j) and (i, j+1)
                temp = encrypted_image[i, j].copy()
                encrypted_image[i, j] = encrypted_image[i, j + 1]
                encrypted_image[i, j + 1] = temp
        
        return encrypted_image
    
    def swap_random_pixels(self, image_array: np.ndarray, swap_percentage: float = 0.5) -> np.ndarray:
        """
        Randomly swap pixels in the image.
        
        Args:
            image_array (np.ndarray): Input image array
            swap_percentage (float): Percentage of pixels to swap (0.0 to 1.0)
            
        Returns:
            np.ndarray: Image with randomly swapped pixels
        """
        encrypted_image = image_array.copy()
        height, width = encrypted_image.shape[:2]
        
        # Get all pixel positions
        positions = self.get_pixel_positions(height, width)
        
        # Determine number of swaps
        num_swaps = int(len(positions) * swap_percentage / 2)  # Divide by 2 since each swap affects 2 pixels
        
        # Randomly select positions to swap
        random.shuffle(positions)
        
        for i in range(0, min(num_swaps * 2, len(positions)), 2):
            if i + 1 < len(positions):
                pos1 = positions[i]
                pos2 = positions[i + 1]
                
                # Swap pixels
                temp = encrypted_image[pos1[0], pos1[1]].copy()
                encrypted_image[pos1[0], pos1[1]] = encrypted_image[pos2[0], pos2[1]]
                encrypted_image[pos2[0], pos2[1]] = temp
        
        return encrypted_image
    
    def swap_block_pixels(self, image_array: np.ndarray, block_size: int = 2) -> np.ndarray:
        """
        Swap pixels within blocks of specified size.
        
        Args:
            image_array (np.ndarray): Input image array
            block_size (int): Size of blocks to swap within
            
        Returns:
            np.ndarray: Image with block-wise pixel swapping
        """
        encrypted_image = image_array.copy()
        height, width = encrypted_image.shape[:2]
        
        # Process image in blocks
        for i in range(0, height, block_size):
            for j in range(0, width, block_size):
                # Define block boundaries
                i_end = min(i + block_size, height)
                j_end = min(j + block_size, width)
                
                # Extract block
                block = encrypted_image[i:i_end, j:j_end].copy()
                block_height, block_width = block.shape[:2]
                
                # Get positions within the block
                block_positions = []
                for bi in range(block_height):
                    for bj in range(block_width):
                        block_positions.append((bi, bj))
                
                # Shuffle positions
                shuffled_positions = block_positions.copy()
                random.shuffle(shuffled_positions)
                
                # Create new block with shuffled positions
                new_block = np.zeros_like(block)
                for original_pos, new_pos in zip(block_positions, shuffled_positions):
                    new_block[new_pos[0], new_pos[1]] = block[original_pos[0], original_pos[1]]
                
                # Place shuffled block back
                encrypted_image[i:i_end, j:j_end] = new_block
        
        return encrypted_image
    
    # =========================
    # MATHEMATICAL OPERATIONS
    # =========================
    
    def xor_encrypt(self, image_array: np.ndarray, key: int = 123) -> np.ndarray:
        """
        Apply XOR encryption to each pixel value.
        
        Args:
            image_array (np.ndarray): Input image array
            key (int): XOR key (0-255)
            
        Returns:
            np.ndarray: XOR encrypted image
        """
        # Ensure key is within valid range
        key = key % 256
        
        # Apply XOR operation
        encrypted_image = image_array.copy().astype(np.int32)
        encrypted_image = encrypted_image ^ key
        
        # Ensure values stay in valid range
        encrypted_image = np.clip(encrypted_image, 0, 255).astype(np.uint8)
        
        return encrypted_image
    
    def arithmetic_encrypt(self, image_array: np.ndarray, operation: str = 'add', value: int = 50) -> np.ndarray:
        """
        Apply arithmetic operations to pixel values.
        
        Args:
            image_array (np.ndarray): Input image array
            operation (str): 'add', 'subtract', 'multiply', or 'divide'
            value (int): Value to use in the operation
            
        Returns:
            np.ndarray: Arithmetically modified image
        """
        encrypted_image = image_array.copy().astype(np.int32)
        
        if operation == 'add':
            encrypted_image = encrypted_image + value
        elif operation == 'subtract':
            encrypted_image = encrypted_image - value
        elif operation == 'multiply':
            encrypted_image = encrypted_image * value
        elif operation == 'divide' and value != 0:
            encrypted_image = encrypted_image // value
        else:
            raise ValueError(f"Unsupported operation: {operation}")
        
        # Ensure values stay in valid range [0, 255]
        encrypted_image = np.clip(encrypted_image, 0, 255).astype(np.uint8)
        
        return encrypted_image
    
    def bit_shift_encrypt(self, image_array: np.ndarray, shift_amount: int = 2, direction: str = 'left') -> np.ndarray:
        """
        Apply bit shifting to pixel values.
        
        Args:
            image_array (np.ndarray): Input image array
            shift_amount (int): Number of bits to shift
            direction (str): 'left' or 'right'
            
        Returns:
            np.ndarray: Bit-shifted image
        """
        encrypted_image = image_array.copy().astype(np.int32)
        
        if direction == 'left':
            encrypted_image = encrypted_image << shift_amount
        elif direction == 'right':
            encrypted_image = encrypted_image >> shift_amount
        else:
            raise ValueError(f"Unsupported direction: {direction}")
        
        # Ensure values stay in valid range [0, 255]
        encrypted_image = np.clip(encrypted_image, 0, 255).astype(np.uint8)
        
        return encrypted_image
    
    def color_channel_shift(self, image_array: np.ndarray) -> np.ndarray:
        """
        Shift color channels (RGB -> GBR -> BRG -> RGB).
        
        Args:
            image_array (np.ndarray): Input image array
            
        Returns:
            np.ndarray: Image with shifted color channels
        """
        encrypted_image = image_array.copy()
        
        # Shift channels: R->G, G->B, B->R
        temp = encrypted_image[:, :, 0].copy()  # Save R channel
        encrypted_image[:, :, 0] = encrypted_image[:, :, 2]  # R = B
        encrypted_image[:, :, 2] = encrypted_image[:, :, 1]  # B = G
        encrypted_image[:, :, 1] = temp  # G = original R
        
        return encrypted_image
    
    # =========================
    # HIGH-LEVEL ENCRYPT/DECRYPT METHODS
    # =========================
    
    def encrypt_image(self, image_path: str, output_path: str, method: str = 'xor', **kwargs) -> None:
        """
        Encrypt an image using the specified method.
        
        Args:
            image_path (str): Path to input image
            output_path (str): Path to save encrypted image
            method (str): Encryption method ('xor', 'arithmetic', 'bit_shift', 
                         'adjacent_swap', 'random_swap', 'block_swap', 'channel_shift')
            **kwargs: Additional arguments for specific methods
        """
        # Load image
        image_array = self.load_image(image_path)
        
        # Apply encryption based on method
        if method == 'xor':
            key = kwargs.get('key', 123)
            encrypted_image = self.xor_encrypt(image_array, key)
        elif method == 'arithmetic':
            operation = kwargs.get('operation', 'add')
            value = kwargs.get('value', 50)
            encrypted_image = self.arithmetic_encrypt(image_array, operation, value)
        elif method == 'bit_shift':
            shift_amount = kwargs.get('shift_amount', 2)
            direction = kwargs.get('direction', 'left')
            encrypted_image = self.bit_shift_encrypt(image_array, shift_amount, direction)
        elif method == 'adjacent_swap':
            encrypted_image = self.swap_adjacent_pixels(image_array)
        elif method == 'random_swap':
            swap_percentage = kwargs.get('swap_percentage', 0.5)
            encrypted_image = self.swap_random_pixels(image_array, swap_percentage)
        elif method == 'block_swap':
            block_size = kwargs.get('block_size', 2)
            encrypted_image = self.swap_block_pixels(image_array, block_size)
        elif method == 'channel_shift':
            encrypted_image = self.color_channel_shift(image_array)
        else:
            raise ValueError(f"Unsupported encryption method: {method}")
        
        # Save encrypted image
        self.save_image(encrypted_image, output_path)
        print(f"Image encrypted using '{method}' method and saved to: {output_path}")
    
    def decrypt_image(self, encrypted_image_path: str, output_path: str, method: str = 'xor', **kwargs) -> None:
        """
        Decrypt an image (for reversible methods).
        
        Args:
            encrypted_image_path (str): Path to encrypted image
            output_path (str): Path to save decrypted image
            method (str): Decryption method (must match encryption method)
            **kwargs: Additional arguments for specific methods
        """
        # Load encrypted image
        encrypted_array = self.load_image(encrypted_image_path)
        
        # Apply decryption based on method
        if method == 'xor':
            # XOR is its own inverse
            key = kwargs.get('key', 123)
            decrypted_image = self.xor_encrypt(encrypted_array, key)
        elif method == 'arithmetic':
            # Reverse the arithmetic operation
            operation = kwargs.get('operation', 'add')
            value = kwargs.get('value', 50)
            
            if operation == 'add':
                decrypted_image = self.arithmetic_encrypt(encrypted_array, 'subtract', value)
            elif operation == 'subtract':
                decrypted_image = self.arithmetic_encrypt(encrypted_array, 'add', value)
            elif operation == 'multiply' and value != 0:
                decrypted_image = self.arithmetic_encrypt(encrypted_array, 'divide', value)
            elif operation == 'divide':
                decrypted_image = self.arithmetic_encrypt(encrypted_array, 'multiply', value)
            else:
                raise ValueError(f"Cannot reverse operation: {operation}")
        elif method == 'bit_shift':
            # Reverse the bit shift
            shift_amount = kwargs.get('shift_amount', 2)
            direction = kwargs.get('direction', 'left')
            
            reverse_direction = 'right' if direction == 'left' else 'left'
            decrypted_image = self.bit_shift_encrypt(encrypted_array, shift_amount, reverse_direction)
        elif method == 'adjacent_swap':
            # Adjacent swap is its own inverse
            decrypted_image = self.swap_adjacent_pixels(encrypted_array)
        elif method == 'channel_shift':
            # Apply channel shift twice more to complete the cycle (3 total shifts = back to original)
            temp_image = self.color_channel_shift(encrypted_array)
            decrypted_image = self.color_channel_shift(temp_image)
        else:
            print(f"Warning: Method '{method}' may not be easily reversible without the exact same random seed.")
            print("Attempting decryption with same parameters...")
            
            if method == 'random_swap':
                swap_percentage = kwargs.get('swap_percentage', 0.5)
                decrypted_image = self.swap_random_pixels(encrypted_array, swap_percentage)
            elif method == 'block_swap':
                block_size = kwargs.get('block_size', 2)
                decrypted_image = self.swap_block_pixels(encrypted_array, block_size)
            else:
                raise ValueError(f"Unsupported decryption method: {method}")
        
        # Save decrypted image
        self.save_image(decrypted_image, output_path)
        print(f"Image decrypted using '{method}' method and saved to: {output_path}")