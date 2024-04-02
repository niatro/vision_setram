import base64
import json
import openai
import os
import time
import pandas as pd
import shutil
from dotenv import load_dotenv
from prompt import prompt
from anthropic import Anthropic

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
Anthropic.api_key = os.getenv('ANTHROPIC_API_KEY')


def encode_image(image_path):
    """Codifica la imagen en base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def describe_image_with_gpt4(image_path, data_records):
    """Envía la imagen codificada en base64 a GPT-4 con visión y maneja límites de tasa."""
    image_url = f"data:image/jpeg;base64,{encode_image(image_path)}"
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4-vision-preview',
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ],
                }
            ],
            max_tokens=500,
        )
        json_string = response.choices[0].message.content.strip()
        if json_string.startswith('```json') and json_string.endswith('```'):
            json_string = json_string[7:-3].strip()
        if json_string:
            json_data = json.loads(json_string)
            # Guarda el JSON en la carpeta 'Data'
            filename_without_extension = os.path.splitext(os.path.basename(image_path))[0]
            json_filename = f"{filename_without_extension}.json"
            if not os.path.exists('Data'):
                os.makedirs('Data')
            with open(os.path.join("Data", json_filename), 'w') as json_file:
                json.dump(json_data, json_file, indent=4)
            
            # Añade la ruta de la imagen al JSON
            json_data['Ruta Imagen'] = os.path.join('repo_imagenes', os.path.basename(image_path))

            json_data['Nombre del archivo'] = os.path.basename(image_path)
            
            # Añade el registro JSON a data_records
            data_records.append(json_data)
            
            # Copia la imagen a 'repo_imagenes'
            if not os.path.exists('repo_imagenes'):
                os.makedirs('repo_imagenes')
            shutil.copy(image_path, os.path.join('repo_imagenes', os.path.basename(image_path)))
            
            print(f"Data saved to Data/{json_filename} and image copied to repo_imagenes/{os.path.basename(image_path)}")
        else:
            print(f"No valid JSON data received for {image_path}")
    except openai.error.RateLimitError:
        print("Límite de tasa alcanzado, esperando para reintentar...")
        time.sleep(60)  # Espera 60 segundos antes de reintentar
        describe_image_with_gpt4(image_path, data_records)  # Reintenta la misma solicitud
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for {image_path}: {str(e)}")



def describe_image_with_haiku(image_path, data_records):
    """Envía la imagen codificada en base64 al modelo Haiku de Anthropic y maneja los datos de respuesta."""
    MODEL_NAME = "claude-3-haiku-20240307"
    
    # Determina el tipo de medio basado en la extensión del archivo
    file_extension = os.path.splitext(image_path)[1].lower()
    media_type = "image/jpeg" if file_extension in ['.jpg', '.jpeg'] else "image/png"
    
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
    base_64_encoded_data = base64.b64encode(binary_data)
    base64_string = base_64_encoded_data.decode('utf-8')
    
    message_list = [
        {
            "role": 'user',
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": base64_string}},
                {"type": "text", "text": prompt}
            ]
        }
    ]
    
    try:
        # Inicializar cliente de Anthropic
        client = Anthropic()
        
        # Envío de la imagen y el texto al modelo Haiku
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=2048,
            messages=message_list
        )
        
        # Procesamiento de la respuesta
        json_data = json.loads(response.content[0].text) if response.content[0].text else {}
        if json_data:
            filename_without_extension = os.path.splitext(os.path.basename(image_path))[0]
            json_filename = f"{filename_without_extension}.json"
            if not os.path.exists('Data'):
                os.makedirs('Data')
            with open(os.path.join("Data", json_filename), 'w') as json_file:
                json.dump(json_data, json_file, indent=4)
            
            # Actualización de registros y copia de la imagen
            json_data['Ruta Imagen'] = os.path.join('repo_imagenes', os.path.basename(image_path))
            json_data['Nombre del archivo'] = os.path.basename(image_path)
            data_records.append(json_data)
            
            if not os.path.exists('repo_imagenes'):
                os.makedirs('repo_imagenes')
            shutil.copy(image_path, os.path.join('repo_imagenes', os.path.basename(image_path)))
            
            print(f"Data saved to Data/{json_filename} and image copied to repo_imagenes/{os.path.basename(image_path)}")
        else:
            print(f"No valid data received for {image_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")



def describe_image(model, image_path, data_records):
    """Función genérica para describir la imagen usando el modelo especificado."""
    if model.lower() == 'haiku':
        describe_image_with_haiku(image_path, data_records)
    elif model.lower() == 'gpt4':
        describe_image_with_gpt4(image_path, data_records)
    else:
        print(f"Modelo '{model}' no reconocido. Por favor, elige 'haiku' o 'gpt4'.")

def process_folder(folder_path, model, data_records):
    """Procesa todas las imágenes en una carpeta específica usando el modelo especificado y guarda los resultados."""
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            print(f"Procesando {filename} con {model}...")
            describe_image(model, image_path, data_records)

def extract_data_to_excel(data_records):
    """Extrae los datos recolectados a un archivo Excel con hipervínculos."""
    df = pd.json_normalize(data_records)
    # Asegúrate de que 'Ruta Imagen' y 'Nombre del archivo' están incluidos en data_records

    # Usamos ExcelWriter para un control más fino sobre la escritura de Excel
    with pd.ExcelWriter('reporte_imagenes.xlsx', engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Reporte')

        # Trabaja con el workbook y el worksheet para editar el formato
        workbook = writer.book
        worksheet = writer.sheets['Reporte']

        # Encuentra las columnas correctas para los hipervínculos y las fotos
        ruta_imagen_col = df.columns.get_loc('Ruta Imagen') + 1  # +1 debido al índice de Excel
        nombre_archivo_col = df.columns.get_loc('Nombre del archivo') + 1  # +1 debido al índice de Excel

        # Itera sobre las filas para añadir hipervínculos
                # Itera sobre las filas para añadir hipervínculos
        for i, row in df.iterrows():
            # Calcula la letra de la columna basada en ruta_imagen_col
            col_letter = chr(ruta_imagen_col + 64)  # Convierte el índice de la columna a letra (A=1, B=2, ...)
            # Añade un hipervínculo en la celda correcta
            worksheet.write_url(f'{col_letter}{i + 2}', f"external:{row['Ruta Imagen']}", string='Ver Imagen')


        # Añade el nombre del archivo de la foto en la celda 'Fotos'
        # Este paso ya se maneja al incluir 'Nombre del archivo' en el DataFrame

    print("Reporte de imágenes generado con éxito.")

def main():
    folders = ["images", "senales", "eventos"]
    data_records = []  # Esta lista almacenará los datos JSON
    model = input("Elige el modelo a utilizar ('haiku' o 'gpt4'): ").strip()
    
    # Asegúrate de que la carpeta 'repo_imagenes' exista
    if not os.path.exists('repo_imagenes'):
        os.makedirs('repo_imagenes')

    for folder in folders:
        print(f"Procesando carpeta: {folder}")
        process_folder(folder, model, data_records)
    
    # Extraer datos a Excel
    extract_data_to_excel(data_records)

if __name__ == "__main__":
    main()
