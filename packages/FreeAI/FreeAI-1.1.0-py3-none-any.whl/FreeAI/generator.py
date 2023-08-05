import requests
from .logger import logger
from .memory import memory
from datetime import datetime
from dateutil import parser

BASE_URL = 'https://gpt4.gravityengine.cc/api/openai/'
ERROR_BASE_URL = 'https://gptdidi.com/api/openai/'
ARGUMENTS = '/v1/chat/completions'
HEADERS = {'Content-Type': 'application/json'}


def generate(prompt, max_tokens, temperature):
    if prompt is None:
        raise ValueError("Please enter a prompt.")
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
                response = choices[0]['message']['content']
                memory.save(prompt, response)  # Save conversation to memory
                return response
    except requests.exceptions.RequestException as error:
        logger.error('Error making the request, retrying with fallback model')
        endpoint = ERROR_BASE_URL + ARGUMENTS
        with session.post(endpoint, headers=HEADERS, json=data) as response:
            response_data = response.json()
            choices = response_data.get('choices')
            if choices:
                response = choices[0]['message']['content']
                memory.save(prompt, response)  # Save conversation to memory
                return response


def main():
    prompt = memory.get_last_prompt()  # Get the last prompt from memory
    max_tokens = 4096  # Default value if not specified by the user
    temperature = 0.7  # Default value if not specified by the user

    try:
        response = generate(prompt, max_tokens, temperature)
        logger.info(f"Response: {response}")
    except ValueError as e:
        logger.error(f"Error: {str(e)}")


if __name__ == '__main__':
    main()
    