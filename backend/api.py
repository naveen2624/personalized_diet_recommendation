# backend/api.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime
import logging

# Suppress gRPC warnings
os.environ['GRPC_ENABLE_FORK_SUPPORT'] = '1'
os.environ['GRPC_POLL_STRATEGY'] = 'poll'
logging.getLogger('google.generativeai').setLevel(logging.ERROR)

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

class DietPlanGenerator:
    def __init__(self, api_key: str = None):
        if api_key is None:
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=api_key)
        
        try:
            available_models = genai.list_models()
            generation_models = [m.name for m in available_models if 'generateContent' in m.supported_generation_methods]
            
            model_names = [
                'models/gemini-2.5-flash-lite',
                'models/gemini-2.5-flash-lite-latest',
                'models/gemini-2.5-flash',
                'models/gemini-2.5-flash-latest',
                'models/gemini-pro',
            ]
            
            model_to_use = None
            for model_name in model_names:
                if model_name in generation_models or model_name.replace('models/', '') in [m.replace('models/', '') for m in generation_models]:
                    model_to_use = model_name.replace('models/', '')
                    break
            
            if model_to_use is None:
                model_to_use = 'gemini-2.5-flash-lite'
            
            self.model = genai.GenerativeModel(model_to_use)
            print(f"✓ Using model: {model_to_use}")
        except Exception as e:
            self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
            print(f"✓ Using fallback model: gemini-2.5-flash-lite")
    
    def generate_diet_plan(self, user_data: dict) -> dict:
        import json
        prompt = f"""
You are a certified nutritionist and fitness expert. Create a detailed, personalized 7-day diet plan based on the following user information and respond ONLY with valid JSON format.

**User Profile:**
- Fitness Goal: {user_data.get('goal', 'Weight Maintenance')}
- Diet Preference: {user_data.get('diet_preference', 'No Preference')}
- Age: {user_data.get('age', 'N/A')} years
- Gender: {user_data.get('gender', 'N/A')}
- Current Weight: {user_data.get('weight', 'N/A')} kg
- Height: {user_data.get('height', 'N/A')} cm
- Activity Level: {user_data.get('activity_level', 'Moderately Active')}
- Food Allergies: {user_data.get('allergies', 'None')}
- Dislikes: {user_data.get('dislikes', 'None')}
- Meals Per Day: {user_data.get('meals_per_day', 3)}

Return ONLY a valid JSON object with the following structure (no markdown, no extra text):
{{
  "daily_calorie_target": <number>,
  "bmr": <number>,
  "tdee": <number>,
  "calorie_adjustment": <number>,
  "macronutrient_breakdown": {{
    "protein_grams": <number>,
    "protein_percentage": <number>,
    "carbs_grams": <number>,
    "carbs_percentage": <number>,
    "fats_grams": <number>,
    "fats_percentage": <number>
  }},
  "meal_plan": [
    {{
      "day": 1,
      "day_name": "Monday",
      "meals": [
        {{
          "meal_type": "Breakfast",
          "time": "8:00 AM",
          "meal_name": "Meal name",
          "food_items": [
            {{"item": "Food name", "quantity": "Amount", "calories": <number>, "protein": <number>, "carbs": <number>, "fats": <number>}}
          ],
          "total_meal_calories": <number>,
          "ingredients": [
            {{"ingredient": "ingredient name", "quantity": "amount", "unit": "grams/ml/cup/etc"}}
          ],
          "recipe_steps": [
            {{"step_number": 1, "instruction": "Step description"}},
            {{"step_number": 2, "instruction": "Step description"}}
          ],
          "cooking_time": "XX minutes",
          "difficulty_level": "Easy/Medium/Hard",
          "notes": "Any special tips or substitutions"
        }},
        {{
          "meal_type": "Lunch",
          "time": "1:00 PM",
          "meal_name": "Meal name",
          "food_items": [...],
          "total_meal_calories": <number>,
          "ingredients": [...],
          "recipe_steps": [...],
          "cooking_time": "XX minutes",
          "difficulty_level": "Easy/Medium/Hard",
          "notes": "Tips"
        }},
        {{
          "meal_type": "Dinner",
          "time": "8:00 PM",
          "meal_name": "Meal name",
          "food_items": [...],
          "total_meal_calories": <number>,
          "ingredients": [...],
          "recipe_steps": [...],
          "cooking_time": "XX minutes",
          "difficulty_level": "Easy/Medium/Hard",
          "notes": "Tips"
        }}
      ],
      "daily_total_calories": <number>
    }},
    {{
      "day": 2,
      "day_name": "Tuesday",
      "meals": [... similar structure ...]
    }},
    {{
      "day": 3,
      "day_name": "Wednesday",
      "meals": [... similar structure ...]
    }},
    {{
      "day": 4,
      "day_name": "Thursday",
      "meals": [... similar structure ...]
    }},
    {{
      "day": 5,
      "day_name": "Friday",
      "meals": [... similar structure ...]
    }},
    {{
      "day": 6,
      "day_name": "Saturday",
      "meals": [... similar structure ...]
    }},
    {{
      "day": 7,
      "day_name": "Sunday",
      "meals": [... similar structure ...]
    }}
  ],
  "snack_options": [
    {{
      "snack_name": "Name",
      "ingredients": ["item1", "item2"],
      "calories": <number>,
      "protein": <number>
    }}
  ],
  "hydration_guidelines": {{
    "daily_water_liters": <number>,
    "water_intake_schedule": ["timing": "liters"]
  }},
  "meal_timing": {{
    "breakfast_time": "time",
    "lunch_time": "time",
    "dinner_time": "time",
    "snack_timings": ["time1", "time2"]
  }},
  "nutrition_tips": [
    "tip1",
    "tip2",
    "tip3",
    "tip4",
    "tip5"
  ],
  "supplement_recommendations": [
    {{
      "supplement_name": "Name",
      "dosage": "Amount",
      "timing": "When to take",
      "benefit": "What it does"
    }}
  ],
  "dietary_restrictions_applied": {{
    "allergies_excluded": ["allergen1", "allergen2"],
    "dislikes_excluded": ["item1", "item2"]
  }},
  "weekly_summary": {{
    "total_calories": <number>,
    "average_daily_calories": <number>,
    "average_protein": <number>,
    "average_carbs": <number>,
    "average_fats": <number>
  }}
}}

Important: Return ONLY the JSON object, with no additional text, markdown formatting, or code blocks.
"""
        
        try:
            print(f"→ Generating diet plan for {user_data.get('goal', 'N/A')} goal...")
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON response
            diet_plan = json.loads(response_text)
            print(f"✓ Diet plan generated successfully!")
            return diet_plan
        except json.JSONDecodeError as e:
            print(f"✗ JSON parsing error: {str(e)}")
            raise Exception(f"Error parsing AI response as JSON: {str(e)}")
        except Exception as e:
            print(f"✗ Generation error: {str(e)}")
            raise Exception(f"Error generating diet plan: {str(e)}")

