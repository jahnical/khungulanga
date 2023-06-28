import cv2
import numpy as np
from PIL import Image

def center_skin(skin, image):
    """
    Centers the skin region within the image.

    Args:
        skin (numpy.ndarray): Binary mask representing the skin region.
        image (numpy.ndarray): Input image.

    Returns:
        numpy.ndarray: Centered image.

    """
    contours, _ = cv2.findContours(skin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    (x, y, w, h) = cv2.boundingRect(largest_contour)

    center_x = x + w // 2
    center_y = y + h // 2

    image_height, image_width, _ = image.shape
    center_image_x = image_width // 2
    center_image_y = image_height // 2

    offset_x = center_image_x - center_x
    offset_y = center_image_y - center_y

    translation_matrix = np.float32([[1, 0, offset_x], [0, 1, offset_y]])

    centered_image = cv2.warpAffine(image, translation_matrix, (image_width, image_height))

    return centered_image

def detect_skin(image):
    """
    Detects the presence of skin in an image.

    Args:
        image (numpy.ndarray): Input image.

    Returns:
        bool: True if skin is present, False otherwise.

    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    ycbcr = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    
    lower_skin = np.array([0, 129, 85], dtype=np.uint8)
    upper_skin = np.array([255, 180, 135], dtype=np.uint8)
    
    skin_mask = cv2.inRange(ycbcr, lower_skin, upper_skin)
    
    kernel = np.ones((3, 3), np.uint8)
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel, iterations=2)
    skin_mask = cv2.dilate(skin_mask, kernel, iterations=1)
    skin_mask = cv2.erode(skin_mask, kernel, iterations=1)
    
    total_pixels = image.shape[0] * image.shape[1]
    skin_pixels = cv2.countNonZero(skin_mask)
    skin_percentage = skin_pixels / total_pixels
    
    has_skin = skin_percentage > 0.4
    
    return has_skin
