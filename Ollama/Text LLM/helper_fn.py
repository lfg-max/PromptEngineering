import pandas as pd

from ollama import Client
import instructions as ins
import ipywidgets as widgets
from IPython.display import display


pd.set_option('display.max_colwidth', None)


# Define the options for the dropdown menu
llm_options = [
    'deepseek-r1:8b',
    'qwen3:latest',
    'llama3.2',
    'mistral',
    'marco-o1',
    'qwen2.5-coder',
]

# Create a dropdown widget
llm_dropdown = widgets.Dropdown(
    options=llm_options,
    value=llm_options[0],  # Default value
    description='Select LLM:',
    disabled=False,
)

# Global variable to store the selected instruction
selected_llm = llm_options[0]

def llm_dropdown_widget():
    display(llm_dropdown)

# Function to get the selected LLM
def get_selected_llm(change):
    global selected_llm
    selected_llm = change['new']
    return selected_llm
    # print(f"Selected LLM: {selected_llm}")

# Attach the function to the dropdown widget
llm_dropdown.observe(get_selected_llm, names='value')


# ------------

# Define the options for the dropdown menu and map them to their respective variables
instruction_options = {
    'I_1': ins.instruction_1,
    'I_2': ins.instruction_2,
    'I_3': ins.instruction_3,
    'I_4': ins.instruction_4,
    'I_5': ins.instruction_5
}

# Create a dropdown widget
instruction_dropdown = widgets.Dropdown(
    options=list(instruction_options.keys()),
    value='I_1',  # Default value
    description='Select Instruction:',
    disabled=False,
)

# Global variable to store the selected instruction
selected_instruction_value = instruction_options['I_1']


def instruction_dropdown_widget():
    # Display the dropdown widget
    display(instruction_dropdown)

# Function to get the selected instruction
def get_selected_instruction(change):
    global selected_instruction_value
    selected_instruction_text = change['new']
    selected_instruction_value = instruction_options[selected_instruction_text]
    print(f"Selected Instruction: {selected_instruction_value}")
    return selected_instruction_value

# Attach the function to the dropdown widget
instruction_dropdown.observe(get_selected_instruction, names='value')


# ------------





class Pompt:

    model = "llama3.2"
    instruction = ins.instruction_1

    def __init__(self, model_name=None, instruction=None):
        if model_name:
            self.model = model_name
        if instruction:
            self.instruction = instruction

    def get_data(self):
        return pd.read_csv("restaurant_reviews.csv")

    def set_model(self, model_name):
        self.model = model_name

    def set_instruction(self, instruction):
        self.instruction = instruction

    def generate_response(self,review):

        # Initialize the client
        client = Client()

        # System message explicitly instructing not to include the review text
        system_message = """
            [INST]<<SYS>>
            {}
            <</SYS>>[/INST]
        """.format(self.instruction)

        # Combine user_prompt and system_message to create the prompt
        prompt = f"{review}\n{system_message}"
        # # Generate a response from the LLaMA model with additional parameters
        # llm_response = client.chat(
        #     model=model,
        #     messages=[{"role": "user", "content": prompt}],
        #     temperature=temperature,
        #     max_tokens=max_tokens,
        #     top_p=top_p,
        #     frequency_penalty=frequency_penalty,
        #     presence_penalty=presence_penalty
        # )
        # Generate a response from the LLaMA model with additional parameters
        llm_response = client.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            options={
                        "temperature": 0,
                        "top_p": 0.9,
                        "max_tokens": 1024,
                        "presence_penalty": 0.0,
                        "frequency_penalty": 0.0,
                        "best_of": 1,
                        "n": 1,
                        "stop": ['INST']

                    }
        )



        # Extract the sentiment from the response
        message = llm_response['message']['content']
        return message


    # Function to extract sentiment from the content message
    def extract_sentiment(self, model_response):
        if 'positive' in model_response.lower():
            return 'Positive'
        elif 'negative' in model_response.lower():
            return 'Negative'
        elif 'neutral' in model_response.lower():
            return 'Neutral'
        

    # defining a function to parse the JSON output from the model
    def extract_json_data(self, json_str):
        try:
            # Find the indices of the opening and closing curly braces
            json_start = json_str.find('{')
            json_end = json_str.rfind('}')

            if json_start != -1 and json_end != -1:
                extracted_sentiment = json_str[json_start:json_end + 1]  # Extract the JSON object
                data_dict = json.loads(extracted_sentiment)
                return data_dict
            else:
                print(f"Warning: JSON object not found in response: {json_str}")
                return {}
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return {}