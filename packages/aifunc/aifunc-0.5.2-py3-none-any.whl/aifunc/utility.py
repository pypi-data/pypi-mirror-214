import openai
import time
import yaml
# check whether OPENAI_API_KEY is set in the environment vairable
import os
import requests

if not os.environ.get('OPENAI_API_KEY'):
    raise Exception('OPENAI_API_KEY is not set')


def create_ai_function(function_name,
                       instruction: str,
                       example_prompt: str | list[str],
                       example_answer: str | list[str],
                       temperature=0.7):
    # check the type of parameters
    assert isinstance(function_name, str)
    assert isinstance(instruction, str)
    if isinstance(example_prompt, str):
        assert isinstance(example_answer, str)
        example_prompt = [example_prompt]
        example_answer = [example_answer]
    elif isinstance(example_prompt, list):
        assert isinstance(example_answer, list)
        assert len(example_prompt) == len(example_answer)
        # check the type of elements in the list
        for prompt in example_prompt:
            assert isinstance(prompt, str)
        for answer in example_answer:
            assert isinstance(answer, str)

    def ai_function(real_prompt):
        messages = []
        messages.append({
            "role": "user",
            "content": instruction + example_prompt[0]
        })
        messages.append({"role": "assistant", "content": example_answer[0]})
        for prompt, answer in zip(example_prompt[1:], example_answer[1:]):
            messages.append({"role": "user", "content": prompt})
            messages.append({"role": "assistant", "content": answer})

        messages.append({"role": "user", "content": real_prompt})

        for i in range(5):
            try:
                completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                          messages=messages,
                                                          temperature=temperature)
                full_response = completion.choices[0].message.content
                return full_response
            except Exception as e:
                if i < 4:  # if it's not the last attempt
                    print(f"Attempt {i + 1} failed, retrying in 5 seconds...")
                    time.sleep(5)  # wait for 5 seconds before next attempt
                else:  # if it's the last attempt
                    print("All attempts failed.")
                    raise e  # re-raise the last exception

    ai_function.__name__ = function_name  # Set the function name
    return ai_function


def create_ai_function_from_yaml(yaml_file):
    import requests
    import yaml
    url = 'https://raw.githubusercontent.com/ZiyanWu93/sturdy-memory/main/' + yaml_file
    response = requests.get(url)
    if response.status_code == 200:
        yaml_data = response.text
        data = yaml.safe_load(yaml_data)
    else:
        print("Failed to load YAML file.")
        exit(0)
    instruction = data["instruction"]
    example_pairs = data["example_pairs"]
    properties = data["properties"]

    for example in example_pairs:
        user_content = example["user_content"]
        assistant_content = example["assistant_content"]
        example["user_content"] = str(user_content)
        example["assistant_content"] = str(assistant_content)

    def fixed_format_ai_wrapper(prompt):
        message = [{"role": "system", "content": instruction}]
        for example in example_pairs:
            user_content = example["user_content"]
            assistant_content = example["assistant_content"]
            message.append({"role": "user", "content": user_content})
            message.append({"role": "assistant", "content": assistant_content})
        message.append({"role": "user", "content": prompt})
        function_name = "print_"
        for prop in properties:
            function_name += prop + "_"
        function_name = function_name[:-1]
        function_description = "print"
        for prop in properties:
            function_description += " " + prop + ","
        function_description = function_description[:-1]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=message,
            functions=[{
                "name": function_name,
                "description": function_description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                },
            }],
            function_call="auto",
        )
        message = response["choices"][0]["message"]
        if message.get("function_call"):
            arguments = eval(message["function_call"]["arguments"])
            return arguments

    return fixed_format_ai_wrapper


def create_fixed_format_ai_function(yaml_file):
    url = 'https://raw.githubusercontent.com/ZiyanWu93/sturdy-memory/main/fixed_format/' + yaml_file
    response = requests.get(url)

    if response.status_code == 200:
        yaml_data = response.text
        data = yaml.safe_load(yaml_data)
    else:
        print("Failed to load YAML file.")
        exit(0)

    instruction = data["instruction"]
    instruction = "Here are the instructions and some examples of conversations between me and you." + instruction
    example_pairs = data["example_pairs"]
    # some examples
    instruction += " For example: " + str(example_pairs) + "." + " Now, let's start!"
    properties = data["properties"]

    def fixed_format_ai_wrapper(prompt) -> dict:
        message = [{"role": "system", "content": instruction}]
        message.append({"role": "user", "content": prompt})
        function_name = "print_parameters"
        function_description = "print the generated result from assistant, including "
        for prop in properties:
            function_description += " " + prop + ","
        function_description = function_description[:-1]
        key_list = []
        for key in properties.keys():
            key_list.append(key)
        print(key_list)
        for i in range(5):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-0613",
                    messages=message,
                    functions=[{
                        "name": function_name,
                        "description": function_description,
                        "parameters": {
                            "type": "object",
                            "properties": properties,

                        },
                        "required": key_list,
                    }],
                    function_call="auto",
                )
                response = response["choices"][0]["message"]
                if response.get("function_call"):
                    arguments = eval(response["function_call"]["arguments"])
                    for key in key_list:
                        if key not in arguments:
                            raise Exception("No function call.")
                    return arguments
                else:
                    print(response)
                    raise Exception("No function call.")
            except Exception as e:
                print(e)
                print(f"Attempt {i} failed, retrying in 1 seconds...")
                time.sleep(1)  # wait for 5 seconds before next attempt
                continue
        raise Exception(
            "Unable to execute fixed_format_ai_wrapper after 5 attempts.")

    return fixed_format_ai_wrapper
