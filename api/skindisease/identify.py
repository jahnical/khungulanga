import tensorflow as tf
from PIL import Image
import os
import numpy as np

from api.models.disease import Disease
from api.models.prediction import Prediction

custom_objects = {'BatchNormalization': tf.keras.layers.BatchNormalization, 'Adam': tf.keras.optimizers.Adam}
# Returns the model for the given part and itchy
def get_model(name):
    return tf.keras.models.load_model(os.path.join(os.path.dirname(__file__), "models", name + ".h5"), custom_objects=custom_objects)

models = {
    "Itchy Face": get_model("Itchy Face"),
    "Non Itchy Face": get_model("Non Itchy Face"),
    "Itchy Cranium": get_model("Itchy Cranium"),
}

labels = {
    "Itchy Face": {'acne': 0, 'eczema': 1, 'rosacea': 2, 'seborrheic dermatitis': 3, 'urticaria': 4},
    "Non Itchy Face": {'acne vulgaris': 0, 'basal cell carcinoma': 1, 'rosacea': 2, 'seborrheic dermatitis': 3, 'squamous cell carcinoma': 4},
    "Itchy Cranium": {'eczema': 0, 'folliculitis': 1, 'lichen planus': 2, 'psoriasis': 3, 'rosacea': 4, 'seborrheic dermatitis': 5}
}

diseases = Disease.objects.all()

def map_predictions(diagnosis, predictions, labels):
    disease_prob = [{"disease": disease, "probability": predictions[labels[disease]]} for disease in labels]
    disease_prob.sort(key=lambda x: x["probability"], reverse=True)
    
    return [Prediction.objects.create(
        disease=diseases.get(name=disease["disease"]), 
        diagnosis=diagnosis, 
        probability=disease["probability"]) 
            for disease in disease_prob[:3]]
    
# Identifies the skin disease in the image
def predict_disease(diagnosis):
    img = np.asarray(Image.open(diagnosis.image).resize((299, 299))) / 255.0
    img = np.expand_dims(img, axis=0)
    model = models[("Itchy" if diagnosis.itchy else "Non Itchy") + " " + diagnosis.body_part]
    model_labels = labels[("Itchy" if diagnosis.itchy else "Non Itchy") + " " + diagnosis.body_part]
    predictions = map_predictions(diagnosis, model.predict(img)[0].tolist(), model_labels)
    return predictions