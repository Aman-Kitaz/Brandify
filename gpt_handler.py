from openai import OpenAI
import uuid

class GPTBrandAssistant:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.conversations = {}
        
        # Simplified questions
        self.questions = [
            {
                'stage': 'industry',
                'question': 'What industry is your brand in?',
                'options': [
                    'Technology', 
                    'Healthcare', 
                    'Fashion', 
                    'Food & Beverage', 
                    'Education', 
                    'Finance', 
                    'Entertainment'
                ]
            },
            {
                'stage': 'theme',
                'question': 'Choose your logo style:',
                'options': [
                    'Minimalist', 
                    'Professional', 
                    'Playful'
                ]
            },
            {
                'stage': 'color_scheme',
                'question': 'Choose a color scheme:',
                'options': [
                    'Blue', 
                    'Black', 
                    'Green'
                ]
            }
        ]

        # Fallback suggestions dictionary
        self.fallback_suggestions = {
            'technology': ['1. TechPro', '2. DigiCore', '3. ByteWise', '4. InnoTech', '5. SmartCore'],
            'healthcare': ['1. HealthHub', '2. CarePlus', '3. MediCare', '4. VitalPro', '5. WellCore'],
            'fashion': ['1. StyleHub', '2. TrendSet', '3. ModePro', '4. FashionCore', '5. ChicPro'],
            'food & beverage': ['1. FreshBite', '2. TastePro', '3. FlavorHub', '4. FoodCore', '5. YumPro'],
            'education': ['1. LearnPro', '2. EduCore', '3. SkillHub', '4. BrainPro', '5. TeachSmart'],
            'finance': ['1. FinCore', '2. WealthPro', '3. MoneyHub', '4. CapitalPro', '5. InvestSmart'],
            'entertainment': ['1. FunHub', '2. PlayCore', '3. JoyPro', '4. EntertainPro', '5. FunZone']
        }

    def create_conversation(self):
        conversation_id = str(uuid.uuid4())
        self.conversations[conversation_id] = {
            'stage': 'initial',
            'brand_details': {},
            'current_question_index': -1,
            'used_gpt_suggestions': False
        }
        return conversation_id

    def get_initial_question(self):
        return "Do you have a name for your brand/company?"

    def get_next_question(self, conversation_id):
        conversation = self.conversations.get(conversation_id)
        
        conversation['current_question_index'] += 1
        
        if conversation['current_question_index'] < len(self.questions):
            current_question = self.questions[conversation['current_question_index']]
            return {
                'question': current_question['question'],
                'options': current_question['options'],
                'stage': current_question['stage']
            }
        
        if conversation['current_question_index'] == len(self.questions):
            conversation['stage'] = 'brand_name_selection'
            brand_suggestions = self.generate_brand_name_suggestions(conversation['brand_details'])
            
            return {
                'message': 'Based on your responses, here are 3 brand name suggestions:\n(Type "more" if you want to see different suggestions)',
                'suggestions': brand_suggestions,
                'stage': 'brand_name_selection'
            }

    def generate_brand_name_suggestions(self, brand_details):
        try:
            industry = brand_details.get('industry', '').lower()
            theme = brand_details.get('theme', '').lower()
            
            prompt = f"""
            Generate 3 short and simple brand names for a {industry} company.
            The brand style is {theme}.
            
            Requirements:
            - Maximum 2 words
            - Easy to pronounce
            - Related to {industry}
            - Simple and memorable
            - No complex or made-up words
            
            Format: 1. Name
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a brand naming expert. Generate simple, practical names."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            suggestions_text = response.choices[0].message.content
            suggestions = suggestions_text.split('\n')
            
            cleaned_suggestions = [
                suggestion.strip() 
                for suggestion in suggestions 
                if suggestion.strip() and suggestion.strip()[0].isdigit()
            ]
            
            return cleaned_suggestions[:3]
            
        except Exception as e:
            print(f"Error generating brand names: {e}")
            return ['1. ProBrand', '2. CoreHub', '3. BizPro']

    def generate_logo_prompt(self, brand_details):
        try:
            # For custom prompt (when user answered "yes")
            if brand_details.get('custom_prompt'):
                return brand_details['custom_prompt']
            
            # For generated prompt (when user answered "no")
            brand_name = brand_details.get('brand_name', '')
            theme = brand_details.get('theme', '')
            colors = brand_details.get('color_scheme', '')
            industry = brand_details.get('industry', '')
            
            # Create a more specific prompt
            prompt = f"a {theme.lower()} style logo design for {brand_name}, a {industry.lower()} brand, using {colors.lower()} color scheme"
            print(f"Generated logo prompt: {prompt}")  # Debug print
            return prompt
            
        except Exception as e:
            print(f"Error generating logo prompt: {e}")
            return f"a logo for {brand_details.get('brand_name', 'Brand')}"

    def process_response(self, conversation_id, user_response):
        print(f"Processing response: {user_response}")
        print(f"Current conversation state: {self.conversations.get(conversation_id)}")  # Debug print
        
        conversation = self.conversations.get(conversation_id)
        if not conversation:
            return {'error': 'Conversation not found'}
        
        # Initial stage handling
        if conversation['stage'] == 'initial':
            if user_response.lower() == 'yes':
                conversation['stage'] = 'brand_name_input'
                return {
                    'message': 'Please enter your brand name:',
                    'stage': 'brand_name_input'
                }
            else:
                return self.get_next_question(conversation_id)
        
        # Handle brand name input stage
        if conversation['stage'] == 'brand_name_input':
            conversation['brand_details']['brand_name'] = user_response
            conversation['stage'] = 'prompt_input'
            return {
                'message': 'Please enter your logo prompt (e.g., "a professional logo for Trade using blue colors"):',
                'stage': 'prompt_input'
            }
        
        # Handle prompt input stage
        if conversation['stage'] == 'prompt_input':
            conversation['brand_details']['custom_prompt'] = user_response
            conversation['stage'] = 'logo_generation'
            return {
                'message': 'Thank you! Generating your logo with your custom prompt.',
                'stage': 'logo_generation',
                'next_step': 'generate_logo'
            }
        
        # Handle multiple-choice responses
        if conversation['current_question_index'] >= 0 and conversation['current_question_index'] < len(self.questions):
            current_question = self.questions[conversation['current_question_index']]
            # Store the actual selected option, not just the number
            selected_option = self.questions[conversation['current_question_index']]['options'][int(user_response) - 1]
            conversation['brand_details'][current_question['stage']] = selected_option
            print(f"Stored {current_question['stage']}: {selected_option}")  # Debug print
            
            return self.get_next_question(conversation_id)
        
        # Handle brand name selection stage
        if conversation['stage'] == 'brand_name_selection':
            # Check if user wants new suggestions
            if user_response.lower() in ['new', 'try again', 'more', 'other']:
                industry = conversation['brand_details'].get('industry', '').lower()
                print(f"Getting fallback suggestions for industry: {industry}")  # Debug print
                
                # Get the correct fallback suggestions based on stored industry
                fallback = self.fallback_suggestions.get(industry.lower(), 
                    ['1. ProBrand', '2. CoreHub', '3. BizPro', '4. SmartPro', '5. ElitePro'])
                
                return {
                    'message': 'Here are some alternative suggestions:',
                    'suggestions': fallback,
                    'stage': 'brand_name_selection'
                }
            
            # If user selected a name, proceed with logo generation
            conversation['brand_details']['brand_name'] = user_response
            conversation['stage'] = 'logo_generation'
            
            return {
                'message': 'Thank you! Generating your logo...',
                'stage': 'logo_generation',
                'next_step': 'generate_logo'
            }
        
        return {
            'message': 'Something went wrong. Please start over.',
            'stage': 'initial'
        }