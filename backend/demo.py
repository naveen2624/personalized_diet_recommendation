import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import warnings
from datetime import datetime, timedelta
import json
warnings.filterwarnings('ignore')

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

class UserDataCollector:
    """Comprehensive user data collection"""
    
    def __init__(self):
        self.user_data = {}
    
    def collect_basic_info(self):
        """Collect basic user information"""
        print("=== PERSONAL INFORMATION ===")
        
        name = input("Enter your name: ").strip()
        age = int(input("Enter your age: "))
        
        gender = input("Enter your gender (male/female/other): ").strip().lower()
        while gender not in ['male', 'female', 'other']:
            gender = input("Please enter 'male', 'female', or 'other': ").strip().lower()
        
        weight = float(input("Enter your weight (kg): "))
        height = float(input("Enter your height (cm): "))
        
        return {
            'name': name,
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height
        }
    
    def collect_activity_info(self):
        """Collect activity level information"""
        print("\n=== ACTIVITY LEVEL ===")
        print("1. Sedentary (little/no exercise)")
        print("2. Lightly active (light exercise 1-3 days/week)")
        print("3. Moderately active (moderate exercise 3-5 days/week)")
        print("4. Very active (hard exercise 6-7 days/week)")
        print("5. Extremely active (very hard exercise, physical job)")
        
        activity_choice = int(input("Select your activity level (1-5): "))
        
        activity_map = {
            1: 'sedentary',
            2: 'lightly_active',
            3: 'moderately_active',
            4: 'very_active',
            5: 'extremely_active'
        }
        
        return {'activity_level': activity_map[activity_choice]}
    
    def collect_health_goals(self):
        """Collect health and fitness goals"""
        print("\n=== HEALTH GOALS ===")
        print("1. Weight loss")
        print("2. Weight gain")
        print("3. Weight maintenance")
        print("4. Muscle gain")
        print("5. Athletic performance")
        
        goal_choice = int(input("Select your primary goal (1-5): "))
        
        goal_map = {
            1: 'weight_loss',
            2: 'weight_gain',
            3: 'weight_maintenance',
            4: 'muscle_gain',
            5: 'athletic_performance'
        }
        
        target_weight = None
        if goal_choice in [1, 2]:
            target_weight = float(input("Enter your target weight (kg): "))
        
        timeline = input("Timeline to achieve goal (e.g., '3 months', '6 weeks'): ").strip()
        
        return {
            'health_goal': goal_map[goal_choice],
            'target_weight': target_weight,
            'timeline': timeline
        }
    
    def collect_dietary_preferences(self):
        """Collect dietary preferences and restrictions"""
        print("\n=== DIETARY PREFERENCES ===")
        
        # Food preferences
        print("Food Type Preference:")
        print("1. Vegetarian")
        print("2. Non-vegetarian")
        print("3. Vegan")
        print("4. Eggetarian")
        
        food_type = int(input("Select food type (1-4): "))
        food_type_map = {1: 'vegetarian', 2: 'non_vegetarian', 3: 'vegan', 4: 'eggetarian'}
        
        # Regional preferences
        print("\nRegional Cuisine Preferences (select multiple, comma-separated):")
        print("1. North Indian  2. South Indian  3. East Indian  4. West Indian")
        print("5. Gujarati  6. Punjabi  7. Bengali  8. Tamil  9. No preference")
        
        region_input = input("Enter numbers (e.g., 1,2,6): ").strip()
        region_map = {
            '1': 'north_indian', '2': 'south_indian', '3': 'east_indian', 
            '4': 'west_indian', '5': 'gujarati', '6': 'punjabi', 
            '7': 'bengali', '8': 'tamil', '9': 'no_preference'
        }
        
        regions = [region_map[r.strip()] for r in region_input.split(',') if r.strip() in region_map]
        
        # Dietary restrictions
        print("\nDietary Restrictions (select multiple, comma-separated):")
        print("1. Diabetic-friendly  2. Gluten-free  3. Dairy-free  4. Nut-free")
        print("5. Keto-friendly  6. Low-sodium  7. Jain-friendly  8. None")
        
        restrictions_input = input("Enter numbers (e.g., 1,3,6): ").strip()
        restriction_map = {
            '1': 'diabetic_friendly', '2': 'gluten_free', '3': 'dairy_free',
            '4': 'nut_free', '5': 'keto_friendly', '6': 'low_sodium',
            '7': 'jain_friendly', '8': 'none'
        }
        
        restrictions = [restriction_map[r.strip()] for r in restrictions_input.split(',') 
                       if r.strip() in restriction_map]
        
        # Food allergies
        allergies = input("Any food allergies (comma-separated, or 'none'): ").strip()
        allergy_list = [a.strip() for a in allergies.split(',') if a.strip().lower() != 'none']
        
        # Disliked foods
        dislikes = input("Foods you dislike (comma-separated, or 'none'): ").strip()
        dislike_list = [d.strip() for d in dislikes.split(',') if d.strip().lower() != 'none']
        
        return {
            'food_type': food_type_map[food_type],
            'regional_preferences': regions,
            'dietary_restrictions': restrictions,
            'allergies': allergy_list,
            'dislikes': dislike_list
        }
    
    def collect_meal_preferences(self):
        """Collect meal timing and frequency preferences"""
        print("\n=== MEAL PREFERENCES ===")
        
        # Meal frequency
        print("How many meals do you prefer per day?")
        print("1. 3 meals (Breakfast, Lunch, Dinner)")
        print("2. 4 meals (+ Evening snack)")
        print("3. 5 meals (+ Pre-breakfast, Pre-lunch)")
        print("4. 6 meals (+ Mid-morning, Mid-afternoon snacks)")
        
        meal_freq = int(input("Select option (1-4): "))
        
        # Meal timings
        print("\nPreferred meal timings:")
        wake_time = input("Wake up time (HH:MM, e.g., 07:00): ").strip()
        sleep_time = input("Sleep time (HH:MM, e.g., 23:00): ").strip()
        
        # Exercise timing
        print("\nExercise preferences:")
        exercises = input("Do you exercise regularly? (yes/no): ").strip().lower() == 'yes'
        exercise_time = None
        if exercises:
            print("When do you usually exercise?")
            print("1. Morning (before breakfast)")
            print("2. Morning (after breakfast)")
            print("3. Afternoon")
            print("4. Evening")
            print("5. Variable timing")
            
            ex_time = int(input("Select option (1-5): "))
            exercise_time_map = {
                1: 'morning_fasted', 2: 'morning_fed', 3: 'afternoon',
                4: 'evening', 5: 'variable'
            }
            exercise_time = exercise_time_map[ex_time]
        
        return {
            'meal_frequency': meal_freq,
            'wake_time': wake_time,
            'sleep_time': sleep_time,
            'exercises': exercises,
            'exercise_time': exercise_time
        }
    
    def collect_health_conditions(self):
        """Collect health conditions and medications"""
        print("\n=== HEALTH CONDITIONS ===")
        
        conditions_input = input("Any health conditions? (diabetes, hypertension, thyroid, etc. or 'none'): ").strip()
        conditions = [c.strip() for c in conditions_input.split(',') if c.strip().lower() != 'none']
        
        medications = input("Any medications that affect diet? (or 'none'): ").strip()
        med_list = [m.strip() for m in medications.split(',') if m.strip().lower() != 'none']
        
        water_intake = float(input("Daily water intake (liters): ") or "2.5")
        
        return {
            'health_conditions': conditions,
            'medications': med_list,
            'water_intake': water_intake
        }
    
    def collect_all_data(self):
        """Collect comprehensive user data"""
        print("Welcome to the Indian Food Nutrition System!")
        print("Please provide the following information for personalized meal recommendations.\n")
        
        self.user_data.update(self.collect_basic_info())
        self.user_data.update(self.collect_activity_info())
        self.user_data.update(self.collect_health_goals())
        self.user_data.update(self.collect_dietary_preferences())
        self.user_data.update(self.collect_meal_preferences())
        self.user_data.update(self.collect_health_conditions())
        
        print("\n=== DATA COLLECTION COMPLETE ===")
        print("Thank you! Processing your personalized meal plan...\n")
        
        return self.user_data

