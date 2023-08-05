import requests

BASE_URL = 'https://gpt4.gravityengine.cc/api/openai/'
ERROR_BASE_URL = 'https://gptdidi.com/api/openai/'
ARGUMENTS = '/v1/chat/completions'
HEADERS = {'Content-Type': 'application/json'}


def generate(prompt, max_tokens, temperature):
    if not (50 <= max_tokens <= 16000):
        raise ValueError("Invalid value for max_tokens. It must be between 50 and 16000.")
    if not (0 <= temperature <= 1):
        raise ValueError("Invalid value for temperature. It must be between 0 and 1.")

    session = requests.Session()
    endpoint = BASE_URL + ARGUMENTS
    data = {
        'model': 'gpt-3.5-turbo-16k-0613',
        'messages': [
            {"role": "system", "content": prompt},
        ],
        'max_tokens': max_tokens,
        'temperature': temperature
    }

    try:
        with session.post(endpoint, headers=HEADERS, json=data) as response:
            response_data = response.json()
            choices = response_data.get('choices')
            if choices:
                return choices[0]['message']['content']
    except requests.exceptions.RequestException as error:
        print('Error making the request, retrying with fallback model')
        endpoint = ERROR_BASE_URL + ARGUMENTS
        with session.post(endpoint, headers=HEADERS, json=data) as response:
            response_data = response.json()
            choices = response_data.get('choices')
            if choices:
                return choices[0]['message']['content']


def main():
    prompt = "write advanced greeting Python code"
    max_tokens = 4096  # Default value if not specified by the user
    temperature = 0.7  # Default value if not specified by the user

    try:
        response = generate(prompt, max_tokens, temperature)
        print(response)
    except ValueError as e:
        print(f"Error: {str(e)}")

main()
