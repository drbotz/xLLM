# xLLM – Interactive Chat Processor GUI for OpenAI Models

**xLLM** is a powerful, user-friendly Python GUI application that enables both interactive and batch-mode communication with OpenAI’s GPT models (e.g., `gpt-4`, `gpt-4o`, `gpt-3.5-turbo`). Designed with `tkinter`, it allows researchers, developers, and analysts to process large-scale prompt datasets via CSV or chat directly in a sleek graphical interface.

---

## 🚀 Features

- ✅ **Secure API Key Handling** via file-based input (no hardcoded keys)
- ✅ **Interactive Chat Mode** with real-time prompt submission & model responses
- ✅ **Batch CSV Mode**: automate thousands of prompts/responses to CSV
- ✅ **Supports latest OpenAI models**: `gpt-4`, `gpt-4-turbo`, `gpt-4o`, `gpt-3.5-turbo`
- ✅ **Clear GUI Layout** using `tkinter`
- ✅ **Log Console** (only shown in CSV mode)
- ✅ **Prompt editing restrictions while response is generating**
- ✅ **Back-to-main navigation and window cleanup**
- ✅ **Multi-platform compatible**: tested on macOS, Windows, Linux

---

## 📁 Folder Structure

```
xLLM/
│
├── gui_chat_processor.py     # Main Python app file
├── README.md                 # This file
├── example_prompts.csv       # (Optional) Sample input
├── .gitignore                # Ignores unnecessary files
├── requirements.txt          # Python dependencies
└── api_key.txt               # (Optional) Your API key file (never commit)
```

---

## 🖥️ How to Use

### 1. 📦 Install Requirements

```bash
pip install openai tkinter
```

### 2. 🔐 Set Up API Key

Save your OpenAI API key in a `.txt` file (e.g., `api_key.txt`).

In the GUI:
- Click **Insert API Key**
- Select your `.txt` file

### 3. 🧠 Choose a Mode

You will see two options in the main GUI:

#### 🗃️ CSV Mode
- Select an input CSV (format: `index, prompt, format`)
- Select an output CSV destination
- Each row is processed by the selected OpenAI model
- Outputs include a model rating & full response

#### 💬 Interactive Mode
- Type your prompt in the text box
- Click **Send Prompt**
- Response appears below
- Use **Cancel**, **Reset**, or **Back to Main Menu** as needed

---

## 📝 CSV Input Format

Your CSV file should contain:

| index | prompt                      | format                  |
|-------|-----------------------------|--------------------------|
| 1     | What's the capital of Japan?| Return just the city name |

The app will generate:

| index | prompt                      | format                  | rating | full_response |
|-------|-----------------------------|--------------------------|--------|----------------|

---

## ✅ Best Practices

- Keep prompts short and clear in CSV for best response accuracy
- Avoid sending API keys directly in code or uploading to GitHub
- Use `gpt-4o` for best speed/cost/performance balance as of 2025

---

## 🔒 Security

- The OpenAI API key is loaded from a file selected via GUI
- No API keys are saved or embedded in the source code
- `.gitignore` should include `api_key.txt` or `.env`

---

## 🧬 Requirements

- Python 3.8+
- `openai>=1.0`
- `tkinter` (comes with most Python installations)

---

## 📄 License

MIT License — free to use, fork, and build upon.

---

## ✨ Credits

Developed by [drbotz](https://github.com/drbotz)

---

## 🔗 Links

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Tkinter Docs](https://docs.python.org/3/library/tkinter.html)
