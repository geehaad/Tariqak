import requests
import json

def fetch_model_tags(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        models = data.get('models', [])
        model_names = [model['name'] for model in models]
        model_prompts = {model['name']: model.get('prompt', '') for model in models}
        return model_names, model_prompts
    except Exception as e:
        print(f"Error fetching model tags: {e}")
        return [], {}

def generate_output(url, selected_model, prompt, temperature, top_p, top_k):
    try:
        payload = {
            'model': selected_model,
            'prompt': prompt,
            'options': {
                'Temperature': temperature,
                'top_p': top_p,
                'top_k': top_k,
                'use_mlock': True
            }
        }
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()
        
        full_response = ''
        for line in response.iter_lines(decode_unicode=True):
            if line:
                try:
                    json_line = json.loads(line)
                    if json_line.get('done', False):
                        full_response += json_line.get('response', '')
                        break
                    full_response += json_line.get('response', '')
                except json.JSONDecodeError:
                    continue  # Skip lines that are not valid JSON

        return full_response
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"
    except Exception as e:
        return f"Error generating output: {e}"
