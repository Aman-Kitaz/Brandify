from flask import Flask, render_template, request, jsonify, send_file
from utils.gpt_handler import GPTBrandAssistant
from utils.logo_generator import LogoGenerator
import os

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI and Logo Generation assistants
gpt_assistant = GPTBrandAssistant(api_key=os.getenv('OPENAI_API_KEY'))
logo_generator = LogoGenerator()

@app.route('/')
def index():
    """
    Render the main application page
    """
    return render_template('index.html')

@app.route('/start_conversation', methods=['POST'])
def start_conversation():
    """
    Initialize a new conversation and get the first question
    """
    initial_question = gpt_assistant.get_initial_question()
    conversation_id = gpt_assistant.create_conversation()
    
    return jsonify({
        'message': initial_question,
        'conversation_id': conversation_id
    })

@app.route('/process_response', methods=['POST'])
def process_response():
    """
    Process user responses during the brand discovery process
    """
    try:
        data = request.json
        conversation_id = data.get('conversation_id')
        user_response = data.get('user_response')

        print(f"Processing user response: {user_response}")

        # Process the user's response and get the next step
        next_step = gpt_assistant.process_response(
            conversation_id, 
            user_response
        )

        print(f"Next step: {next_step}")
        return jsonify(next_step)
    
    except Exception as e:
        print(f"Error in process_response: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/generate_logo', methods=['POST'])
def generate_logo():
    """
    Generate a logo based on brand details
    """
    try:
        data = request.json
        brand_details = data.get('brand_details')
        
        print(f"Generating logo with details: {brand_details}")
        
        # Generate logo prompt using GPT
        logo_prompt = gpt_assistant.generate_logo_prompt(brand_details)
        print(f"Generated prompt: {logo_prompt}")
        
        # Generate logo using DeepFloyd
        brand_name = brand_details.get('brand_name')
        logo_path = logo_generator.generate(logo_prompt, brand_name)

        return jsonify({
            'logo_path': logo_path,
            'prompt_used': logo_prompt
        })
    
    except Exception as e:
        print(f"Error generating logo: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/download_logo/<path:filename>')
def download_logo(filename):
    """
    Provide a route to download the generated logo
    """
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        print(f"Error downloading logo: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)