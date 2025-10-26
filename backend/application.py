from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime
import logging
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time

# Suppress gRPC warnings
os.environ['GRPC_ENABLE_FORK_SUPPORT'] = '1'
os.environ['GRPC_POLL_STRATEGY'] = 'poll'
logging.getLogger('google.generativeai').setLevel(logging.ERROR)

# Load environment variables from .env file (for local development)
# On Elastic Beanstalk, environment variables are set through EB configuration
load_dotenv()

application = Flask(__name__)

# ============= PROMETHEUS METRICS =============

# Request metrics
REQUEST_COUNT = Counter(
    'flask_app_requests_total', 
    'Total HTTP requests', 
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'flask_app_request_latency_seconds', 
    'HTTP request latency', 
    ['method', 'endpoint'],
    buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0)
)

# Diet plan specific metrics
DIET_PLAN_REQUESTS = Counter(
    'diet_plan_requests_total',
    'Total diet plan generation requests',
    ['goal', 'diet_preference', 'status']
)

DIET_PLAN_GENERATION_TIME = Histogram(
    'diet_plan_generation_seconds',
    'Time taken to generate diet plan',
    ['goal', 'diet_preference'],
    buckets=(1.0, 2.0, 5.0, 10.0, 15.0, 20.0, 30.0, 45.0, 60.0)
)

DIET_PLAN_FAILURES = Counter(
    'diet_plan_failures_total',
    'Total diet plan generation failures',
    ['error_type', 'goal']
)

# API health metrics
API_INITIALIZATION_STATUS = Gauge(
    'api_initialization_status',
    'API initialization status (1=success, 0=failure)'
)

ACTIVE_REQUESTS = Gauge(
    'active_requests',
    'Number of requests currently being processed',
    ['endpoint']
)

# Model metrics
MODEL_API_CALLS = Counter(
    'gemini_api_calls_total',
    'Total Gemini API calls',
    ['model_name', 'status']
)

JSON_PARSE_ERRORS = Counter(
    'json_parse_errors_total',
    'Total JSON parsing errors from AI responses'
)

# User profile metrics
USER_PROFILE_DISTRIBUTION = Counter(
    'user_profile_requests',
    'Distribution of user profiles',
    ['goal', 'diet_preference', 'activity_level', 'gender']
)

CALORIE_TARGET_DISTRIBUTION = Histogram(
    'calorie_target_distribution',
    'Distribution of calorie targets generated',
    buckets=(1000, 1500, 2000, 2500, 3000, 3500, 4000, 5000)
)

# ============= END METRICS =============

CORS(application)

class DietPlanGenerator:
    def __init__(self, api_key: str = None):
        if api_key is None:
            # Try to get from environment variables (EB sets these automatically)
            api_key = os.environ.get('GEMINI_API_KEY') or os.getenv('GEMINI_API_KEY')
          
            if not api_key:
                API_INITIALIZATION_STATUS.set(0)
                raise ValueError("GEMINI_API_KEY not found in environment variables")
        
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
            self.model_name = model_to_use
            API_INITIALIZATION_STATUS.set(1)
            print(f"✓ Using model: {model_to_use}")
        except Exception as e:
            self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
            self.model_name = 'gemini-2.5-flash-lite'
            API_INITIALIZATION_STATUS.set(1)
            print(f"✓ Using fallback model: gemini-2.5-flash-lite")
    
    def generate_diet_plan(self, user_data: dict) -> dict:
        import json
        
        goal = user_data.get('goal', 'Weight Maintenance')
        diet_pref = user_data.get('diet_preference', 'No Preference')
        
        # Start timing
        start_time = time.time()
        
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
            print(f"→ Generating diet plan for {goal} goal...")
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Track successful API call
            MODEL_API_CALLS.labels(model_name=self.model_name, status='success').inc()
            
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
            
            # Track generation time
            generation_time = time.time() - start_time
            DIET_PLAN_GENERATION_TIME.labels(goal=goal, diet_preference=diet_pref).observe(generation_time)
            
            # Track successful generation
            DIET_PLAN_REQUESTS.labels(goal=goal, diet_preference=diet_pref, status='success').inc()
            
            # Track calorie target distribution
            if 'daily_calorie_target' in diet_plan:
                CALORIE_TARGET_DISTRIBUTION.observe(diet_plan['daily_calorie_target'])
            
            print(f"✓ Diet plan generated successfully in {generation_time:.2f}s!")
            return diet_plan
            
        except json.JSONDecodeError as e:
            JSON_PARSE_ERRORS.inc()
            DIET_PLAN_FAILURES.labels(error_type='json_parse_error', goal=goal).inc()
            DIET_PLAN_REQUESTS.labels(goal=goal, diet_preference=diet_pref, status='failure').inc()
            MODEL_API_CALLS.labels(model_name=self.model_name, status='json_error').inc()
            print(f"✗ JSON parsing error: {str(e)}")
            raise Exception(f"Error parsing AI response as JSON: {str(e)}")
            
        except Exception as e:
            DIET_PLAN_FAILURES.labels(error_type='generation_error', goal=goal).inc()
            DIET_PLAN_REQUESTS.labels(goal=goal, diet_preference=diet_pref, status='failure').inc()
            MODEL_API_CALLS.labels(model_name=self.model_name, status='error').inc()
            print(f"✗ Generation error: {str(e)}")
            raise Exception(f"Error generating diet plan: {str(e)}")

