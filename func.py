from flask import Flask, render_template_string
import requests
from io import BytesIO

app = Flask(__name__)

# Route principale
@app.route('/afficher_image')
def afficher_image():
    # URL de l'image à afficher
    url_image = 'https://www.manutan.fr/fstrz/r/s/www.manutan.fr/img/S/GRP/ST/AIG18043952.jpg?frz-v=96'

    # Télécharger l'image à partir de l'URL spécifiée
    response = requests.get(url_image)
    
    # Vérifier si la requête a réussi (code 200)
    if response.status_code == 200:
        # Convertir les données binaires de l'image en un objet BytesIO
        image_data = BytesIO(response.content)

        # Charger le modèle HTML avec l'image en paramètre
        template = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Afficher Image</title>
        </head>
        <body>
            <h1>Affichage de l'image</h1>
            <img src="data:image/png;base64,{{ image_data }}" alt="Image">
        </body>
        </html>
        '''

        # Rendre le modèle HTML en utilisant Flask
        return render_template_string(template, image_data=image_data.getvalue().decode('utf-8'))

    # Si la requête a échoué, retourner une erreur 404
    return "Erreur: Impossible de récupérer l'image", 404

if __name__ == '__main__':
    app.run(debug=True)
