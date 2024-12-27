import tkinter as tk
from tkinter import scrolledtext
import threading
from openai import OpenAI

# Initialize the OpenAI client for interacting with the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

class ChatUI:
    def __init__(self, master):
        self.master = master
        master.title("Chat with Local LLM")
        
        # Chat area
        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=40, height=20)
        self.chat_area.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.chat_area.config(state='disabled')

        # Entry for user input
        self.entry = tk.Entry(master, width=30)
        self.entry.grid(row=1, column=0, padx=5, pady=5)
        self.entry.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=5, pady=5)

        # Chat history for the session
        self.history = [
            {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
            {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
        ]

    def send_message(self, event=None):
        message = self.entry.get().strip()
        if message:
            self.display_message("You", message)
            self.entry.delete(0, tk.END)  # Clear the entry after sending
            
            # Start a thread to handle the LLM response
            threading.Thread(target=self.get_llm_response, args=(message,)).start()

    def display_message(self, sender, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: ")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)
        self.display_char_by_char(message)

    def display_char_by_char(self, message):
        for char in message:
            self.chat_area.config(state='normal')
            self.chat_area.insert(tk.END, char)
            self.chat_area.config(state='disabled')
            self.chat_area.update_idletasks()  # Force an update of the GUI
            self.master.after(20)  # Small delay to simulate typing
        self.chat_area.insert(tk.END, "\n\n")  # New line after each message

    def get_llm_response(self, message):
        self.history.append({"role": "user", "content": message})
        
        completion = client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-7B-Instruct-GGUF",
            messages=self.history,
            temperature=0.7,
            stream=True,
        )
        
        full_response = ""
        
        for chunk in completion:
            if chunk.choices[0].delta.content:
                new_char = chunk.choices[0].delta.content
                full_response += new_char
                self.master.after(0, lambda c=new_char: self.display_char_by_char(c))
        
        self.history.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    root = tk.Tk()
    chat_ui = ChatUI(root)
    root.mainloop()