# Initialize generator
try:
    generator = DietPlanGenerator()
except Exception as e:
    print(f"✗ Error initializing API: {e}")
    generator = None

@application.before_request
def start_timer():
    request.start_time = time.time()
    # Track active requests
    ACTIVE_REQUESTS.labels(endpoint=request.path).inc()

@application.after_request
def record_metrics(response):
    # Calculate response time
    resp_time = time.time() - request.start_time
    
    # Record metrics
    REQUEST_LATENCY.labels(request.method, request.path).observe(resp_time)
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    
    # Decrement active requests
    ACTIVE_REQUESTS.labels(endpoint=request.path).dec()
    
    return response

@application.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@application.route('/')
def index():
    return jsonify({
        'status': 'success',
        'message': 'Diet Plan API is running',
        'endpoints': ['/api/health', '/api/diet-plan', '/metrics']
    }), 200

@application.route("/test_env")
def test_env():
    return os.environ.get("GEMINI_API_KEY", "NOT FOUND")


@application.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'Diet Plan API is running',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'api_initialized': generator is not None
    }), 200


@application.route('/api/diet-plan', methods=['POST'])
def create_diet_plan():
    """Generate personalized diet plan"""
    try:
        if not generator:
            return jsonify({
                'status': 'error',
                'message': 'API not properly initialized. Check GEMINI_API_KEY environment variable'
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
        
        # Track user profile distribution
        USER_PROFILE_DISTRIBUTION.labels(
            goal=data.get('goal', 'Unknown'),
            diet_preference=data.get('diet_preference', 'Unknown'),
            activity_level=data.get('activity_level', 'Unknown'),
            gender=data.get('gender', 'Unknown')
        ).inc()
        
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


@application.route('/api/diet-plan/quick', methods=['POST'])
def quick_diet_plan():
    """Quick diet plan with minimal inputs"""
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
        
        # Track user profile
        USER_PROFILE_DISTRIBUTION.labels(
            goal=user_data['goal'],
            diet_preference=user_data['diet_preference'],
            activity_level=user_data['activity_level'],
            gender=user_data['gender']
        ).inc()
        
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


@application.route('/api/options', methods=['GET'])
def get_options():
    """Get available options for diet plan generation"""
    return jsonify({
        'status': 'success',
        'goals': ['Weight Loss', 'Muscle Gain', 'Weight Maintenance', 'Athletic Performance'],
        'diet_preferences': ['Vegetarian', 'Non-Vegetarian', 'Vegan', 'Pescatarian', 'Keto', 'No Preference'],
        'activity_levels': ['Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active', 'Extremely Active'],
        'meals_per_day_range': [3, 4, 5, 6]
    }), 200


@application.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'available_endpoints': [
            'GET /api/health',
            'GET /api/options',
            'GET /metrics',
            'POST /api/diet-plan',
            'POST /api/diet-plan/quick'
        ]
    }), 404


@application.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Get port from environment variable (EB uses PORT environment variable)
    port = int(os.environ.get('PORT', 8000))
    
    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║     Diet Plan Generator API - Running on Port {port}           ║
    ║                  Using Google Gemini API                     ║
    ║              Prometheus Metrics: /metrics                    ║
    ╚══════════════════════════════════════════════════════════════╝
    
    📝 Available Endpoints:
    - GET  /api/health              → Health check
    - GET  /api/options             → Available options
    - POST /api/diet-plan           → Generate full diet plan
    - POST /api/diet-plan/quick     → Quick diet plan
    - GET  /metrics                 → Prometheus metrics
    
    🔗 Base URL: http://localhost:{port}
    🌐 Environment: {'Elastic Beanstalk' if 'AWS_EXECUTION_ENV' in os.environ else 'Local Development'}
    
    """)
    application.run(debug=False, host='0.0.0.0', port=port)