# Initialize generator
try:
    generator = DietPlanGenerator()
except Exception as e:
    print(f"✗ Error initializing API: {e}")
    generator = None


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'Diet Plan API is running',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200


@app.route('/api/diet-plan', methods=['POST'])
def create_diet_plan():
    """
    Generate personalized diet plan
    Expects JSON payload with user data
    """
    try:
        if not generator:
            return jsonify({
                'status': 'error',
                'message': 'API not properly initialized. Check GEMINI_API_KEY in .env file'
            }), 500
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['goal', 'diet_preference', 'age', 'gender', 'weight', 'height', 'activity_level']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {", ".join(missing_fields)}',
                'required_fields': required_fields
            }), 400
        
        print(f"\n{'='*60}")
        print(f"📋 New Diet Plan Request")
        print(f"{'='*60}")
        print(f"Goal: {data.get('goal')}")
        print(f"Diet: {data.get('diet_preference')}")
        print(f"Activity: {data.get('activity_level')}")
        print(f"{'='*60}\n")
        
        # Generate diet plan
        diet_plan = generator.generate_diet_plan(data)
        
        return jsonify({
            'status': 'success',
            'message': 'Diet plan generated successfully',
            'timestamp': datetime.now().isoformat(),
            'user_profile': {
                'goal': data.get('goal'),
                'diet_preference': data.get('diet_preference'),
                'age': data.get('age'),
                'gender': data.get('gender'),
                'weight': data.get('weight'),
                'height': data.get('height'),
                'activity_level': data.get('activity_level'),
                'allergies': data.get('allergies', 'None'),
                'dislikes': data.get('dislikes', 'None'),
                'meals_per_day': data.get('meals_per_day', 3)
            },
            'diet_plan': diet_plan if isinstance(diet_plan, dict) else {}
        }), 200
    
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/diet-plan/quick', methods=['POST'])
def quick_diet_plan():
    """
    Quick diet plan with minimal inputs
    """
    try:
        if not generator:
            return jsonify({
                'status': 'error',
                'message': 'API not properly initialized'
            }), 500
        
        data = request.get_json()
        
        # Use default values for optional fields
        user_data = {
            'goal': data.get('goal', 'Weight Maintenance'),
            'diet_preference': data.get('diet_preference', 'No Preference'),
            'age': data.get('age', '30'),
            'gender': data.get('gender', 'M'),
            'weight': data.get('weight', '70'),
            'height': data.get('height', '175'),
            'activity_level': data.get('activity_level', 'Moderately Active'),
            'allergies': data.get('allergies', 'None'),
            'dislikes': data.get('dislikes', 'None'),
            'meals_per_day': data.get('meals_per_day', 3)
        }
        
        diet_plan = generator.generate_diet_plan(user_data)
        
        return jsonify({
            'status': 'success',
            'message': 'Quick diet plan generated',
            'timestamp': datetime.now().isoformat(),
            'user_profile': user_data,
            'diet_plan': diet_plan if isinstance(diet_plan, dict) else {}
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/options', methods=['GET'])
def get_options():
    """Get available options for diet plan generation"""
    return jsonify({
        'status': 'success',
        'goals': ['Weight Loss', 'Muscle Gain', 'Weight Maintenance', 'Athletic Performance'],
        'diet_preferences': ['Vegetarian', 'Non-Vegetarian', 'Vegan', 'Pescatarian', 'Keto', 'No Preference'],
        'activity_levels': ['Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active', 'Extremely Active'],
        'meals_per_day_range': [3, 4, 5, 6]
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'available_endpoints': [
            'GET /api/health',
            'GET /api/options',
            'POST /api/diet-plan',
            'POST /api/diet-plan/quick'
        ]
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     Diet Plan Generator API - Running on Port 6060           ║
    ║                  Using Google Gemini API                     ║
    ╚══════════════════════════════════════════════════════════════╝
    
    📝 Available Endpoints:
    - GET  /api/health              → Health check
    - GET  /api/options             → Available options
    - POST /api/diet-plan           → Generate full diet plan
    - POST /api/diet-plan/quick     → Quick diet plan
    
    🔗 Base URL: http://localhost:6060
    
    """)
    app.run(debug=True, host='0.0.0.0', port=6060)