class WeeklyMealPlanner:
    """Generate comprehensive weekly meal schedules"""
    
    def __init__(self, user_profile, food_df):
        self.user_profile = user_profile
        self.food_df = food_df
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # Meal timing based on user preferences
        self.meal_schedule = self._create_meal_schedule()
        
        # Calorie distribution based on meal frequency
        self.calorie_distribution = self._calculate_calorie_distribution()
    
    def _create_meal_schedule(self):
        """Create meal schedule based on user preferences"""
        meal_freq = self.user_profile.get('meal_frequency', 3)
        exercises = self.user_profile.get('exercises', False)
        exercise_time = self.user_profile.get('exercise_time', 'morning_fed')
        
        schedule = {}
        
        if meal_freq >= 3:
            schedule.update({
                'breakfast': '08:00',
                'lunch': '13:00',
                'dinner': '20:00'
            })
        
        if meal_freq >= 4:
            schedule['evening_snack'] = '17:00'
        
        if meal_freq >= 5:
            if exercises and exercise_time == 'morning_fasted':
                schedule['pre_breakfast'] = '06:30'  # Pre-workout
            else:
                schedule['pre_breakfast'] = '07:30'  # Light start
            schedule['pre_lunch'] = '11:30'
        
        if meal_freq >= 6:
            schedule['mid_morning_snack'] = '10:00'
            schedule['mid_afternoon_snack'] = '15:30'
        
        return schedule
    
    def _calculate_calorie_distribution(self):
        """Calculate calorie distribution across meals"""
        target_calories = self.user_profile['target_calories']
        meal_count = len(self.meal_schedule)
        
        # Standard distributions based on meal importance
        distributions = {
            3: {'breakfast': 0.25, 'lunch': 0.40, 'dinner': 0.35},
            4: {'breakfast': 0.25, 'lunch': 0.35, 'dinner': 0.30, 'evening_snack': 0.10},
            5: {'pre_breakfast': 0.08, 'breakfast': 0.22, 'pre_lunch': 0.10, 
                'lunch': 0.35, 'dinner': 0.25},
            6: {'pre_breakfast': 0.08, 'breakfast': 0.20, 'mid_morning_snack': 0.07,
                'pre_lunch': 0.08, 'lunch': 0.30, 'mid_afternoon_snack': 0.07,
                'evening_snack': 0.10, 'dinner': 0.20}
        }
        
        meal_freq = self.user_profile.get('meal_frequency', 3)
        if meal_freq in distributions:
            base_dist = distributions[meal_freq]
        else:
            # Equal distribution for custom frequencies
            equal_share = 1.0 / len(self.meal_schedule)
            base_dist = {meal: equal_share for meal in self.meal_schedule.keys()}
        
        # Calculate actual calories per meal
        calorie_dist = {}
        for meal, percentage in base_dist.items():
            if meal in self.meal_schedule:
                calorie_dist[meal] = int(target_calories * percentage)
        
        return calorie_dist
    
    def _filter_foods_by_criteria(self, meal_type, calorie_target, day_num):
        """Filter foods based on meal type and dietary restrictions"""
        filtered_df = self.food_df.copy()
        
        # Apply dietary restrictions
        food_type = self.user_profile.get('food_type', 'non_vegetarian')
        if food_type == 'vegetarian' or food_type == 'vegan':
            filtered_df = filtered_df[filtered_df['veg_nonveg'] == 'veg']
        
        if food_type == 'vegan':
            filtered_df = filtered_df[filtered_df.get('is_vegan', True) == True]
        
        # Apply health-based restrictions
        restrictions = self.user_profile.get('dietary_restrictions', [])
        for restriction in restrictions:
            column_name = f'is_{restriction}'
            if column_name in filtered_df.columns:
                filtered_df = filtered_df[filtered_df[column_name] == True]
        
        # Filter by meal category if available
        if 'meal_category' in filtered_df.columns:
            if meal_type in ['breakfast', 'lunch', 'dinner']:
                meal_foods = filtered_df[filtered_df['meal_category'] == meal_type]
                if len(meal_foods) > 0:
                    filtered_df = meal_foods
        
        # Filter by calorie range (±30% of target)
        calorie_min = calorie_target * 0.7
        calorie_max = calorie_target * 1.3
        
        filtered_df = filtered_df[
            (filtered_df['calories_(kcal)'] >= calorie_min) & 
            (filtered_df['calories_(kcal)'] <= calorie_max)
        ]
        
        # Remove foods user dislikes
        dislikes = self.user_profile.get('dislikes', [])
        for dislike in dislikes:
            filtered_df = filtered_df[~filtered_df['dish_name'].str.contains(dislike, case=False, na=False)]
        
        return filtered_df
    
    def _get_meal_variety(self, meal_type, options, day_num, used_foods):
        """Ensure variety in meal selection across the week"""
        # Remove already used foods for variety
        available_options = options[~options['dish_name'].isin(used_foods)]
        
        if len(available_options) == 0:
            available_options = options  # Fall back to original if no variety possible
        
        # Score foods based on user goals
        scored_options = self._score_foods(available_options, meal_type)
        
        return scored_options.head(1)
    
    def _score_foods(self, df, meal_type):
        """Score foods based on user health goals and meal timing"""
        if len(df) == 0:
            return df
        
        df = df.copy()
        scores = np.zeros(len(df))
        health_goal = self.user_profile.get('health_goal', 'weight_maintenance')
        
        # Base nutritional scoring
        if health_goal == 'weight_loss':
            scores += (df['protein_(g)'] / df['calories_(kcal)']) * 100  # High protein efficiency
            scores += (df['fibre_(g)'] / df['calories_(kcal)']) * 80    # High fiber for satiety
            scores -= (df['fats_(g)'] / df['calories_(kcal)']) * 40     # Lower fat preference
            
        elif health_goal == 'weight_gain':
            scores += df['calories_(kcal)'] / 50  # Higher calories preferred
            scores += df['protein_(g)'] * 3       # Good protein content
            scores += df['fats_(g)'] * 2          # Healthy fats for calories
            
        elif health_goal == 'muscle_gain':
            scores += df['protein_(g)'] * 5       # Very high protein preference
            scores += (df['protein_(g)'] / df['calories_(kcal)']) * 150
            
        # Meal-specific adjustments
        if meal_type in ['pre_breakfast', 'pre_lunch']:
            scores += (500 - df['calories_(kcal)']) / 100  # Prefer lighter options
            scores += df['carbohydrates_(g)'] * 2          # Quick energy
            
        elif meal_type == 'breakfast':
            scores += df['protein_(g)'] * 2    # Good protein to start day
            scores += df['fibre_(g)'] * 3      # Fiber for sustained energy
            
        elif meal_type in ['mid_morning_snack', 'mid_afternoon_snack', 'evening_snack']:
            scores += (300 - df['calories_(kcal)']) / 100  # Prefer lighter snacks
            scores += df['protein_(g)'] * 2    # Protein for satiety
        
        # Penalize high sodium for health-conscious users
        if 'low_sodium' in self.user_profile.get('dietary_restrictions', []):
            scores -= df['sodium_(mg)'] / 100
        
        # Boost foods with high nutrients
        scores += df.get('calcium_(mg)', 0) / 100
        scores += df.get('iron_(mg)', 0) * 10
        scores += df.get('vitamin_c_(mg)', 0) / 10
        
        df['score'] = scores
        return df.sort_values('score', ascending=False)
    
    def generate_weekly_plan(self):
        """Generate complete weekly meal plan"""
        weekly_plan = {}
        used_foods_global = set()  # Track foods used globally for maximum variety
        
        for day in self.days:
            daily_plan = {}
            used_foods_daily = set()  # Track foods used in a single day
            
            for meal_type, time in self.meal_schedule.items():
                calorie_target = self.calorie_distribution.get(meal_type, 300)
                
                # Get available foods for this meal
                available_foods = self._filter_foods_by_criteria(
                    meal_type, calorie_target, self.days.index(day)
                )
                
                if len(available_foods) > 0:
                    # Select meal with variety consideration
                    selected_meal = self._get_meal_variety(
                        meal_type, available_foods, 
                        self.days.index(day), 
                        used_foods_global.union(used_foods_daily)
                    )
                    
                    if len(selected_meal) > 0:
                        meal_info = selected_meal.iloc[0]
                        daily_plan[meal_type] = {
                            'time': time,
                            'dish_name': meal_info['dish_name'],
                            'calories': meal_info['calories_(kcal)'],
                            'protein': meal_info['protein_(g)'],
                            'carbs': meal_info['carbohydrates_(g)'],
                            'fats': meal_info['fats_(g)'],
                            'fiber': meal_info.get('fibre_(g)', 0),
                            'target_calories': calorie_target
                        }
                        
                        used_foods_daily.add(meal_info['dish_name'])
                        used_foods_global.add(meal_info['dish_name'])
                    else:
                        daily_plan[meal_type] = self._create_fallback_meal(meal_type, calorie_target)
                else:
                    daily_plan[meal_type] = self._create_fallback_meal(meal_type, calorie_target)
            
            weekly_plan[day] = daily_plan
            
            # Reset global tracking every 3 days for some repetition
            if (self.days.index(day) + 1) % 3 == 0:
                used_foods_global = set()
        
        return weekly_plan
    
    def _create_fallback_meal(self, meal_type, calorie_target):
        """Create fallback meal when no suitable food found"""
        fallback_meals = {
            'pre_breakfast': {'dish_name': 'Green Tea + 2 Almonds', 'calories': 50},
            'breakfast': {'dish_name': 'Oats with Milk', 'calories': 300},
            'mid_morning_snack': {'dish_name': 'Apple', 'calories': 80},
            'pre_lunch': {'dish_name': 'Buttermilk', 'calories': 60},
            'lunch': {'dish_name': 'Dal Rice with Vegetables', 'calories': 400},
            'mid_afternoon_snack': {'dish_name': 'Green Tea + Biscuits', 'calories': 100},
            'evening_snack': {'dish_name': 'Mixed Nuts', 'calories': 150},
            'dinner': {'dish_name': 'Vegetable Curry with Roti', 'calories': 350}
        }
        
        fallback = fallback_meals.get(meal_type, {'dish_name': 'Healthy Snack', 'calories': calorie_target})
        fallback.update({
            'protein': 5,
            'carbs': 30,
            'fats': 5,
            'fiber': 3,
            'target_calories': calorie_target,
            'note': 'Fallback suggestion - please customize based on availability'
        })
        
        return fallback
    
    def get_daily_summary(self, daily_plan):
        """Calculate daily nutritional summary"""
        total_calories = sum(meal.get('calories', 0) for meal in daily_plan.values())
        total_protein = sum(meal.get('protein', 0) for meal in daily_plan.values())
        total_carbs = sum(meal.get('carbs', 0) for meal in daily_plan.values())
        total_fats = sum(meal.get('fats', 0) for meal in daily_plan.values())
        total_fiber = sum(meal.get('fiber', 0) for meal in daily_plan.values())
        
        return {
            'total_calories': total_calories,
            'total_protein': total_protein,
            'total_carbs': total_carbs,
            'total_fats': total_fats,
            'total_fiber': total_fiber,
            'target_calories': self.user_profile['target_calories'],
            'calorie_difference': total_calories - self.user_profile['target_calories']
        }
    
    def display_weekly_plan(self, weekly_plan):
        """Display formatted weekly meal plan"""
        print("="*80)
        print(f"PERSONALIZED WEEKLY MEAL PLAN FOR {self.user_profile.get('name', 'USER').upper()}")
        print("="*80)
        
        print(f"Target Daily Calories: {self.user_profile['target_calories']:.0f} kcal")
        print(f"Health Goal: {self.user_profile.get('health_goal', 'maintenance').replace('_', ' ').title()}")
        print(f"Food Preference: {self.user_profile.get('food_type', 'mixed').replace('_', ' ').title()}")
        print()
        
        for day, daily_plan in weekly_plan.items():
            print(f"\n📅 {day.upper()}")
            print("-" * 50)
            
            for meal_type, meal_info in daily_plan.items():
                time = meal_info.get('time', '')
                dish = meal_info.get('dish_name', 'Not specified')
                calories = meal_info.get('calories', 0)
                protein = meal_info.get('protein', 0)
                
                meal_display = meal_type.replace('_', ' ').title()
                print(f"{time:>6} | {meal_display:<18} | {dish:<25} | {calories:>3.0f} kcal | {protein:>4.1f}g protein")
            
            # Daily summary
            summary = self.get_daily_summary(daily_plan)
            print(f"       | {'DAILY TOTAL':<18} | {'':<25} | {summary['total_calories']:>3.0f} kcal | {summary['total_protein']:>4.1f}g protein")
            
            # Show if over/under target
            diff = summary['calorie_difference']
            if abs(diff) > 50:
                status = "⚠️  OVER" if diff > 0 else "⚠️  UNDER"
                print(f"       | {status:<18} | Target: {summary['target_calories']:.0f} kcal | Diff: {diff:+.0f} kcal")
        
        # Weekly summary
        self._display_weekly_summary(weekly_plan)
    
    def _display_weekly_summary(self, weekly_plan):
        """Display weekly nutritional summary"""
        weekly_calories = 0
        weekly_protein = 0
        
        for daily_plan in weekly_plan.values():
            summary = self.get_daily_summary(daily_plan)
            weekly_calories += summary['total_calories']
            weekly_protein += summary['total_protein']
        
        avg_daily_calories = weekly_calories / 7
        avg_daily_protein = weekly_protein / 7
        target_calories = self.user_profile['target_calories']
        
        print("\n" + "="*80)
        print("WEEKLY SUMMARY")
        print("="*80)
        print(f"Average Daily Calories: {avg_daily_calories:.0f} kcal (Target: {target_calories:.0f} kcal)")
        print(f"Average Daily Protein: {avg_daily_protein:.1f}g")
        print(f"Weekly Calorie Difference: {(avg_daily_calories - target_calories) * 7:.0f} kcal")
        
        # Recommendations
        print("\n📝 RECOMMENDATIONS:")
        if avg_daily_calories < target_calories - 100:
            print("• Consider adding healthy snacks or increasing portion sizes")
        elif avg_daily_calories > target_calories + 100:
            print("• Consider reducing portion sizes or choosing lower-calorie alternatives")
        else:
            print("• Your meal plan is well-balanced for your goals!")
        
        if avg_daily_protein < 50:
            print("• Consider adding more protein-rich foods to your meals")
        
        print("\n💡 TIPS:")
        print("• Stay hydrated - aim for 8-10 glasses of water daily")
        print("• Listen to your body and adjust portions as needed")
        print("• Include variety in vegetables and fruits for better nutrition")

