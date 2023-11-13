import requests
from PIL import Image
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import img_to_array
import mlflow
import os
from flask import Flask, render_template_string

# Prédit le contenu de l'image
def predict_image(model, img):
    img_resized = img.resize((224, 224))
    img_array = img_to_array(img_resized)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    predictions = model.predict(img_array)
    return decode_predictions(predictions, top=1)[0][0]

app = Flask(__name__)

# Route principale
@app.route('/afficher_image')

def afficher_image():
    # URL de l'image
    image_url = 'https://www.manutan.fr/fstrz/r/s/www.manutan.fr/img/S/GRP/ST/AIG18043952.jpg?frz-v=96'  # Remplacez avec l'URL de l'image que vous souhaitez analyser

    # Télécharge et analyse l'image

    response = requests.get(image_url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))

    if img is not None:
        model = MobileNetV2(weights='imagenet')
        prediction = predict_image(model, img)
        
        # Log l'image
        img.save("predicted_image.jpg")

        # Charger le modèle HTML avec l'image en paramètre
        template = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Afficher Image</title>
        </head>
        <body>
            <h1>Affichage de l'image {{ prediction[1] }} avec confiance {{ prediction[2]*100:.2f }}</h1>
            <img src="{{ ./predicted_image.jpg }}" alt="Image">
        </body>
        </html>
        '''

    else:
        print("L'image n'a pas pu être téléchargée.")


    # Rendre le modèle HTML en utilisant Flask
    return render_template_string(template)

if __name__ == '__main__':
    app.run(debug=True)