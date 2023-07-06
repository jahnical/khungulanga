import numpy as np
import cv2

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

def skin_segmentation(image):
    """
    Performs skin segmentation on the input image.

    Args:
        image (numpy.ndarray): Input image.

    Returns:
        tuple: A tuple containing the centered image and the skin mask.

    """
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_image[:, :, 2] = cv2.equalizeHist(hsv_image[:, :, 2])
    image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    ycbcr = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    lower_skin = np.array([0, 132, 80], dtype=np.uint8)
    upper_skin = np.array([255, 183, 135], dtype=np.uint8)
    skin_mask = cv2.inRange(ycbcr, lower_skin, upper_skin)
    kernel = np.ones((3, 3), np.uint8)
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel, iterations=4)
    skin_mask = cv2.dilate(skin_mask, kernel, iterations=3)
    skin_mask = cv2.erode(skin_mask, kernel, iterations=3)

    img_skin = cv2.bitwise_and(image, image, mask=skin_mask)

    return center_skin(skin_mask, img_skin), skin_mask

def preprocess_image(img, target_size=(299, 299)):
    """
    Preprocesses the input image for further analysis.
    
    Denoising, Equalization, Skin Segmentation, Skin Centering, 
    Contrast Enhancement, Resizing and Normalization

    Args:
        img (PIL.Image.Image): Input image.
        target_size (tuple): Target size for resizing the image.

    Returns:
        numpy.ndarray: Preprocessed image.

    """
    img = np.asarray(img.resize(target_size), dtype=np.uint8)
    denoised_image = cv2.GaussianBlur(img, (3, 3), 0)
    skin_image, skin_mask = skin_segmentation(denoised_image)
    lab_img = cv2.cvtColor(skin_image, cv2.COLOR_RGB2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab_img)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_channel = clahe.apply(l_channel)
    modified_lab_img = cv2.merge((l_channel, a_channel, b_channel))
    enhanced_image = cv2.cvtColor(modified_lab_img, cv2.COLOR_LAB2BGR)
    hsv_image = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2HSV)
    hsv_image[:, :, 2] = cv2.equalizeHist(hsv_image[:, :, 2])
    equalized_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)

    return np.asarray(equalized_image, dtype=np.float32) / 255.0