# Enhanced Food Recommendation System with meal planning
class EnhancedFoodRecommendationSystem:
    """Enhanced system with comprehensive meal planning"""
    
    def __init__(self):
        self.user_profiler = UserProfiler()
        self.data_collector = UserDataCollector()
        self.food_df = None
    
    def initialize_system(self, food_data_path=None, food_df=None):
        """Initialize system with data"""
        if food_df is not None:
            self.food_df = food_df
        elif food_data_path:
            self.food_df = pd.read_csv(food_data_path)
        else:
            self.food_df = self._create_enhanced_sample_data()
        
        self._preprocess_food_data()
    
    def _create_enhanced_sample_data(self):
        """Create comprehensive sample Indian food data"""
        sample_data = {
            'dish_name': [
                # Breakfast items
                'Poha', 'Upma', 'Idli Sambar', 'Dosa', 'Paratha with Curd',
                'Oats Upma', 'Vegetable Daliya', 'Moong Dal Cheela',
                
                # Pre-breakfast/snacks
                'Green Tea', 'Almonds (10 pieces)', 'Apple', 'Banana', 'Buttermilk',
                'Mixed Nuts', 'Roasted Chana', 'Dates (3 pieces)',
                
                # Lunch items
                'Dal Rice', 'Rajma Rice', 'Chole with Roti', 'Vegetable Biryani',
                'Fish Curry with Rice', 'Chicken Curry with Roti', 'Sambar Rice',
                'Vegetable Pulao',
                
                # Dinner items
                'Roti with Dal', 'Khichdi', 'Vegetable Curry with Rice',
                'Grilled Chicken with Salad', 'Paneer Curry with Roti',
                'Fish Tikka with Vegetables', 'Moong Dal with Roti'
            ],
            'calories_(kcal)': [
                250, 200, 300, 150, 350, 180, 220, 200,  # Breakfast
                5, 70, 80, 100, 60, 150, 120, 90,        # Snacks
                400, 450, 380, 500, 420, 480, 350, 400,  # Lunch
                320, 300, 350, 280, 400, 320, 280        # Dinner
            ],
            'protein_(g)': [
                6, 5, 12, 4, 12, 6, 8, 14,      # Breakfast
                0, 3, 0, 1, 3, 6, 8, 2,         # Snacks
                15, 18, 16, 12, 25, 28, 14, 10, # Lunch
                12, 12, 8, 30, 20, 28, 15       # Dinner
            ],
            'carbohydrates_(g)': [
                45, 35, 50, 25, 40, 32, 38, 20, # Breakfast
                0, 2, 20, 25, 8, 5, 15, 22,     # Snacks
                65, 70, 55, 80, 45, 35, 60, 75, # Lunch
                45, 50, 55, 5, 35, 8, 40        # Dinner
            ],
            'fats_(g)': [
                8, 6, 5, 3, 15, 4, 6, 8,        # Breakfast
                0, 6, 0, 0, 1, 12, 3, 0,        # Snacks
                12, 8, 10, 15, 18, 20, 8, 12,   # Lunch
                8, 6, 10, 15, 20, 18, 8         # Dinner
            ],
            'fibre_(g)': [
                4, 3, 3, 2, 2, 5, 6, 4,         # Breakfast
                0, 3, 3, 3, 0, 2, 6, 2,         # Snacks
                8, 10, 8, 4, 2, 1, 6, 3,        # Lunch
                6, 4, 8, 2, 3, 1, 6             # Dinner
            ],
            'sodium_(mg)': [
                300, 400, 500, 200, 450, 350, 300, 250, # Breakfast
                0, 0, 2, 1, 150, 0, 5, 0,               # Snacks
                600, 700, 800, 650, 750, 900, 550, 600, # Lunch
                500, 400, 600, 400, 700, 500, 450       # Dinner
            ],
            'calcium_(mg)': [
                50, 30, 100, 60, 120, 40, 60, 80,   # Breakfast
                0, 75, 10, 6, 120, 50, 25, 15,      # Snacks
                80, 60, 100, 70, 40, 35, 120, 60,   # Lunch
                90, 70, 80, 25, 200, 30, 80         # Dinner
            ],
            'iron_(mg)': [
                2, 1, 3, 1, 2, 2, 3, 3,         # Breakfast
                0, 1, 0, 0, 0, 1, 2, 1,         # Snacks
                4, 5, 4, 3, 2, 3, 4, 2,         # Lunch
                3, 2, 3, 2, 2, 2, 4             # Dinner
            ],
            'meal_category': [
                'breakfast', 'breakfast', 'breakfast', 'breakfast', 'breakfast',
                'breakfast', 'breakfast', 'breakfast',
                'snack', 'snack', 'snack', 'snack', 'snack',
                'snack', 'snack', 'snack',
                'lunch', 'lunch', 'lunch', 'lunch', 'lunch', 'lunch', 'lunch', 'lunch',
                'dinner', 'dinner', 'dinner', 'dinner', 'dinner', 'dinner', 'dinner'
            ],
            'veg_nonveg': [
                'veg', 'veg', 'veg', 'veg', 'veg', 'veg', 'veg', 'veg',     # Breakfast
                'veg', 'veg', 'veg', 'veg', 'veg', 'veg', 'veg', 'veg',     # Snacks
                'veg', 'veg', 'veg', 'veg', 'non-veg', 'non-veg', 'veg', 'veg', # Lunch
                'veg', 'veg', 'veg', 'non-veg', 'veg', 'non-veg', 'veg'     # Dinner
            ],
            'region': [
                'west', 'south', 'south', 'south', 'north', 'north', 'north', 'north', # Breakfast
                'all', 'all', 'all', 'all', 'all', 'all', 'north', 'all',              # Snacks
                'all', 'north', 'north', 'south', 'south', 'north', 'south', 'north',  # Lunch
                'all', 'all', 'all', 'north', 'north', 'north', 'all'                  # Dinner
            ],
            'is_vegan': [
                True, True, False, True, False, True, True, True,    # Breakfast
                True, True, True, True, False, True, True, True,    # Snacks
                True, True, True, True, False, False, True, True,   # Lunch
                True, True, True, False, False, False, True         # Dinner
            ],
            'is_gluten_free': [
                True, False, True, True, False, False, False, True, # Breakfast
                True, True, True, True, True, True, True, True,     # Snacks
                True, True, False, True, True, False, True, True,   # Lunch
                False, True, True, True, False, True, False         # Dinner
            ],
            'is_diabetic_friendly': [
                True, True, True, False, False, True, True, True,   # Breakfast
                True, True, True, False, True, False, True, False,  # Snacks
                True, True, True, False, True, True, True, True,    # Lunch
                True, True, True, True, True, True, True            # Dinner
            ],
            'is_keto_friendly': [
                False, False, False, False, False, False, False, True, # Breakfast
                True, True, False, False, False, True, False, False,   # Snacks
                False, False, False, False, True, True, False, False,  # Lunch
                False, False, False, True, True, True, False            # Dinner
            ],
            'is_high_protein': [
                False, False, True, False, True, False, False, True, # Breakfast
                False, False, False, False, False, True, True, False, # Snacks
                True, True, True, False, True, True, True, False,    # Lunch
                True, True, False, True, True, True, True           # Dinner
            ],
            'is_low_calorie': [
                False, True, False, True, False, True, True, True,  # Breakfast
                True, True, True, False, True, False, False, True,  # Snacks
                False, False, False, False, False, False, False, False, # Lunch
                False, False, False, True, False, False, True       # Dinner
            ]
        }
        return pd.DataFrame(sample_data)
    
    def _preprocess_food_data(self):
        """Preprocess food data"""
        numeric_columns = self.food_df.select_dtypes(include=[np.number]).columns
        self.food_df[numeric_columns] = self.food_df[numeric_columns].fillna(0)
        
        # Encode categorical variables
        categorical_columns = ['meal_category', 'veg_nonveg', 'region']
        self.label_encoders = {}
        
        for col in categorical_columns:
            if col in self.food_df.columns:
                le = LabelEncoder()
                self.food_df[col + '_encoded'] = le.fit_transform(self.food_df[col].astype(str))
                self.label_encoders[col] = le
    
    def run_complete_system(self):
        """Run the complete recommendation system"""
        print("🍽️  INDIAN FOOD NUTRITION & MEAL PLANNING SYSTEM")
        print("=" * 60)
        
        # Collect user data
        user_data = self.data_collector.collect_all_data()
        
        # Create comprehensive user profile
        user_profile = self.create_comprehensive_profile(user_data)
        
        # Generate weekly meal plan
        meal_planner = WeeklyMealPlanner(user_profile, self.food_df)
        weekly_plan = meal_planner.generate_weekly_plan()
        
        # Display results
        meal_planner.display_weekly_plan(weekly_plan)
        
        # Offer additional features
        self._offer_additional_features(user_profile, weekly_plan)
        
        return user_profile, weekly_plan
    
    def create_comprehensive_profile(self, user_data):
        """Create comprehensive user profile with all calculations"""
        profile = user_data.copy()
        
        # Calculate nutritional needs
        bmr = self.user_profiler.calculate_bmr(
            user_data['age'], user_data['gender'], 
            user_data['weight'], user_data['height']
        )
        
        tdee = self.user_profiler.calculate_tdee(bmr, user_data['activity_level'])
        target_calories = self.user_profiler.adjust_calories_for_goal(tdee, user_data['health_goal'])
        
        bmi = self.user_profiler.calculate_bmi(user_data['weight'], user_data['height'])
        bmi_category = self.user_profiler.get_bmi_category(bmi)
        
        # Calculate macronutrient targets
        protein_target = self._calculate_protein_target(user_data, target_calories)
        carb_target = self._calculate_carb_target(user_data, target_calories)
        fat_target = self._calculate_fat_target(target_calories, protein_target, carb_target)
        
        profile.update({
            'bmr': bmr,
            'tdee': tdee,
            'target_calories': target_calories,
            'bmi': bmi,
            'bmi_category': bmi_category,
            'protein_target': protein_target,
            'carb_target': carb_target,
            'fat_target': fat_target
        })
        
        return profile
    
    def _calculate_protein_target(self, user_data, target_calories):
        """Calculate daily protein target in grams"""
        weight = user_data['weight']
        goal = user_data['health_goal']
        activity = user_data['activity_level']
        
        if goal == 'muscle_gain':
            protein_per_kg = 2.0  # 2g per kg for muscle gain
        elif goal == 'weight_loss':
            protein_per_kg = 1.6  # Higher protein for weight loss
        elif activity in ['very_active', 'extremely_active']:
            protein_per_kg = 1.4  # Higher for active individuals
        else:
            protein_per_kg = 1.0  # Standard requirement
        
        return weight * protein_per_kg
    
    def _calculate_carb_target(self, user_data, target_calories):
        """Calculate daily carbohydrate target in grams"""
        goal = user_data['health_goal']
        restrictions = user_data.get('dietary_restrictions', [])
        
        if 'keto_friendly' in restrictions:
            carb_percentage = 0.05  # 5% for keto
        elif goal == 'weight_loss':
            carb_percentage = 0.30  # 30% for weight loss
        elif goal in ['muscle_gain', 'athletic_performance']:
            carb_percentage = 0.50  # 50% for performance
        else:
            carb_percentage = 0.40  # 40% standard
        
        carb_calories = target_calories * carb_percentage
        return carb_calories / 4  # 4 calories per gram of carbs
    
    def _calculate_fat_target(self, target_calories, protein_grams, carb_grams):
        """Calculate daily fat target in grams"""
        protein_calories = protein_grams * 4
        carb_calories = carb_grams * 4
        fat_calories = target_calories - protein_calories - carb_calories
        
        # Ensure fat is at least 20% of total calories
        min_fat_calories = target_calories * 0.20
        fat_calories = max(fat_calories, min_fat_calories)
        
        return fat_calories / 9  # 9 calories per gram of fat
    
    def _offer_additional_features(self, user_profile, weekly_plan):
        """Offer additional features and customizations"""
        print("\n🔧 ADDITIONAL FEATURES AVAILABLE:")
        print("-" * 40)
        print("1. Modify specific meals")
        print("2. Generate grocery shopping list")
        print("3. Get recipe suggestions")
        print("4. Export meal plan to file")
        print("5. Nutritional analysis report")
        
        while True:
            try:
                choice = input("\nSelect an option (1-5) or 'q' to quit: ").strip()
                
                if choice.lower() == 'q':
                    break
                elif choice == '1':
                    self._modify_meals(weekly_plan)
                elif choice == '2':
                    self._generate_shopping_list(weekly_plan)
                elif choice == '3':
                    self._suggest_recipes(user_profile)
                elif choice == '4':
                    self._export_meal_plan(weekly_plan, user_profile)
                elif choice == '5':
                    self._generate_nutrition_report(weekly_plan, user_profile)
                else:
                    print("Invalid option. Please try again.")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
    
    def _modify_meals(self, weekly_plan):
        """Allow user to modify specific meals"""
        print("\n📝 MEAL MODIFICATION")
        print("Available days:", ", ".join(weekly_plan.keys()))
        
        day = input("Enter day to modify: ").strip().title()
        if day not in weekly_plan:
            print("Invalid day selected.")
            return
        
        print(f"\nMeals for {day}:")
        meals = list(weekly_plan[day].keys())
        for i, meal in enumerate(meals, 1):
            meal_info = weekly_plan[day][meal]
            print(f"{i}. {meal.replace('_', ' ').title()}: {meal_info['dish_name']}")
        
        try:
            meal_choice = int(input("Select meal to modify (number): ")) - 1
            selected_meal = meals[meal_choice]
            
            print(f"\nCurrent meal: {weekly_plan[day][selected_meal]['dish_name']}")
            new_dish = input("Enter new dish name (or press Enter to keep current): ").strip()
            
            if new_dish:
                weekly_plan[day][selected_meal]['dish_name'] = new_dish
                print(f"✅ Updated {selected_meal} to {new_dish}")
            
        except (ValueError, IndexError):
            print("Invalid selection.")
    
    def _generate_shopping_list(self, weekly_plan):
        """Generate grocery shopping list"""
        print("\n🛒 GROCERY SHOPPING LIST")
        print("=" * 40)
        
        all_dishes = []
        for daily_plan in weekly_plan.values():
            for meal_info in daily_plan.values():
                all_dishes.append(meal_info['dish_name'])
        
        # Group common ingredients (simplified categorization)
        categories = {
            'Grains & Cereals': ['Rice', 'Roti', 'Bread', 'Oats', 'Poha', 'Upma', 'Daliya'],
            'Dals & Legumes': ['Dal', 'Rajma', 'Chole', 'Moong'],
            'Vegetables': ['Vegetable', 'Potato', 'Onion', 'Tomato'],
            'Proteins': ['Chicken', 'Fish', 'Paneer', 'Egg'],
            'Dairy': ['Milk', 'Curd', 'Cheese', 'Buttermilk'],
            'Fruits & Nuts': ['Apple', 'Banana', 'Almonds', 'Dates', 'Nuts'],
            'Spices & Others': ['Tea', 'Oil', 'Salt', 'Spices']
        }
        
        shopping_list = {category: set() for category in categories.keys()}
        
        for dish in all_dishes:
            dish_lower = dish.lower()
            categorized = False
            
            for category, keywords in categories.items():
                for keyword in keywords:
                    if keyword.lower() in dish_lower:
                        shopping_list[category].add(dish)
                        categorized = True
                        break
                if categorized:
                    break
            
            if not categorized:
                shopping_list['Spices & Others'].add(dish)
        
        for category, items in shopping_list.items():
            if items:
                print(f"\n{category}:")
                for item in sorted(items):
                    print(f"  • {item}")
    
    def _suggest_recipes(self, user_profile):
        """Suggest recipes based on preferences"""
        print("\n👨‍🍳 RECIPE SUGGESTIONS")
        print("=" * 30)
        
        food_type = user_profile.get('food_type', 'mixed')
        region_prefs = user_profile.get('regional_preferences', ['north_indian'])
        
        recipe_suggestions = {
            'Breakfast': [
                "🥣 Vegetable Poha: Soak poha, sauté with onions, mustard seeds, curry leaves",
                "🥞 Moong Dal Cheela: Mix moong dal batter with vegetables, make pancakes",
                "🍚 Vegetable Upma: Roast semolina, add vegetables and spices"
            ],
            'Lunch': [
                "🍛 Dal Tadka: Cook yellow dal, temper with cumin, garlic, ginger",
                "🍚 Vegetable Biryani: Layer rice with spiced vegetables",
                "🥘 Rajma Curry: Slow cook kidney beans with onion-tomato gravy"
            ],
            'Dinner': [
                "🥘 Mixed Vegetable Curry: Sauté seasonal vegetables with spices",
                "🍞 Whole Wheat Roti: Knead dough, roll and cook on tawa",
                "🥣 Khichdi: Cook rice and dal together with turmeric"
            ]
        }
        
        for meal_type, recipes in recipe_suggestions.items():
            print(f"\n{meal_type} Recipes:")
            for recipe in recipes:
                print(f"  {recipe}")
    
    def _export_meal_plan(self, weekly_plan, user_profile):
        """Export meal plan to text file"""
        filename = f"meal_plan_{user_profile.get('name', 'user').lower().replace(' ', '_')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("PERSONALIZED WEEKLY MEAL PLAN\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"User: {user_profile.get('name', 'User')}\n")
                f.write(f"Target Calories: {user_profile['target_calories']:.0f} kcal/day\n")
                f.write(f"Health Goal: {user_profile.get('health_goal', '').replace('_', ' ').title()}\n\n")
                
                for day, daily_plan in weekly_plan.items():
                    f.write(f"{day}\n")
                    f.write("-" * 20 + "\n")
                    
                    for meal_type, meal_info in daily_plan.items():
                        f.write(f"{meal_info.get('time', ''):<8} {meal_type.replace('_', ' ').title():<20} ")
                        f.write(f"{meal_info['dish_name']:<30} {meal_info['calories']:.0f} kcal\n")
                    f.write("\n")
            
            print(f"✅ Meal plan exported to '{filename}'")
            
        except Exception as e:
            print(f"❌ Error exporting file: {e}")
    
    def _generate_nutrition_report(self, weekly_plan, user_profile):
        """Generate detailed nutritional analysis report"""
        print("\n📊 DETAILED NUTRITIONAL ANALYSIS")
        print("=" * 50)
        
        weekly_totals = {
            'calories': 0, 'protein': 0, 'carbs': 0, 
            'fats': 0, 'fiber': 0, 'days': 0
        }
        
        for day, daily_plan in weekly_plan.items():
            daily_total = {'calories': 0, 'protein': 0, 'carbs': 0, 'fats': 0, 'fiber': 0}
            
            for meal_info in daily_plan.values():
                daily_total['calories'] += meal_info.get('calories', 0)
                daily_total['protein'] += meal_info.get('protein', 0)
                daily_total['carbs'] += meal_info.get('carbs', 0)
                daily_total['fats'] += meal_info.get('fats', 0)
                daily_total['fiber'] += meal_info.get('fiber', 0)
            
            for key in daily_total:
                weekly_totals[key] += daily_total[key]
            weekly_totals['days'] += 1
        
        # Calculate averages
        avg_calories = weekly_totals['calories'] / weekly_totals['days']
        avg_protein = weekly_totals['protein'] / weekly_totals['days']
        avg_carbs = weekly_totals['carbs'] / weekly_totals['days']
        avg_fats = weekly_totals['fats'] / weekly_totals['days']
        avg_fiber = weekly_totals['fiber'] / weekly_totals['days']
        
        target_calories = user_profile['target_calories']
        protein_target = user_profile.get('protein_target', 60)
        
        print(f"Daily Averages:")
        print(f"  Calories: {avg_calories:.0f} kcal (Target: {target_calories:.0f}) - {((avg_calories/target_calories-1)*100):+.1f}%")
        print(f"  Protein:  {avg_protein:.1f}g (Target: {protein_target:.0f}g) - {((avg_protein/protein_target-1)*100):+.1f}%")
        print(f"  Carbs:    {avg_carbs:.1f}g ({(avg_carbs*4/avg_calories*100):.1f}% of calories)")
        print(f"  Fats:     {avg_fats:.1f}g ({(avg_fats*9/avg_calories*100):.1f}% of calories)")
        print(f"  Fiber:    {avg_fiber:.1f}g")
        
        # Health recommendations
        print(f"\n🏥 Health Recommendations:")
        if avg_protein < protein_target * 0.8:
            print("  • ⚠️  Increase protein intake through dal, paneer, or chicken")
        if avg_fiber < 25:
            print("  • ⚠️  Add more fruits, vegetables, and whole grains for fiber")
        if (avg_fats * 9 / avg_calories) > 0.35:
            print("  • ⚠️  Consider reducing oil and fried foods")
        
        print("\n✅ Your meal plan provides balanced nutrition for your goals!")

