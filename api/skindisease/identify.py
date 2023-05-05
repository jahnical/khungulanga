import tensorflow as tf
from PIL import Image
import os
import numpy as np

custom_objects = {'BatchNormalization': tf.keras.layers.BatchNormalization, 'Adam': tf.keras.optimizers.Adam}
# Returns the model for the given part and itchy
def get_model(name):
    return tf.keras.models.load_model(os.path.join(os.path.dirname(__file__), "models", name), custom_objects=custom_objects)

models = {
    "Itchy Face": get_model("Itchy Face")
}

labels = {
    "Itchy Face": ['rosacea', 'eczema', 'vitiligo', 'Unknown', 'seborrheic dermatitis', 'psoriasis']
}

# Identifies the skin disease in the image
def predict_disease(img, body_part, itchy):
    img = np.asarray(Image.open(img).resize((299, 299))) / 255.0
    img = np.expand_dims(img, axis=0)
    model = models[("Itchy" if itchy else "Non Itchy") + " " + body_part]
    model_labels = labels[("Itchy" if itchy else "Non Itchy") + " " + body_part]
    predictions = model.predict(img)[0].tolist()
    return list(zip(model_labels, predictions))