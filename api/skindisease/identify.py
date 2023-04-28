from tensorflow.python.keras.models import load_model
from PIL import Image
import os

# Returns the model for the given part and itchy
def get_model(part, itchy):
    name = ("Itchy " if itchy else "Non-Itchy ") + part
    return load_model(os.path.join(os.path.dirname(__file__), "models", name))

# Identifies the skin disease in the image
def identify(img, body_part, itchy):
    img = Image.open(img).resize((299, 299))
    model = get_model(body_part, itchy)
    return model.predict(img)