# User Profile and Calorie Calculator classes (from original code)
class UserProfiler:
    """Handles user profiling and calorie need calculation"""
    
    def __init__(self):
        self.activity_multipliers = {
            'sedentary': 1.2,
            'lightly_active': 1.375,
            'moderately_active': 1.55,
            'very_active': 1.725,
            'extremely_active': 1.9
        }
    
    def calculate_bmr(self, age, gender, weight, height):
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        if gender.lower() == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        return bmr
    
    def calculate_tdee(self, bmr, activity_level):
        """Calculate Total Daily Energy Expenditure"""
        return bmr * self.activity_multipliers.get(activity_level, 1.2)
    
    def calculate_bmi(self, weight, height):
        """Calculate BMI"""
        height_m = height / 100  # Convert cm to meters
        return weight / (height_m ** 2)
    
    def get_bmi_category(self, bmi):
        """Get BMI category"""
        if bmi < 18.5:
            return 'underweight'
        elif 18.5 <= bmi < 25:
            return 'normal'
        elif 25 <= bmi < 30:
            return 'overweight'
        else:
            return 'obese'
    
    def adjust_calories_for_goal(self, tdee, goal):
        """Adjust calories based on health goal"""
        if goal == 'weight_loss':
            return tdee - 500  # 500 calorie deficit
        elif goal == 'weight_gain':
            return tdee + 500  # 500 calorie surplus
        else:
            return tdee  # maintenance

