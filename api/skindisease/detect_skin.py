import cv2
import numpy as np
from PIL import Image

def center_skin(skin, image):
    # Find the bounding box of the skin region
    contours, _ = cv2.findContours(skin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Find the contour with the largest area
    largest_contour = None
    largest_area = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > largest_area:
            largest_area = area
            largest_contour = contour
    print(largest_contour)
    (x, y, w, h) = cv2.boundingRect(largest_contour)
    print(x, y, w, h)

    # Calculate the center of the bounding box
    center_x = x + w // 2
    center_y = y + h // 2
    
    print(center_x, center_y)

    # Calculate the center of the image
    image_height, image_width, _ = image.shape
    center_image_x = image_width // 2
    center_image_y = image_height // 2
    
    print(center_image_x, center_image_y)

    # Calculate the offset to center the bounding box in the image
    offset_x = center_image_x - center_x
    offset_y = center_image_y - center_y
    
    print(offset_x, offset_y)

    # Create a translation matrix
    translation_matrix = np.float32([[1, 0, offset_x], [0, 1, offset_y]])

    # Apply the translation matrix to the image
    centered_image = cv2.warpAffine(image, translation_matrix, (image_width, image_height))
    
    return centered_image

def detect_skin(image):
    # Load the image
    # image = cv2.imread("D:/Xool/4/2/2/smartskin/media/media/diagnosis/2023/05/08/angioedema_of_lips.jpg")
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Convert the image to YCbCr color space
    ycbcr = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    
    # Define range of skin color in YCbCr
    # lower_skin = np.array([0, 135, 85], dtype=np.uint8)
    # upper_skin = np.array([255, 180, 135], dtype=np.uint8)
    # Define range of skin color in YCbCr
    lower_skin = np.array([0, 130, 85], dtype=np.uint8)
    upper_skin = np.array([255, 185, 135], dtype=np.uint8) # np.array([255, 180, 135], dtype=np.uint8)
    
    # Create a mask of skin pixels using YCbCr color space
    skin_mask = cv2.inRange(ycbcr, lower_skin, upper_skin)
    
    # Apply morphological operations to remove noise and refine the mask
    kernel = np.ones((3, 3), np.uint8)
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel, iterations=2)
    skin_mask = cv2.dilate(skin_mask, kernel, iterations=1)
    skin_mask = cv2.erode(skin_mask, kernel, iterations=1)
    
    # Determine the percentage of skin area in the image
    total_pixels = image.shape[0] * image.shape[1]
    skin_pixels = cv2.countNonZero(skin_mask)
    skin_percentage = skin_pixels / total_pixels
    
    has_skin = skin_percentage > 0.4
    print(f"Has skin: {has_skin}")
    # # Apply the mask to the original image
    # img_skin = cv2.bitwise_and(image, image, mask=skin_mask)
    
    # centered_skin = center_skin(skin_mask, img_skin)
    # img_skin = cv2.cvtColor(centered_skin, cv2.COLOR_RGB2BGR)
    # # Show the skin pixels in the original image
    # cv2.imshow('Skin Detection', img_skin)
    # cv2.waitKey(0)
    # Return the skin mask
    return has_skin #, img_skin


#detect_skin(np.asarray(Image.open("D:/Xool/4/2/2/smartskin/media/media/diagnosis/2023/05/08/angioedema_of_lips.jpg").resize((299, 299))))
