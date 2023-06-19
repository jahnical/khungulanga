import numpy as np
import cv2

# Preprocessing
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

    (x, y, w, h) = cv2.boundingRect(largest_contour)

    # Calculate the center of the bounding box
    center_x = x + w // 2
    center_y = y + h // 2
    
    # Calculate the center of the image
    image_height, image_width, _ = image.shape
    center_image_x = image_width // 2
    center_image_y = image_height // 2
    
    # Calculate the offset to center the bounding box in the image
    offset_x = center_image_x - center_x
    offset_y = center_image_y - center_y
    
    # Create a translation matrix
    translation_matrix = np.float32([[1, 0, offset_x], [0, 1, offset_y]])

    # Apply the translation matrix to the image
    centered_image = cv2.warpAffine(image, translation_matrix, (image_width, image_height))
    
    return centered_image

def skin_segmentation(image):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # Convert the image to YCbCr color space
    ycbcr = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    # Define range of skin color in YCbCr
    lower_skin = np.array([0, 130, 80], dtype=np.uint8)
    upper_skin = np.array([255, 185, 135], dtype=np.uint8)
    # Create a mask of skin pixels using YCbCr color space
    skin_mask = cv2.inRange(ycbcr, lower_skin, upper_skin)
    # Apply morphological operations to remove noise and refine the mask
    kernel = np.ones((3, 3), np.uint8)
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel, iterations=4)
    skin_mask = cv2.dilate(skin_mask, kernel, iterations=1)
    skin_mask = cv2.erode(skin_mask, kernel, iterations=1)

    # Apply the mask to the original image
    img_skin = cv2.bitwise_and(image, image, mask=skin_mask)

    return center_skin(skin_mask, img_skin), skin_mask

def preprocess_image(img, target_size=(299, 299)):
    img = np.asarray(img.resize(target_size), dtype=np.uint8)
    # Noise removal (example using Gaussian blur)
    denoised_image = cv2.GaussianBlur(img, (3, 3), 0)
    # Skin segmentation
    skin_image, skin_mask = skin_segmentation(denoised_image)
    # Contrast enhancement (example using CLAHE)
    # Convert the image to LAB color space
    lab_img = cv2.cvtColor(skin_image, cv2.COLOR_RGB2LAB)
    # Split the LAB image into L, A, and B channels
    l_channel, a_channel, b_channel = cv2.split(lab_img)
    # Apply histogram equalization to the L channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_channel = clahe.apply(l_channel)
    # Merge the modified L channel with the original A and B channels
    modified_lab_img = cv2.merge((l_channel, a_channel, b_channel))
    # Convert the LAB image back to RGB color space
    enhanced_image = cv2.cvtColor(modified_lab_img, cv2.COLOR_LAB2BGR)
    # Histogram equalization
    hsv_image = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2HSV)
    hsv_image[:, :, 2] = cv2.equalizeHist(hsv_image[:, :, 2])
    equalized_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)

    return np.asarray(equalized_image, dtype=np.float32) / 255.0