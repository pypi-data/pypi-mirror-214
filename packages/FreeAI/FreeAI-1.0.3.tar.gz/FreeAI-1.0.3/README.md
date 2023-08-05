# FreeAI: An Advanced GPT-based Text Generation Package

<!-- ![FreeAI Logo](/img/freeai_logo.png)-->

FreeAI is a powerful Python package that utilizes the advanced capabilities of GPT-3/4 (Generative Pre-trained Transformer) models for text generation. It allows users to generate creative and context-aware text based on a given prompt. Whether you need to generate code snippets, creative writing pieces, or technical documentation, FreeAI has got you covered.

## Features

- **Advanced GPT Text Generation**: FreeAI leverages state-of-the-art GPT models to generate high-quality and contextually relevant text.
- **Flexible Prompt Customization**: Users can easily provide their own prompts to guide the text generation process.
- **Dynamic Temperature Control**: Adjust the temperature parameter to control the randomness and creativity of the generated text.
- **Customizable Max Tokens**: Set the maximum number of tokens to limit the length of the generated text.
- **Error Handling and Fallback**: FreeAI gracefully handles errors during the API request and switches to a fallback model if necessary.
- **Professional and Easy-to-Use API**: The API design of FreeAI makes it straightforward to integrate into your own projects.

## Installation

You can install FreeAI using pip:

```shell
pip install FreeAI
```

Make sure you have Python 3.6 or later installed.

## Usage

Here's a basic example of how to use FreeAI:

```python
import FreeAI

prompt = "write a blog post on Python Programming"
temperature = 0.7  # Set custom temperature (optional)
max_tokens = 1024  # Set custom max_tokens (optional)

response = FreeAI.generate(prompt, temperature=temperature, max_tokens=max_tokens)
print(response)
```

By default, FreeAI uses a temperature of 0.7 and a max_tokens value of 1024 if not specified by the user.

## Error Handling

FreeAI includes robust error handling to ensure a smooth user experience. If the provided max_tokens or temperature values are outside the allowed range, a `ValueError` will be raised, providing an informative error message. Make sure to validate your input values before calling the `generate` function.

## Contributing

We welcome contributions from the open source community to improve and enhance FreeAI. If you have any bug fixes, feature requests, or suggestions, please open an issue or submit a pull request on our GitHub repository.

## License

FreeAI is released under the MIT License. See the [LICENSE](https://github.com/mir-ashiq/FreeAI/blob/main/LICENSE) file for more details.

---

FreeAI is developed and maintained by Ashiq Hussain(https://github.com/mir-ashiq). We are dedicated to providing advanced AI solutions to empower developers and enhance their productivity. If you have any questions or need support, feel free to reach out to us at imseldrith@gmail.com.

Happy text generation with FreeAI!