import chainlit as cl
import ollama

@cl.on_chat_start
async def start_chat():
    cl.user_session.set(
        "interaction",
        [
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            }
        ],
    )

    # Create a dropdown for model selection
    model_dropdown = cl.Dropdown(
        id="model_dropdown",
        label="Select Model",
        options=[
            {"label": "Llama 3.2", "value": "llama3.2"},
            {"label": "Llama 3.2 Vision", "value": "llama3.2-vision"},
            # Add more models as needed
        ],
        default="llama3.2"
    )

    await model_dropdown.send()

    msg = cl.Message(content="")

    start_message = "Hello, I'm your 100% local alternative to ChatGPT. How can I help you today?"

    for token in start_message:
        await msg.stream_token(token)

    await msg.send()

@cl.step(type="tool")
async def tool(input_message, image=None):

    interaction = cl.user_session.get("interaction")

    # Get the selected model from the dropdown
    selected_model = cl.user_session.get("model_dropdown")

    if image:
        interaction.append({"role": "user",
                            "content": input_message,
                            "images": image})
    else:
        interaction.append({"role": "user",
                            "content": input_message})
    
    response = ollama.chat(model=selected_model,
                           messages=interaction) 
    
    interaction.append({"role": "assistant",
                        "content": response.message.content})
    
    return response


@cl.on_message 
async def main(message: cl.Message):

    images = [file for file in message.elements if "image" in file.mime]

    if images:
        tool_res = await tool(message.content, [i.path for i in images])

    else:
        tool_res = await tool(message.content)

    msg = cl.Message(content="")

    for token in tool_res.message.content:
        await msg.stream_token(token)

    await msg.send()