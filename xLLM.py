# file: gui_chat_processor.py

import openai
import csv
import os
import sys
import importlib
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox, simpledialog

client = None  # Global client

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

def process_csv(input_path, output_path, model, log_widget):
    try:
        log_widget.config(state="normal")
        with open(input_path, encoding="utf-8") as infile, open(output_path, "w", newline="", encoding="utf-8") as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            headers = next(reader)
            writer.writerow(headers + ["rating", "full_response"])
            for row in reader:
                if len(row) < 3:
                    continue
                idx, prompt, fmt = row[0], row[1], row[2]
                try:
                    resp = get_response(f"{prompt}\n{fmt}", model)
                    writer.writerow(row + [resp])
                    log_widget.insert(tk.END, f"{idx}: {resp}\n")
                    log_widget.see(tk.END)
                except Exception as e:
                    log_widget.insert(tk.END, f"Error {idx}: {e}\n")
        log_widget.config(state="disabled")
        messagebox.showinfo("Done", "CSV processing completed.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

class App:
    def __init__(self, root):
        self.root = root
        root.title("Chat Processor GUI")
        self.models = get_available_models()
        self.model_var = tk.StringVar(value=self.models[0])

        ttk.Label(root, text="Choose model:").grid(row=0, column=0, sticky="w")
        ttk.Combobox(root, values=self.models, textvariable=self.model_var, width=40).grid(row=0, column=1)

        ttk.Button(root, text="Insert API Key", command=self.set_api_key).grid(row=1, column=0)
        ttk.Button(root, text="CSV Mode", command=self.csv_mode).grid(row=1, column=1)
        ttk.Button(root, text="Interactive Mode", command=self.interactive_mode).grid(row=1, column=2)

        self.log = scrolledtext.ScrolledText(root, width=80, height=20, state="disabled")

    def set_api_key(self):
        global client
        key_path = filedialog.askopenfilename(title="Select a text file with your OpenAI API Key")
        if key_path:
            with open(key_path, "r") as f:
                key = f.read().strip()
                client = openai.OpenAI(api_key=key)
                messagebox.showinfo("API Key Set", "API key loaded successfully.")

    def csv_mode(self):
        if client is None:
            messagebox.showwarning("API Key Required", "Please set your OpenAI API key first.")
            return
        inp = filedialog.askopenfilename(title="Select input CSV")
        if not inp:
            return
        out = filedialog.asksaveasfilename(title="Select output CSV", defaultextension=".csv")
        if not out:
            return
        self.log.grid(row=2, column=0, columnspan=3, pady=10)
        self.log.config(state="normal")
        self.log.delete("1.0", tk.END)
        self.log.config(state="disabled")
        process_csv(inp, out, self.model_var.get(), self.log)

    def interactive_mode(self):
        if client is None:
            messagebox.showwarning("API Key Required", "Please set your OpenAI API key first.")
            return
        self.root.withdraw()
        win = tk.Toplevel()
        win.title("Interactive Q&A")

        container = tk.Frame(win)
        container.grid(row=0, column=0, padx=10, pady=10)

        input_frame = tk.Frame(container)
        input_frame.grid(row=0, column=0, sticky="nw")
        tk.Label(input_frame, text="Enter your prompt below:").pack(anchor="w")

        txt_in = scrolledtext.ScrolledText(input_frame, width=60, height=10)
        txt_in.pack()

        button_frame = tk.Frame(container)
        button_frame.grid(row=0, column=1, padx=10, sticky="n")
        send_btn = ttk.Button(button_frame, text="Send Prompt")
        cancel_btn = ttk.Button(button_frame, text="Cancel Prompt")
        reset_btn = ttk.Button(button_frame, text="Reset")
        back_btn = ttk.Button(button_frame, text="Back to Main Menu")
        send_btn.pack(fill="x", pady=2)
        cancel_btn.pack(fill="x", pady=2)
        reset_btn.pack(fill="x", pady=2)
        back_btn.pack(fill="x", pady=10)

        tk.Label(container, text="Model response:").grid(row=1, column=0, columnspan=2)
        txt_out = scrolledtext.ScrolledText(container, width=80, height=20)
        txt_out.grid(row=2, column=0, columnspan=2)

        def ask():
            txt_in.config(state="disabled")
            prompt = txt_in.get("1.0", tk.END).strip()
            if not prompt:
                messagebox.showwarning("Empty Prompt", "Please enter a prompt before clicking Send.")
                txt_in.config(state="normal")
                return
            try:
                resp = get_response(prompt, self.model_var.get())
                txt_out.insert(tk.END, f"> {prompt}\n{resp}\n\n")
                txt_out.see(tk.END)
            except Exception as e:
                txt_out.insert(tk.END, f"Error: {e}\n")
            txt_in.config(state="normal")
            txt_in.delete("1.0", tk.END)

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

        send_btn.config(command=ask)
        cancel_btn.config(command=cancel)
        reset_btn.config(command=reset)
        back_btn.config(command=go_back)

        def on_enter_key(event):
            ask()
            return "break"

        txt_in.bind("<Return>", on_enter_key)
        win.protocol("WM_DELETE_WINDOW", go_back)

def main():
    root = tk.Tk()
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
