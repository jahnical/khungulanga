import tensorflow as tf
from PIL import Image
import os
import numpy as np

from api.models.disease import Disease
from api.models.prediction import Prediction
from api.skindisease.detect_skin import detect_skin
from api.skindisease.preprocess import preprocess_image

# Custom objects required for loading the model
custom_objects = {'BatchNormalization': tf.keras.layers.BatchNormalization, 'Adam': tf.keras.optimizers.Adam}

def get_model(name):
    """
    Returns the model for the given body part.

    Args:
        name (str): Name of the body part.

    Returns:
        tf.keras.Model: Loaded model for the specified body part.
    """
    tf.keras.backend.clear_session()
    model = tf.keras.models.load_model(os.path.join(os.path.dirname(__file__), "models", name + ".h5"), custom_objects=custom_objects)
    for layer in model.layers:
        if isinstance(layer, tf.keras.layers.Dropout):
            layer.rate = 0.0
        layer.training = False
    return model

# Dictionary of models for different body parts
models = {
    "Face": get_model("Face"),
    "Upper Body": get_model("Upper Body"),
    "Legs Feet": get_model("Legs Feet"),
    "Arms Hands": get_model("Arms Hands")
}

# Labels for different body parts
labels = {
    "Face": {'acne vulgaris': 0, 'basal cell carcinoma': 1, 'rosacea': 2, 'squamous cell carcinoma': 3, 'urticaria': 4, 'zed': 5},
    "Upper Body": {'acne vulgaris': 0, 'basal cell carcinoma': 1, 'folliculitis': 2, 'lichen planus': 3, 'psoriasis': 4, 'rosacea': 5, 'scabies': 6, 'zed': 7},
    "Legs Feet": {'basal cell carcinoma': 0, 'folliculitis': 1, 'melanoma': 2, 'psoriasis': 3, 'scabies': 4, 'zed': 5},
    "Arms Hands": {'allergic contact dermatitis': 0, 'basal cell carcinoma': 1, 'lichen planus': 2, 'psoriasis': 3, 'scabies': 4, 'urticaria': 5, 'zed': 6}
}

# Fetch all diseases
diseases = Disease.objects.all()

def map_predictions(diagnosis, predictions, labels):
    """
    Maps the predictions to diseases and calculates probabilities.

    Args:
        diagnosis (Diagnosis): The diagnosis instance.
        predictions (list): Predictions obtained from the model.
        labels (dict): Labels for different diseases.

    Returns:
        list: List of Prediction instances sorted by probability.
    """
    disease_prob = [{"disease": disease, "probability": predictions[labels[disease]]} for disease in labels]
    disease_prob.sort(key=lambda x: x["probability"], reverse=True)

    if disease_prob[0]['disease'] == 'zed' and disease_prob[0]['probability'] > 0.5:
        return []

    disease_prob = list(filter(lambda x: not (x["disease"] == 'zed'), disease_prob))

    return [Prediction.objects.create(
        disease=diseases.get(name=disease["disease"]),
        diagnosis=diagnosis,
        probability=disease["probability"])
            for disease in disease_prob[:3]]

def prepare_image(img):
    """
    Preprocesses the input image for model prediction.

    Args:
        img (PIL.Image.Image): Input image.

    Returns:
        np.ndarray: Preprocessed image as numpy array.
    """
    img = preprocess_image(img, target_size=(299, 299))
    img = np.expand_dims(img, axis=0)
    return img

def predict_disease(diagnosis):
    """
    Identifies the skin disease in the image.

    Args:
        diagnosis (Diagnosis): The diagnosis instance.

    Returns:
        list: List of Prediction instances.
    """
    img = prepare_image(Image.open(diagnosis.image))
    model = models[diagnosis.body_part]
    model_labels = labels[diagnosis.body_part]
    predictions = map_predictions(diagnosis, model.predict(img)[0].tolist(), model_labels)
    return predictions
