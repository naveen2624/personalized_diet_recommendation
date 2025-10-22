import google.generativeai as genai
import json
from typing import Dict, List
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DietPlanGenerator:
    def __init__(self, api_key: str = None):
        """
        Initialize the Diet Plan Generator with Gemini API
        Automatically loads API key from .env file
        """
        if api_key is None:
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError(
                    "API key not found! Please add GEMINI_API_KEY to your .env file\n"
                    "Example .env file content:\n"
                    "GEMINI_API_KEY=your_api_key_here"
                )
        
        # Configure with the correct API settings
        genai.configure(api_key=api_key)
        
        # List available models to debug
        try:
            print("🔍 Checking available models...")
            available_models = genai.list_models()
            generation_models = [m.name for m in available_models if 'generateContent' in m.supported_generation_methods]
            print(f"✅ Found {len(generation_models)} models")
            
            # --- MODIFICATION START (Prioritizing Max RPD) ---
            # Prioritize models known to have the highest free-tier Requests Per Day (RPD) limits.
            model_names = [
                'models/gemini-2.5-flash-lite',       # Highest RPD (up to 1,000)
                'models/gemini-2.5-flash-lite-latest',
                'models/gemini-2.5-flash',            # Second highest RPD (up to 250)
                'models/gemini-2.5-flash-latest',
                'models/gemini-pro',                  # Older but generally reliable free tier model
            ]
            
            model_to_use = None
            for model_name in model_names:
                # Check for both 'models/name' and 'name' formats
                if model_name in generation_models or model_name.replace('models/', '') in [m.replace('models/', '') for m in generation_models]:
                    model_to_use = model_name.replace('models/', '')
                    print(f"✅ Using high-limit model: **{model_to_use}**")
                    break
            
            if model_to_use is None:
                # Fallback to the known, stable, high-limit model if auto-detection fails
                model_to_use = 'gemini-2.5-flash-lite'
                print(f"⚠️ Using hardcoded fallback: **{model_to_use}** for maximum RPD.")
            # --- MODIFICATION END ---
            
            self.model = genai.GenerativeModel(model_to_use)
            
        except Exception as e:
            print(f"⚠️ Model listing failed: {e}")
            print("Trying default model: **gemini-2.5-flash-lite**")
            # Final fallback to the model with the best free-tier limits
            self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    # --- The rest of the class methods (collect_user_data, generate_diet_plan, etc.) remain unchanged ---

    def collect_user_data(self) -> Dict:
        """Collect user preferences and data"""
        print("=== Personalized Diet Plan Generator ===")
        
        # Goal selection
        print("Select your fitness goal:")
        print("1. Weight Loss")
        print("2. Muscle Gain")
        print("3. Weight Maintenance")
        print("4. Athletic Performance")
        goal_map = {
            '1': 'Weight Loss',
            '2': 'Muscle Gain',
            '3': 'Weight Maintenance',
            '4': 'Athletic Performance'
        }
        goal_choice = input("Enter choice (1-4): ").strip()
        goal = goal_map.get(goal_choice, 'Weight Maintenance')
        
        # Diet preference
        print("\nSelect your diet preference:")
        print("1. Vegetarian")
        print("2. Non-Vegetarian")
        print("3. Vegan")
        print("4. Pescatarian")
        print("5. Keto")
        print("6. No Preference")
        diet_map = {
            '1': 'Vegetarian',
            '2': 'Non-Vegetarian',
            '3': 'Vegan',
            '4': 'Pescatarian',
            '5': 'Keto',
            '6': 'No Preference'
        }
        diet_choice = input("Enter choice (1-6): ").strip()
        diet_pref = diet_map.get(diet_choice, 'No Preference')
        
        # Basic info
        age = input("\nEnter your age: ").strip()
        gender = input("Enter your gender (M/F): ").strip().upper()
        weight = input("Enter your current weight (kg): ").strip()
        height = input("Enter your height (cm): ").strip()
        
        # Activity level
        print("\nSelect your activity level:")
        print("1. Sedentary (little or no exercise)")
        print("2. Lightly Active (1-3 days/week)")
        print("3. Moderately Active (3-5 days/week)")
        print("4. Very Active (6-7 days/week)")
        print("5. Extremely Active (physical job + exercise)")
        activity_map = {
            '1': 'Sedentary',
            '2': 'Lightly Active',
            '3': 'Moderately Active',
            '4': 'Very Active',
            '5': 'Extremely Active'
        }
        activity_choice = input("Enter choice (1-5): ").strip()
        activity = activity_map.get(activity_choice, 'Moderately Active')
        
        # Allergies and dislikes
        allergies = input("\nAny food allergies? (comma-separated, or 'none'): ").strip()
        dislikes = input("Any foods you dislike? (comma-separated, or 'none'): ").strip()
        
        # Meal preferences
        meals_per_day = input("Preferred number of meals per day (3-6): ").strip()
        
        return {
            'goal': goal,
            'diet_preference': diet_pref,
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height,
            'activity_level': activity,
            'allergies': allergies,
            'dislikes': dislikes,
            'meals_per_day': meals_per_day
        }
    
    def generate_diet_plan(self, user_data: Dict) -> str:
        """Generate personalized diet plan using Gemini AI"""
        
        # Create detailed prompt for AI
        prompt = f"""
You are a certified nutritionist and fitness expert. Create a detailed, personalized 7-day diet plan based on the following user information:

**User Profile:**
- Fitness Goal: {user_data['goal']}
- Diet Preference: {user_data['diet_preference']}
- Age: {user_data['age']} years
- Gender: {user_data['gender']}
- Current Weight: {user_data['weight']} kg
- Height: {user_data['height']} cm
- Activity Level: {user_data['activity_level']}
- Food Allergies: {user_data['allergies']}
- Dislikes: {user_data['dislikes']}
- Meals Per Day: {user_data['meals_per_day']}

**Requirements:**
1. Calculate daily calorie requirements based on BMR and activity level
2. Provide macronutrient breakdown (protein, carbs, fats) for the goal
3. Create a 7-day meal plan with specific meals for each day
4. Include portion sizes and approximate calories for each meal
5. Add 2-3 healthy snack options
6. Provide hydration recommendations
7. Include meal timing suggestions
8. Add 3-5 general nutrition tips for their goal
9. Suggest 3 supplement recommendations (if needed)
10. Make it practical, affordable, and easy to follow

**Format the response with clear sections:**
- Daily Caloric Target
- Macronutrient Breakdown
- Day-wise Meal Plan (Day 1-7)
- Snack Options
- Hydration Guidelines
- Meal Timing
- Nutrition Tips
- Supplement Suggestions

Make it detailed, specific, and actionable. Use foods commonly available and appropriate for their dietary preference.
"""
        
        try:
            print("\n🤖 Generating your personalized diet plan using AI...\n")
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating diet plan: {str(e)}\nPlease check your API key and internet connection."
    
    def save_diet_plan(self, diet_plan: str, user_data: Dict, filename: str = "my_diet_plan.txt"):
        """Save the diet plan to a file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("PERSONALIZED DIET PLAN\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Generated for: {user_data['goal']} | {user_data['diet_preference']}\n")
            f.write(f"Profile: {user_data['age']}Y | {user_data['gender']} | {user_data['weight']}kg | {user_data['height']}cm\n")
            f.write("\n" + "=" * 80 + "\n\n")
            f.write(diet_plan)
        print(f"\n✅ Diet plan saved to '{filename}'")
    
    def run(self):
        """Main execution function"""
        try:
            # Collect user data
            user_data = self.collect_user_data()
            
            # Generate diet plan
            diet_plan = self.generate_diet_plan(user_data)
            
            # Display the plan
            print("\n" + "=" * 80)
            print("YOUR PERSONALIZED DIET PLAN")
            print("=" * 80 + "\n")
            print(diet_plan)
            
            # Save to file
            save_option = input("\n\nWould you like to save this diet plan? (y/n): ").strip().lower()
            if save_option == 'y':
                filename = input("Enter filename (default: my_diet_plan.txt): ").strip()
                if not filename:
                    filename = "my_diet_plan.txt"
                if not filename.endswith('.txt'):
                    filename += '.txt'
                self.save_diet_plan(diet_plan, user_data, filename)
            
            print("\n🎉 Thank you for using the Diet Plan Generator!")
            print("Remember to consult with a healthcare professional before starting any new diet plan.")
            
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user.")
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")


# Alternative: Using Hugging Face (another free option)
class DietPlanGeneratorHF:
    """Alternative implementation using Hugging Face API (free tier)"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize with Hugging Face API
        Automatically loads API key from .env file
        """
        if api_key is None:
            api_key = os.getenv('HF_API_KEY')
            if not api_key:
                raise ValueError(
                    "API key not found! Please add HF_API_KEY to your .env file\n"
                    "Example .env file content:\n"
                    "HF_API_KEY=your_api_key_here"
                )
        
        self.api_key = api_key
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def query_model(self, prompt: str) -> str:
        import requests
        payload = {"inputs": prompt, "parameters": {"max_new_tokens": 2000, "temperature": 0.7}}
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.json()[0]['generated_text']


# Main execution
if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║         AI-Powered Personalized Diet Plan Generator          ║
    ║                       Using Google Gemini API                ║
    ╚══════════════════════════════════════════════════════════════╝
    
    📝 Setup Instructions:
    1. Install required packages:
        pip install google-generativeai python-dotenv
    
    2. Get your FREE Gemini API key from: 
        https://makersuite.google.com/app/apikey
    
    3. Create a .env file in the same directory with:
        GEMINI_API_KEY=your_api_key_here
    
    """)
    
    try:
        # Automatically loads from .env file
        generator = DietPlanGenerator()
        generator.run()
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease create a .env file with your API key and try again.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")