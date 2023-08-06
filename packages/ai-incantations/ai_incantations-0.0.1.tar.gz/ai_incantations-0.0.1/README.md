# ai-incantations
 
ai-incantations is a versatile Python library that allows you to easily read, deserialize, and manage structured text files containing prompts and their contents. With its simple interface, ai-incantations enables you to access prompt contents using dot notation and seamlessly perform interpolation of placeholders within the contents.

The library offers an intuitive approach to handling text files with a specific format and is particularly useful for natural language processing tasks, chatbot frameworks, and other applications that require dynamic content management.

## Features
- File deserialization: Automatically reads and deserializes the input file, storing contents in a structured, dictionary-like format.
- Dot notation: Allows access to prompt contents through dot notation, making the syntax clean and easy to read.
- Interpolation: Supports interpolation of placeholders within prompt contents, making it simple to dynamically insert values.
- Flexible: Can easily be extended and adapted for use in various applications.

## Installation
 
To install ai-incantations, simply run the following command:
```
pip install ai_incantations
```
or, to install from source, run:
```
pip install git+https://github.com/supreethrao99/ai-incantations.git
```  
 
## Usage
 
Below is a step-by-step guide on how to use Incantation.
1. Create an input file
 Create a text file with your desired prompts and content. The format should follow these guidelines:
    - Each prompt category should be on a new line and end with a colon.
    - The content for each prompt should be indented with a single space and have a key and value separated by a colon.
    - If the content includes multiple lines or placeholders, use triple quotes (""") to enclose the text.

    Example input file (input.llmp):

    **Note that the prompt is on a new line after the `"""` (tripe quotes)**
    ```llmp
    gpt_4_prompt:  
        system_prompt: """
                You are an AI assistant that helps people find information. 
              """  
        user_prompt: """
            tell me something in common between ${city1} and ${city2}.
            """
    ```
  
 
2. Initialize Incantation with the input file

    Create a Incantation instance by providing the path to your input file.
    ```python
    prompts = Incantation("input.llmp")  
    ```
 
3. Access prompt contents using dot notation
    Retrieve content for a specific prompt using dot notation.
    ```python
    system_prompt = prompts.gpt_4_prompt.system_prompt 
    user_prompt = prompts.gpt_4_prompt.user_prompt
    ```
 
 
4. Interpolate placeholders in the content
 
    Perform interpolation for placeholders in the content by providing a dictionary with the corresponding values.
    ```python
    interpolated_system_prompt = prompts.interpolate(system_prompt, {})

    interpolated_user_prompt = prompts.interpolate(
        user_prompt, {"city1": "New York", "city2": "London"}
        )
    ``` 
 
## Example
Here's a complete example of using Incantation to read, access, and interpolate content from a file.
```python
from incantation import Incantation  

# Create a Incantation instance  
prompts = Incantation("input.llmp")  

# Access content using dot notation  
system_prompt = prompts.gpt_4_prompt.system_prompt 
user_prompt = prompts.gpt_4_prompt.user_prompt  

# Perform interpolation  
interpolated_system_prompt = prompts.interpolate(
    system_prompt, {}
    )

interpolated_user_prompt = prompts.interpolate(
    user_prompt, {"city1": "New York", "city2": "London"}
    )  

print(interpolated_system_prompt)  
# Output: You are an AI assistant that helps people find information.

print(interpolated_user_prompt)  
# Output: tell me something in common between New York and London.
```  
 
## License
 
Incantation is released under the Apache 2.0 License.