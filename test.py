import base64
import json
import os
import pandas as pd
import shutil
from dotenv import load_dotenv
from prompt import prompt_r1, prompt_r2, prompt_r3
from anthropic import Anthropic
import openai

# Cargar las variables de entorno
load_dotenv()

# Configurar las claves API
Anthropic.api_key = os.getenv('ANTHROPIC_API_KEY')
openai.api_key = os.getenv('OPENAI_API_KEY')

def load_and_encode_image(image_path):
    file_extension = os.path.splitext(image_path)[1].lower()
    media_type = "image/jpeg" if file_extension in ['.jpg', '.jpeg'] else "image/png"
    
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
    base64_encoded_data = base64.b64encode(binary_data)
    base64_string = base64_encoded_data.decode('utf-8')
    
    return base64_string, media_type

def create_api_message(base64_string, media_type, prompt_text):
    return [
        {"role": "system", "content": "You are an assistant."},
        {"role": "user", "content": prompt_text},
        {"role": "user", "content": f"data:image/{media_type};base64,{base64_string}"}
    ]

def send_to_openai_api(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=2048
    )
    return response['choices'][0]['message']['content']

def send_to_api_and_process(client, model_name, message_list, use_gpt4o, call_index, gpt4o_calls):
    try:
        if use_gpt4o and str(call_index) in gpt4o_calls:
            response_content = send_to_openai_api(message_list)
            json_data = json.loads(response_content)
        else:
            response = client.completions.create(
                model=model_name,
                max_tokens_to_sample=2048,
                prompt=message_list
            )
            print("Respuesta cruda de la API:", response.choices[0].text)
            if response.choices[0].text:
                json_data = json.loads(response.choices[0].text)
            else:
                print("Respuesta de la API vacía o no válida.")
                return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {str(e)}")
        return {}
    except Exception as e:
        print(f"Error processing API response: {str(e)}")
        return {}
    return json_data

def save_data_and_manage_files(json_data, image_path, data_records):
    if json_data:
        filename_without_extension = os.path.splitext(os.path.basename(image_path))[0]
        json_filename = f"{filename_without_extension}.json"
        if not os.path.exists('Data'):
            os.makedirs('Data')
        with open(os.path.join("Data", json_filename), 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        
        json_data['Imagen'] = os.path.basename(image_path)
        json_data['Link'] = os.path.join('repo_imagenes', os.path.basename(image_path))
        
        data_records.append(json_data)
        
        if not os.path.exists('repo_imagenes'):
            os.makedirs('repo_imagenes')
        shutil.copy(image_path, os.path.join('repo_imagenes', os.path.basename(image_path)))
        
        return f"Data saved to Data/{json_filename} and image copied to repo_imagenes/{os.path.basename(image_path)}"
    else:
        return f"No valid data received for {image_path}"

def describe_image_with_haiku(image_path, data_records, use_gpt4o, gpt4o_calls):
    MODEL_NAME = "claude-3-haiku-20240307"

    try:
        base64_string, media_type = load_and_encode_image(image_path)

        # Primer llamado a la API
        message_list = create_api_message(base64_string, media_type, prompt_r1)
        client = Anthropic()
        json_data = send_to_api_and_process(client, MODEL_NAME, message_list, use_gpt4o, 1, gpt4o_calls)

        # Preparar segundo llamado
        formatted_prompt_r2 = prompt_r2.replace("{$JSON}", json.dumps(json_data))
        message_list_r2 = create_api_message(base64_string, media_type, formatted_prompt_r2)
        json_data_r2 = send_to_api_and_process(client, MODEL_NAME, message_list_r2, use_gpt4o, 2, gpt4o_calls)

        # Preparar tercer llamado
        formatted_prompt_r3 = prompt_r3.replace("{$JSON}", json.dumps(json_data_r2))
        message_list_r3 = create_api_message(base64_string, media_type, formatted_prompt_r3)
        json_data_r3 = send_to_api_and_process(client, MODEL_NAME, message_list_r3, use_gpt4o, 3, gpt4o_calls)

        save_data_and_manage_files(json_data_r3, image_path, data_records)

    except Exception as e:
        print(f"An error occurred while processing {image_path}: {str(e)}")

def describe_image(model, image_path, data_records, use_gpt4o, gpt4o_calls):
    if model.lower() == 'haiku':
        describe_image_with_haiku(image_path, data_records, use_gpt4o, gpt4o_calls)
    else:
        print(f"Modelo '{model}' no reconocido. Por favor, elige 'haiku'.")

def process_folder(folder_path, model, data_records, use_gpt4o, gpt4o_calls):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            print(f"Procesando {filename} con {model}...")
            describe_image(model, image_path, data_records, use_gpt4o, gpt4o_calls)

def extract_data_to_excel(data_records):
    if not data_records:
        print("No hay datos para exportar.")
        return

    df = pd.json_normalize(data_records)
    with pd.ExcelWriter('reporte_imagenes.xlsx', engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Reporte')
        
        worksheet = writer.sheets['Reporte']
        
        if 'Link' in df.columns:
            link_col = df.columns.get_loc('Link')
            for i, row in enumerate(df['Link']):
                worksheet.write_url(i+1, link_col, f"external:{row}", string=row)

    print("Reporte de imágenes generado con éxito.")

def main():
    folders = ["images", "senales", "eventos"]
    data_records = []
    model = 'haiku'

    use_gpt4o = input("¿Quieres usar GPT-4o? (si/no): ").lower() == 'si'
    gpt4o_calls = []
    if use_gpt4o:
        gpt4o_calls = input("¿En cuántas llamadas quieres usar GPT-4o? (1, 2, 3): ").split(',')

    if not os.path.exists('repo_imagenes'):
        os.makedirs('repo_imagenes')

    for folder in folders:
        print(f"Procesando carpeta: {folder}")
        process_folder(folder, model, data_records, use_gpt4o, gpt4o_calls)

    extract_data_to_excel(data_records)

if __name__ == "__main__":
    main()

