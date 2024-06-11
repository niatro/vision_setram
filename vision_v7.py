import base64
import json
import os
import pandas as pd
import shutil
import requests
from dotenv import load_dotenv
from prompt import prompt_r1, prompt_r2, prompt_r3
from anthropic import Anthropic

load_dotenv()

Anthropic.api_key = os.getenv('ANTHROPIC_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

models = {
    "openai": ["gpt-4o"],
    "anthropic": [
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307"
    ]
}

def select_model():
    print("Select a model type:")
    model_types = list(models.keys())
    for i, key in enumerate(model_types, 1):
        print(f"{i}. {key}")
    model_type_index = int(input("Model type (number): ").strip()) - 1
    
    if model_type_index < 0 or model_type_index >= len(model_types):
        print("Invalid model type. Please choose a valid number.")
        return select_model()
    
    model_type = model_types[model_type_index]
    
    print(f"Select a model from {model_type}:")
    model_list = models[model_type]
    for j, model in enumerate(model_list, 1):
        print(f"{j}. {model}")
    model_name_index = int(input("Model name (number): ").strip()) - 1
    
    if model_name_index < 0 or model_name_index >= len(model_list):
        print("Invalid model name. Please choose a valid number.")
        return select_model()
    
    model_name = model_list[model_name_index]
    
    # Select image detail level
    print("Select image detail level:")
    detail_levels = ["low", "high"]
    for k, level in enumerate(detail_levels, 1):
        print(f"{k}. {level}")
    detail_level_index = int(input("Detail level (number): ").strip()) - 1
    
    if detail_level_index < 0 or detail_level_index >= len(detail_levels):
        print("Invalid detail level. Please choose a valid number.")
        return select_model()
    
    detail_level = detail_levels[detail_level_index]
    
    return model_type, model_name, detail_level


def load_and_encode_image(image_path):
    file_extension = os.path.splitext(image_path)[1].lower()
    media_type = "image/jpeg" if file_extension in ['.jpg', '.jpeg'] else "image/png"
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
    base64_encoded_data = base64.b64encode(binary_data)
    base64_string = base64_encoded_data.decode('utf-8')
    return base64_string, media_type

def create_api_message(base64_string, media_type, prompt_text):
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

def send_to_anthropic(client, model_name, message_list):
    try:
        response = client.messages.create(
            model=model_name,
            max_tokens=2048,
            messages=message_list
        )
        print("Respuesta cruda de la API:", response.content)
        if response.content and response.content[0].text:
            json_data = json.loads(response.content[0].text)
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

def send_to_openai(model_name, image_path, prompt_text, detail_level, prev_json=None):
    encoded_image = load_and_encode_image(image_path)[0]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    message = {
        "role": "user",
        "content": [
            {"type": "text", "text": prompt_text},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpg;base64,{encoded_image}",
                    "detail": detail_level
                }
            }
        ]
    }
    
    if prev_json:
        message["content"].append({"type": "text", "text": prev_json})

    payload = {
        "model": model_name,
        "temperature": 0.5,
        "messages": [message],
        "max_tokens": 1000
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    try:
        response_json = response.json()
        print("Full API response:", response_json)  # Agregar depuración
        return response_json
    except Exception as e:
        print(f"Error processing OpenAI response: {str(e)}")
        print(f"Response content: {response.content}")  # Imprimir contenido de la respuesta
        return {}





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

def describe_image_with_anthropic(image_path, data_records):
    MODEL_NAME = "claude-3-haiku-20240307"
    try:
        base64_string, media_type = load_and_encode_image(image_path)
        message_list = create_api_message(base64_string, media_type, prompt_r1)
        client = Anthropic()
        json_data = send_to_anthropic(client, MODEL_NAME, message_list)
        formatted_prompt_r2 = prompt_r2.replace("{$JSON}", json.dumps(json_data))
        message_list_r2 = create_api_message(base64_string, media_type, formatted_prompt_r2)
        json_data_r2 = send_to_anthropic(client, MODEL_NAME, message_list_r2)
        formatted_prompt_r3 = prompt_r3.replace("{$JSON}", json.dumps(json_data_r2))
        message_list_r3 = create_api_message(base64_string, media_type, formatted_prompt_r3)
        json_data_r3 = send_to_anthropic(client, MODEL_NAME, message_list_r3)
        save_data_and_manage_files(json_data_r3, image_path, data_records)
    except Exception as e:
        print(f"An error occurred while processing {image_path}: {str(e)}")

def describe_image_with_openai(image_path, data_records, detail_level):
    try:
        base64_string, media_type = load_and_encode_image(image_path)

        # Primera llamada a la API
        response = send_to_openai("gpt-4o", image_path, prompt_r1, detail_level)
        if 'choices' in response and response['choices']:
            json_data = response['choices'][0]['message']['content'].strip('```json').strip('```')
            try:
                json_data = json.loads(json_data)  # Convertir de cadena a JSON
            except json.JSONDecodeError:
                print(f"Error decoding JSON content: {json_data}")
                return

            # Segunda llamada a la API
            formatted_prompt_r2 = prompt_r2.replace("{$JSON}", json.dumps(json_data))
            response_r2 = send_to_openai("gpt-4o", image_path, formatted_prompt_r2, detail_level, json.dumps(json_data))
            if 'choices' in response_r2 and response_r2['choices']:
                json_data_r2 = response_r2['choices'][0]['message']['content'].strip('```json').strip('```')
                try:
                    json_data_r2 = json.loads(json_data_r2)  # Convertir de cadena a JSON
                except json.JSONDecodeError:
                    print(f"Error decoding JSON content: {json_data_r2}")
                    return

                # Tercera llamada a la API
                formatted_prompt_r3 = prompt_r3.replace("{$JSON}", json.dumps(json_data_r2))
                response_r3 = send_to_openai("gpt-4o", image_path, formatted_prompt_r3, detail_level, json.dumps(json_data_r2))
                if 'choices' in response_r3 and response_r3['choices']:
                    json_data_r3 = response_r3['choices'][0]['message']['content'].strip('```json').strip('```')
                    try:
                        json_data_r3 = json.loads(json_data_r3)  # Convertir de cadena a JSON
                        save_data_and_manage_files(json_data_r3, image_path, data_records)
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON content: {json_data_r3}")
                else:
                    print(f"No valid response received for third call of {image_path}")
            else:
                print(f"No valid response received for second call of {image_path}")
        else:
            print(f"No valid response received for first call of {image_path}")
    except Exception as e:
        print(f"An error occurred while processing {image_path}: {str(e)}")





def describe_image(model_type, model_name, image_path, data_records, detail_level):
    if model_type == 'anthropic':
        describe_image_with_anthropic(image_path, data_records)
    elif model_type == 'openai':
        describe_image_with_openai(image_path, data_records, detail_level)
    else:
        print(f"Model '{model_name}' not recognized. Please choose 'anthropic' or 'openai'.")




def process_folder(folder_path, model_type, model_name, data_records, detail_level):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            print(f"Processing {filename} with {model_type}:{model_name} at detail level {detail_level}...")
            describe_image(model_type, model_name, image_path, data_records, detail_level)


def extract_data_to_excel(data_records):
    if not data_records:
        print("No data to export.")
        return
    df = pd.json_normalize(data_records)
    with pd.ExcelWriter('reporte_imagenes.xlsx', engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Reporte')
        worksheet = writer.sheets['Reporte']
        if 'Link' in df.columns:
            link_col = df.columns.get_loc('Link')
            for i, row in enumerate(df['Link']):
                worksheet.write_url(i+1, link_col, f"external:{row}", string=row)
    print("Image report generated successfully.")

def main():
    folders = ["images", "senales", "eventos"]
    data_records = []
    model_type, model_name, detail_level = select_model()  # Ahora maneja tres valores de retorno
    if not os.path.exists('repo_imagenes'):
        os.makedirs('repo_imagenes')
    for folder in folders:
        print(f"Processing folder: {folder}")
        process_folder(folder, model_type, model_name, data_records, detail_level)
    extract_data_to_excel(data_records)

if __name__ == "__main__":
    main()
