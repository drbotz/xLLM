import openai
import csv
import os
import sys
import importlib
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox, simpledialog

client = None

def get_available_models():
    return ["gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-3.5-turbo"]

def get_openai_response(prompt, model):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def get_response(prompt, model):
    return get_openai_response(prompt, model)

class App:
    def __init__(self, root):
        self.root = root
        root.title("xLLM - Main GUI")
        self.models = get_available_models()

        main = ttk.Frame(root, padding=20)
        main.grid(row=0, column=0, sticky="nsew")
        root.resizable(False, False)

        ttk.Label(main, text="Choose models:").pack(anchor="w", pady=(0, 5))

        self.model_listbox = tk.Listbox(main, selectmode="multiple", height=4, exportselection=False)
        for model in self.models:
            self.model_listbox.insert(tk.END, model)
        self.model_listbox.pack(fill="x", pady=(0, 15))

        button_row = ttk.Frame(main)
        button_row.pack(fill="x", pady=5)
        ttk.Button(button_row, text="CSV Mode", command=self.csv_mode).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(button_row, text="Interactive Mode", command=self.interactive_mode).pack(side="left", expand=True, fill="x", padx=(5, 0))

        ttk.Button(main, text="Insert API Key", command=self.set_api_key).pack(fill="x", pady=(15, 0))

        self.log = scrolledtext.ScrolledText(root, width=80, height=20, state="disabled")

    def get_selected_models(self):
        return [self.models[i] for i in self.model_listbox.curselection()]

    def set_api_key(self):
        global client
        key_path = filedialog.askopenfilename(title="Select a text file with your OpenAI API Key")
        if key_path:
            with open(key_path, "r") as f:
                key = f.read().strip()
                client = openai.OpenAI(api_key=key)
                messagebox.showinfo("API Key Set", "API key loaded successfully.")

    def csv_mode(self):
        messagebox.showinfo("CSV Mode", "CSV mode not modified in this version.")

    def interactive_mode(self):
        if client is None:
            messagebox.showwarning("API Key Required", "Please set your OpenAI API key first.")
            return

        selected_models = self.get_selected_models()
        if not selected_models:
            messagebox.showwarning("Model Required", "Please select at least one model.")
            return
        self.root.withdraw()
        win = tk.Toplevel()
        win.title("Interactive Q&A")

        container = tk.Frame(win)
        container.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(container, text="Enter your prompt below:").grid(row=0, column=0, sticky="w")
        txt_in = scrolledtext.ScrolledText(container, width=80, height=8)
        txt_in.grid(row=1, column=0, columnspan=2)

        selected_label = tk.Label(container, text=f"Selected Models: {', '.join(selected_models)}")
        selected_label.grid(row=2, column=0, sticky="w", pady=(5, 5))

        txt_out = scrolledtext.ScrolledText(container, width=100, height=20)
        txt_out.grid(row=3, column=0, columnspan=2)

        def ask():
            prompt = txt_in.get("1.0", tk.END).strip()
            if not prompt:
                messagebox.showwarning("Empty Prompt", "Please enter a prompt before clicking Send.")
                return
            txt_in.delete("1.0", tk.END)
            for model in selected_models:
                try:
                    resp = get_response(prompt, model)
                    txt_out.insert(tk.END, f"[{model}]\n> {prompt}\n{resp}\n\n")
                except Exception as e:
                    txt_out.insert(tk.END, f"[{model}] Error: {e}\n\n")
            txt_out.see(tk.END)

        def cancel():
            txt_in.delete("1.0", tk.END)
            txt_out.insert(tk.END, "Prompt cancelled.\n")
            txt_out.see(tk.END)

        def reset():
            txt_in.config(state="normal")
            txt_in.delete("1.0", tk.END)
            txt_out.delete("1.0", tk.END)

        def go_back():
            win.destroy()
            self.root.deiconify()

        button_frame = tk.Frame(container)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(button_frame, text="Send Prompt", command=ask).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel Prompt", command=cancel).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Reset", command=reset).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Back to Main Menu", command=go_back).pack(side="left", padx=5)

        win.protocol("WM_DELETE_WINDOW", go_back)

def main():
    root = tk.Tk()
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
