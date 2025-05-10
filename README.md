# Brandify
Brandify is an AI-powered tool designed to simplify the branding process. It generates unique brand names and logos based on user input. By leveraging OpenAI’s GPT-4o (Mini) API for natural language processing and DeepFloyd’s image generation capabilities, Brandify provides creative branding solutions in seconds.

## Features

- **Generate Unique Brand Names** 
- **AI-Generated Logos**
- **Interactive Web Interface** 
- **Modular Backend**
- **Organized Project Structure** 

---

## Project Structure

```
Brandify/
│
├── application.py       # Main backend app logic
├── gpt_handler.py       # Handles communication with GPT API
├── logo_generator.py    # Integrates DeepFloyd for logo creation
├── index.html           # Frontend HTML file
├── script.js            # Frontend interactivity
├── styles.css           # Frontend styling
├── README.md            # Project documentation (you’re reading it!)
├── API.ipynb            # Notebook for testing GPT API functionality
├── DeepFloyd.ipynb      # Notebook for testing DeepFloyd integration
└── requirements.txt     # Dependencies for the project
```

---

## How It Works

1. **User Input:** The frontend collects user input, such as business type or theme.
![PHOTO-2025-05-10-16-52-00](https://github.com/user-attachments/assets/bb68508b-366a-4c3f-a424-4c270d3ce87e)

2. **Backend Processing:**
   - `gpt_handler.py` uses the GPT-4o API to generate a brand name.
   - `logo_generator.py` integrates DeepFloyd to create a logo based on the generated brand name.
3. **Display Results:** The results are sent back to the frontend and rendered in the browser.
Here’s an example of a generated brand result:
![PHOTO-2025-04-04-19-21-10](https://github.com/user-attachments/assets/03c1196e-cc8e-4e61-9e47-60f26c3db435)
![PHOTO-2025-04-04-19-21-10 2](https://github.com/user-attachments/assets/537421f1-fd11-4921-93d5-cfa95de557ea)

---

## Models Used

- **OpenAI GPT-4o API:** For generating brand names.
- **DeepFloyd IF Model:** For creating AI-generated logos. https://huggingface.co/DeepFloyd/IF-II-L-v1.0
- **Python & Flask:** Backend logic and optional web server.
- **HTML, CSS, JavaScript:** Frontend development.

---

## Author

- **Aman Kitaz**
- **Nour El Houda**
- **Shatha**

 ---

## License 
This project is licensed under the MIT License.
  
