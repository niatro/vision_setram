import base64
import json
import openai
import os
import time
import pandas as pd
import shutil
from dotenv import load_dotenv
from prompt import prompt_r1, prompt_r2
from anthropic import Anthropic
import textwrap


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
                        {"type": "text", "text": prompt_r1},
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

def load_and_encode_image(image_path):
    """Load an image from a path and encode it to base64."""
    # Determine the media type based on file extension
    file_extension = os.path.splitext(image_path)[1].lower()
    media_type = "image/jpeg" if file_extension in ['.jpg', '.jpeg'] else "image/png"
    
    # Read and encode the image
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
    base64_encoded_data = base64.b64encode(binary_data)
    base64_string = base64_encoded_data.decode('utf-8')
    
    return base64_string, media_type

def create_api_message(base64_string, media_type, prompt_text):
    """Create a message list for API request."""
    message_list = [
        {
            "role": 'user',
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": base64_string}},
                {"type": "text", "text": prompt_text}
            ]
        }
    ]
    return message_list

def send_to_api_and_process(client, model_name, message_list):
    """Send the constructed message to the API and process the response."""
    try:
        response = client.messages.create(
            model=model_name,
            max_tokens=2048,
            messages=message_list
        )
         # Imprime la respuesta cruda para depuración
        print("Respuesta cruda de la API:", response.content)
        # Verifica si la respuesta tiene contenido y si es un JSON válido
        if response.content and response.content[0].text:
            json_data = json.loads(response.content[0].text)
        else:
            print("Respuesta de la API vacía o no válida.")
            return {}  # Retorna un diccionario vacío si no hay datos válidos
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {str(e)}")
        return {}
    except Exception as e:
        print(f"Error processing API response: {str(e)}")
        return {}
    return json_data


def save_data_and_manage_files(json_data, image_path, data_records):
    """Save JSON data to a file, update records, and copy the image to a repository."""
    if json_data:
        filename_without_extension = os.path.splitext(os.path.basename(image_path))[0]
        json_filename = f"{filename_without_extension}.json"
        if not os.path.exists('Data'):
            os.makedirs('Data')
        with open(os.path.join("Data", json_filename), 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        
        # Update data records and copy image
        data_records.append(json_data)
        
        if not os.path.exists('repo_imagenes'):
            os.makedirs('repo_imagenes')
        shutil.copy(image_path, os.path.join('repo_imagenes', os.path.basename(image_path)))

        return f"Data saved to Data/{json_filename} and image copied to repo_imagenes/{os.path.basename(image_path)}"
    else:
        return f"No valid data received for {image_path}"
    
def describe_image_with_haiku(image_path, data_records):
    """Envía la imagen codificada en base64 al modelo Haiku de Anthropic y maneja los datos de respuesta."""
    MODEL_NAME = "claude-3-haiku-20240307"
    
    try:
        # Load and encode image
        base64_string, media_type = load_and_encode_image(image_path)
        
        # First API call
        message_list = create_api_message(base64_string, media_type, prompt_r1)
        client = Anthropic()  # Assume client initialization
        json_data = send_to_api_and_process(client, MODEL_NAME, message_list)
        save_data_and_manage_files(json_data, image_path, data_records)

        # Format prompt_r2 with the JSON data from the first call
        formatted_prompt_r2 = prompt_r2.replace("{$JSON}", json.dumps(json_data))
        
        # Second API call with the updated prompt
        message_list_r2 = create_api_message(base64_string, media_type, formatted_prompt_r2)
        json_data_r2 = send_to_api_and_process(client, MODEL_NAME, message_list_r2)
        save_data_and_manage_files(json_data_r2, image_path, data_records)
        
    except Exception as e:
        print(f"An error occurred while processing {image_path}: {str(e)}")



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