# Demonstration function
def run_demo():
    """Run a demonstration of the complete system"""
    print("🚀 RUNNING DEMO MODE")
    print("This demo shows how the system works with sample data.\n")
    
    system = EnhancedFoodRecommendationSystem()
    system.initialize_system()
    
    # Create sample user for demo
    sample_user = {
        'name': 'Demo User',
        'age': 28,
        'gender': 'female',
        'weight': 65,
        'height': 165,
        'activity_level': 'moderately_active',
        'health_goal': 'weight_loss',
        'target_weight': 60,
        'timeline': '3 months',
        'food_type': 'vegetarian',
        'regional_preferences': ['north_indian', 'south_indian'],
        'dietary_restrictions': ['diabetic_friendly'],
        'allergies': [],
        'dislikes': [],
        'meal_frequency': 5,
        'wake_time': '07:00',
        'sleep_time': '23:00',
        'exercises': True,
        'exercise_time': 'morning_fed',
        'health_conditions': [],
        'medications': [],
        'water_intake': 3.0
    }
    
    user_profile = system.create_comprehensive_profile(sample_user)
    meal_planner = WeeklyMealPlanner(user_profile, system.food_df)
    weekly_plan = meal_planner.generate_weekly_plan()
    meal_planner.display_weekly_plan(weekly_plan)

if __name__ == "__main__":
    # Choose between full system or demo
    mode = input("Choose mode - 'full' for complete system or 'demo' for demonstration: ").strip().lower()
    
    if mode == 'demo':
        run_demo()
    else:
        system = EnhancedFoodRecommendationSystem()
        system.initialize_system()
        system.run_complete_system()