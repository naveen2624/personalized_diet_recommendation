import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import warnings
from datetime import datetime, timedelta
import json
warnings.filterwarnings('ignore')

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
        
        food_type = int(input("Select food type (1-3): "))
        food_type_map = {1: 'Vegetarian', 2: 'Non-Vegetarian', 3: 'Vegan'}
        
        # Regional preferences
        print("\nRegional Cuisine Preferences (select multiple, comma-separated):")
        print("1. North Indian  2. South Indian  3. Pan Indian  4. East Indian")
        print("5. West Indian  6. No preference")
        
        region_input = input("Enter numbers (e.g., 1,2,3): ").strip()
        region_map = {
            '1': 'North Indian', '2': 'South Indian', '3': 'Pan Indian', 
            '4': 'East Indian', '5': 'West Indian', '6': 'Pan Indian'
        }
        
        regions = [region_map[r.strip()] for r in region_input.split(',') if r.strip() in region_map]
        if not regions:
            regions = ['Pan Indian']
        
        # Dietary restrictions (based on dataset columns)
        print("\nDietary Restrictions (select multiple, comma-separated):")
        print("1. Vegan  2. Gluten-Free  3. Dairy-Free  4. Nut-Free")
        print("5. Diabetic-Friendly  6. Keto-Friendly  7. Jain-Friendly")
        print("8. Low-Calorie  9. Low-Sodium  10. None")
        
        restrictions_input = input("Enter numbers (e.g., 1,3,6): ").strip()
        restriction_map = {
            '1': 'is_vegan', '2': 'is_gluten_free', '3': 'is_dairy_free',
            '4': 'is_nut_free', '5': 'is_diabetic_friendly', '6': 'is_keto_friendly',
            '7': 'is_jain_friendly', '8': 'is_low_calorie', '9': 'is_low_sodium', '10': 'none'
        }
        
        restrictions = [restriction_map[r.strip()] for r in restrictions_input.split(',') 
                       if r.strip() in restriction_map and restriction_map[r.strip()] != 'none']
        
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
    """Generate comprehensive weekly meal schedules using real dataset"""
    
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
        """Filter foods based on meal type and dietary restrictions using real dataset"""
        filtered_df = self.food_df.copy()
        
        # Apply food type restrictions (vegetarian/non-vegetarian)
        food_type = self.user_profile.get('food_type', 'Non-Vegetarian')
        if food_type in ['Vegetarian', 'Vegan']:
            filtered_df = filtered_df[filtered_df['veg_nonveg'] == 'Vegetarian']
        
        # Apply regional preferences
        regional_prefs = self.user_profile.get('regional_preferences', ['Pan Indian'])
        if regional_prefs and 'Pan Indian' not in regional_prefs:
            filtered_df = filtered_df[filtered_df['region'].isin(regional_prefs)]
        
        # Apply dietary restrictions based on dataset columns
        restrictions = self.user_profile.get('dietary_restrictions', [])
        for restriction in restrictions:
            if restriction in filtered_df.columns:
                # For binary restriction columns, filter for True values
                filtered_df = filtered_df[filtered_df[restriction] == 1]
        
        # Filter by meal category if available
        if 'meal_category' in filtered_df.columns:
            # Map our meal types to dataset categories
            meal_category_map = {
                'breakfast': 'Main Course',  # Most breakfast items are in Main Course
                'lunch': 'Main Course',
                'dinner': 'Main Course',
                'pre_breakfast': 'Main Course',
                'pre_lunch': 'Main Course',
                'mid_morning_snack': 'Dessert',
                'mid_afternoon_snack': 'Dessert',
                'evening_snack': 'Dessert'
            }
            
            if meal_type in meal_category_map:
                category = meal_category_map[meal_type]
                category_foods = filtered_df[filtered_df['meal_category'] == category]
                if len(category_foods) > 0:
                    filtered_df = category_foods
        
        # Filter by calorie range (±40% of target for more flexibility)
        # Ensure calorie_target is valid
        if calorie_target <= 0:
            calorie_target = 300  # Default fallback value
        
        calorie_min = calorie_target * 0.6
        calorie_max = calorie_target * 1.4
        
        # Ensure calories column exists and has valid values
        if 'calories_(kcal)' in filtered_df.columns:
            filtered_df = filtered_df[
                (filtered_df['calories_(kcal)'] >= calorie_min) & 
                (filtered_df['calories_(kcal)'] <= calorie_max) &
                (filtered_df['calories_(kcal)'] > 0)  # Ensure positive calories
            ]
        
        # Remove foods user dislikes
        dislikes = self.user_profile.get('dislikes', [])
        for dislike in dislikes:
            if 'dish_name' in filtered_df.columns:
                filtered_df = filtered_df[~filtered_df['dish_name'].str.contains(dislike, case=False, na=False)]
        
        return filtered_df
    def _get_meal_variety(self, meal_type, options, day_num, used_foods):
        """Ensure variety in meal selection across the week"""
        if len(options) == 0:
            return options
        
        # Remove already used foods for variety
        available_options = options[~options['dish_name'].isin(used_foods)]
        
        if len(available_options) == 0:
            available_options = options  # Fall back to original if no variety possible
        
        # Score foods based on user goals
        scored_options = self._score_foods(available_options, meal_type)
        
        return scored_options.head(1)
    
    def _score_foods(self, df, meal_type):
        """Score foods based on user health goals and nutritional content"""
        if len(df) == 0:
            return df
        
        df = df.copy()
        scores = np.zeros(len(df))
        health_goal = self.user_profile.get('health_goal', 'weight_maintenance')
        
        # Base nutritional scoring using actual dataset columns
        calories = df['calories_(kcal)'].fillna(0)
        protein = df['protein_(g)'].fillna(0)
        carbs = df['carbohydrates_(g)'].fillna(0)
        fats = df['fats_(g)'].fillna(0)
        fiber = df['fibre_(g)'].fillna(0)
        
        # Safe division - avoid division by zero
        def safe_divide(numerator, denominator, default=0):
            return np.where(denominator > 0, numerator / denominator, default)
        
        if health_goal == 'weight_loss':
            scores += safe_divide(protein, calories, 0) * 100  # High protein efficiency
            scores += safe_divide(fiber, calories, 0) * 80     # High fiber for satiety
            scores -= safe_divide(fats, calories, 0) * 40      # Lower fat preference
            # Bonus for low-calorie foods
            if 'is_low_calorie' in df.columns:
                scores += df['is_low_calorie'].fillna(0) * 30
            
        elif health_goal == 'weight_gain':
            scores += calories / 50  # Higher calories preferred
            scores += protein * 3    # Good protein content
            scores += fats * 2       # Healthy fats for calories
            
        elif health_goal == 'muscle_gain':
            scores += protein * 5    # Very high protein preference
            scores += safe_divide(protein, calories, 0) * 150
            # Bonus for high-protein foods
            if 'is_high_protein' in df.columns:
                scores += df['is_high_protein'].fillna(0) * 50
            
        # Meal-specific adjustments
        if meal_type in ['pre_breakfast', 'pre_lunch']:
            scores += (300 - calories) / 100  # Prefer lighter options
            scores += carbs * 2               # Quick energy
            
        elif meal_type == 'breakfast':
            scores += protein * 2    # Good protein to start day
            scores += fiber * 3      # Fiber for sustained energy
            
        elif meal_type in ['mid_morning_snack', 'mid_afternoon_snack', 'evening_snack']:
            scores += (200 - calories) / 100  # Prefer lighter snacks
            scores += protein * 2    # Protein for satiety
        
        # Apply dietary restriction bonuses
        restrictions = self.user_profile.get('dietary_restrictions', [])
        for restriction in restrictions:
            if restriction in df.columns:
                scores += df[restriction].fillna(0) * 20
        
        # Penalize high sodium for health-conscious users
        if 'sodium_(mg)' in df.columns:
            sodium = df['sodium_(mg)'].fillna(0)
            scores -= sodium / 100
        
        # Boost foods with high nutrients
        if 'calcium_(mg)' in df.columns:
            scores += df['calcium_(mg)'].fillna(0) / 100
        if 'iron_(mg)' in df.columns:
            scores += df['iron_(mg)'].fillna(0) * 10
        if 'vitamin_c_(mg)' in df.columns:
            scores += df['vitamin_c_(mg)'].fillna(0) / 10
        
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
                            'sodium': meal_info.get('sodium_(mg)', 0),
                            'calcium': meal_info.get('calcium_(mg)', 0),
                            'iron': meal_info.get('iron_(mg)', 0),
                            'vitamin_c': meal_info.get('vitamin_c_(mg)', 0),
                            'target_calories': calorie_target,
                            'meal_category': meal_info.get('meal_category', ''),
                            'region': meal_info.get('region', ''),
                            'veg_nonveg': meal_info.get('veg_nonveg', '')
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
            'pre_breakfast': {'dish_name': 'Green Tea with Honey', 'calories': 25},
            'breakfast': {'dish_name': 'Poha with Vegetables', 'calories': 250},
            'mid_morning_snack': {'dish_name': 'Fresh Fruit', 'calories': 80},
            'pre_lunch': {'dish_name': 'Buttermilk', 'calories': 60},
            'lunch': {'dish_name': 'Dal Rice with Vegetables', 'calories': 400},
            'mid_afternoon_snack': {'dish_name': 'Nuts and Seeds', 'calories': 150},
            'evening_snack': {'dish_name': 'Herbal Tea with Biscuits', 'calories': 100},
            'dinner': {'dish_name': 'Vegetable Curry with Roti', 'calories': 350}
        }
        
        fallback = fallback_meals.get(meal_type, {'dish_name': 'Healthy Meal', 'calories': calorie_target})
        fallback.update({
            'protein': 8,
            'carbs': 45,
            'fats': 6,
            'fiber': 4,
            'sodium': 200,
            'calcium': 50,
            'iron': 2,
            'vitamin_c': 5,
            'target_calories': calorie_target,
            'meal_category': 'Fallback',
            'region': 'Pan Indian',
            'veg_nonveg': 'Vegetarian',
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
        total_sodium = sum(meal.get('sodium', 0) for meal in daily_plan.values())
        total_calcium = sum(meal.get('calcium', 0) for meal in daily_plan.values())
        total_iron = sum(meal.get('iron', 0) for meal in daily_plan.values())
        total_vitamin_c = sum(meal.get('vitamin_c', 0) for meal in daily_plan.values())
        
        return {
            'total_calories': total_calories,
            'total_protein': total_protein,
            'total_carbs': total_carbs,
            'total_fats': total_fats,
            'total_fiber': total_fiber,
            'total_sodium': total_sodium,
            'total_calcium': total_calcium,
            'total_iron': total_iron,
            'total_vitamin_c': total_vitamin_c,
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
        print(f"Regional Preferences: {', '.join(self.user_profile.get('regional_preferences', ['Pan Indian']))}")
        print()
        
        for day, daily_plan in weekly_plan.items():
            print(f"\n📅 {day.upper()}")
            print("-" * 70)
            
            for meal_type, meal_info in daily_plan.items():
                time = meal_info.get('time', '')
                dish = meal_info.get('dish_name', 'Not specified')
                calories = meal_info.get('calories', 0)
                protein = meal_info.get('protein', 0)
                region = meal_info.get('region', '')
                veg_status = meal_info.get('veg_nonveg', '')
                
                meal_display = meal_type.replace('_', ' ').title()
                print(f"{time:>6} | {meal_display:<18} | {dish:<30} | {calories:>3.0f} kcal")
                print(f"       | {'':18} | P:{protein:>4.1f}g | {region} | {veg_status}")
            
            # Daily summary
            summary = self.get_daily_summary(daily_plan)
            print(f"       | {'DAILY TOTAL':<18} | {'':<30} | {summary['total_calories']:>3.0f} kcal")
            print(f"       | {'Nutrients':<18} | P:{summary['total_protein']:>4.1f}g C:{summary['total_carbs']:>4.1f}g F:{summary['total_fats']:>4.1f}g Fiber:{summary['total_fiber']:>4.1f}g")
            
            # Show if over/under target
            diff = summary['calorie_difference']
            if abs(diff) > 50:
                status = "⚠️  OVER" if diff > 0 else "⚠️  UNDER"
                print(f"       | {status:<18} | Target: {summary['target_calories']:.0f} kcal | Diff: {diff:+.0f} kcal")
        
        # Weekly summary
        self._display_weekly_summary(weekly_plan)
    
    def _display_weekly_summary(self, weekly_plan):
        """Display weekly nutritional summary"""
        weekly_totals = {
            'calories': 0, 'protein': 0, 'carbs': 0, 'fats': 0, 
            'fiber': 0, 'sodium': 0, 'calcium': 0, 'iron': 0, 'vitamin_c': 0
        }
        
        for daily_plan in weekly_plan.values():
            summary = self.get_daily_summary(daily_plan)
            weekly_totals['calories'] += summary['total_calories']
            weekly_totals['protein'] += summary['total_protein']
            weekly_totals['carbs'] += summary['total_carbs']
            weekly_totals['fats'] += summary['total_fats']
            weekly_totals['fiber'] += summary['total_fiber']
            weekly_totals['sodium'] += summary['total_sodium']
            weekly_totals['calcium'] += summary['total_calcium']
            weekly_totals['iron'] += summary['total_iron']
            weekly_totals['vitamin_c'] += summary['total_vitamin_c']
        
        avg_daily_calories = weekly_totals['calories'] / 7
        avg_daily_protein = weekly_totals['protein'] / 7
        avg_daily_fiber = weekly_totals['fiber'] / 7
        avg_daily_sodium = weekly_totals['sodium'] / 7
        avg_daily_calcium = weekly_totals['calcium'] / 7
        avg_daily_iron = weekly_totals['iron'] / 7
        avg_daily_vitamin_c = weekly_totals['vitamin_c'] / 7
        
        target_calories = self.user_profile['target_calories']
        
        print("\n" + "="*80)
        print("WEEKLY NUTRITIONAL SUMMARY")
        print("="*80)
        print(f"Average Daily Calories: {avg_daily_calories:.0f} kcal (Target: {target_calories:.0f} kcal)")
        print(f"Average Daily Protein: {avg_daily_protein:.1f}g")
        print(f"Average Daily Fiber: {avg_daily_fiber:.1f}g")
        print(f"Average Daily Sodium: {avg_daily_sodium:.0f}mg")
        print(f"Average Daily Calcium: {avg_daily_calcium:.0f}mg")
        print(f"Average Daily Iron: {avg_daily_iron:.1f}mg")
        print(f"Average Daily Vitamin C: {avg_daily_vitamin_c:.1f}mg")
        print(f"Weekly Calorie Difference: {(avg_daily_calories - target_calories) * 7:.0f} kcal")
        
        # Recommendations based on nutritional analysis
        print("\n📝 NUTRITIONAL RECOMMENDATIONS:")
        if avg_daily_calories < target_calories - 100:
            print("• Consider adding healthy snacks or increasing portion sizes")
        elif avg_daily_calories > target_calories + 100:
            print("• Consider reducing portion sizes or choosing lower-calorie alternatives")
        else:
            print("• Your meal plan is well-balanced for your calorie goals!")
        
        if avg_daily_protein < 50:
            print("• Consider adding more protein-rich foods like dal, paneer, or lean meats")
        
        if avg_daily_fiber < 25:
            print("• Add more fruits, vegetables, and whole grains for adequate fiber intake")
        
        if avg_daily_sodium > 2300:
            print("• Consider reducing sodium intake by choosing low-sodium alternatives")
        
        if avg_daily_calcium < 800:
            print("• Include more dairy products or calcium-rich foods like sesame seeds")
        
        if avg_daily_iron < 8:
            print("• Include iron-rich foods like spinach, lentils, and jaggery")
        
        print("\n💡 TIPS:")
        print("• Stay hydrated - aim for 8-10 glasses of water daily")
        print("• Listen to your body and adjust portions as needed")
        print("• Include variety in vegetables and fruits for better nutrition")
        print("• Try to eat meals at consistent times for better digestion")

# Enhanced Food Recommendation System with real dataset integration
class EnhancedFoodRecommendationSystem:
    """Enhanced system with comprehensive meal planning using real dataset"""
    
    def __init__(self):
        self.user_profiler = UserProfiler()
        self.data_collector = UserDataCollector()
        self.food_df = None
    
    def initialize_system(self, food_data_path='indian_food_nutrition.csv'):
        """Initialize system with real dataset"""
        try:
            # Try to load the main dataset first
            if food_data_path == 'indian_food_nutrition.csv':
                self.food_df = pd.read_csv('indian_food_nutrition.csv')
                print("✅ Loaded main Indian food dataset successfully!")
            else:
                # Fallback to smaller dataset
                self.food_df = pd.read_csv('food_dataset.csv')
                print("✅ Loaded sample food dataset successfully!")
            
            print(f"Dataset contains {len(self.food_df)} food items")
            self._preprocess_food_data()
            self._analyze_dataset()
            
        except FileNotFoundError:
            print("❌ Dataset file not found. Creating minimal sample data...")
            self.food_df = self._create_minimal_sample_data()
            self._preprocess_food_data()
    
    def _analyze_dataset(self):
        """Analyze and display dataset information"""
        print("\n📊 DATASET ANALYSIS:")
        print(f"Total dishes: {len(self.food_df)}")
        
        if 'veg_nonveg' in self.food_df.columns:
            veg_counts = self.food_df['veg_nonveg'].value_counts()
            print(f"Vegetarian dishes: {veg_counts.get('Vegetarian', 0)}")
            print(f"Non-vegetarian dishes: {veg_counts.get('Non-Vegetarian', 0)}")
        
        if 'region' in self.food_df.columns:
            region_counts = self.food_df['region'].value_counts()
            print(f"Regional distribution: {dict(region_counts.head())}")
        
        if 'meal_category' in self.food_df.columns:
            meal_counts = self.food_df['meal_category'].value_counts()
            print(f"Meal categories: {dict(meal_counts)}")
        
        # Check for dietary restriction columns
        restriction_cols = [col for col in self.food_df.columns if col.startswith('is_')]
        print(f"Available dietary filters: {len(restriction_cols)} types")
        
        print()
    
    def _create_minimal_sample_data(self):
        """Create minimal sample data if dataset not found"""
        sample_data = {
            'dish_name': [
                'Poha', 'Upma', 'Idli Sambar', 'Dosa', 'Paratha',
                'Dal Rice', 'Rajma Rice', 'Chole Bhature', 'Biryani',
                'Roti Sabzi', 'Khichdi', 'Sambar Rice'
            ],
            'calories_(kcal)': [250, 200, 300, 150, 350, 400, 450, 500, 550, 320, 280, 350],
            'protein_(g)': [6, 5, 12, 4, 12, 15, 18, 16, 20, 12, 10, 14],
            'carbohydrates_(g)': [45, 35, 50, 25, 40, 65, 70, 60, 75, 45, 50, 60],
            'fats_(g)': [8, 6, 5, 3, 15, 12, 8, 15, 18, 8, 6, 8],
            'fibre_(g)': [4, 3, 3, 2, 2, 8, 10, 6, 4, 6, 4, 6],
            'sodium_(mg)': [300, 400, 500, 200, 450, 600, 700, 800, 650, 500, 400, 550],
            'calcium_(mg)': [50, 30, 100, 60, 120, 80, 60, 90, 70, 90, 70, 120],
            'iron_(mg)': [2, 1, 3, 1, 2, 4, 5, 4, 3, 3, 2, 4],
            'vitamin_c_(mg)': [5, 3, 8, 2, 4, 10, 12, 8, 6, 15, 8, 10],
            'meal_category': ['Main Course'] * 12,
            'veg_nonveg': ['Vegetarian'] * 12,
            'region': ['Pan Indian'] * 12,
            'is_vegan': [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1],
            'is_gluten_free': [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1],
            'is_diabetic_friendly': [1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1],
            'is_low_calorie': [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
            'is_high_protein': [0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1]
        }
        return pd.DataFrame(sample_data)
    
    def _preprocess_food_data(self):
        """Preprocess food data for analysis"""
        # Fill missing numeric values
        numeric_columns = self.food_df.select_dtypes(include=[np.number]).columns
        self.food_df[numeric_columns] = self.food_df[numeric_columns].fillna(0)
        
        # Fill missing categorical values
        categorical_columns = ['meal_category', 'veg_nonveg', 'region']
        for col in categorical_columns:
            if col in self.food_df.columns:
                self.food_df[col] = self.food_df[col].fillna('Unknown')
        
        # Ensure binary columns are properly formatted
        binary_columns = [col for col in self.food_df.columns if col.startswith('is_')]
        for col in binary_columns:
            if col in self.food_df.columns:
                # Convert to 1/0 if they're boolean or string
                self.food_df[col] = self.food_df[col].astype(str).str.lower()
                self.food_df[col] = self.food_df[col].map({'true': 1, '1': 1, 'yes': 1}).fillna(0).astype(int)
        
        # Clean dish names
        if 'dish_name' in self.food_df.columns:
            self.food_df['dish_name'] = self.food_df['dish_name'].astype(str).str.strip()
        
        # Create calorie categories for easier filtering
        if 'calories_(kcal)' in self.food_df.columns:
            self.food_df['calorie_category'] = pd.cut(
                self.food_df['calories_(kcal)'], 
                bins=[0, 100, 200, 300, 500, float('inf')], 
                labels=['Very Low', 'Low', 'Medium', 'High', 'Very High']
            )
    
    def run_complete_system(self):
        """Run the complete recommendation system"""
        print("🍽️  INDIAN FOOD NUTRITION & MEAL PLANNING SYSTEM")
        print("=" * 60)
        
        # Collect user data
        user_data = self.data_collector.collect_all_data()
        
        # Create comprehensive user profile
        user_profile = self.create_comprehensive_profile(user_data)
        
        # Display user profile summary
        self._display_user_profile(user_profile)
        
        # Generate weekly meal plan
        meal_planner = WeeklyMealPlanner(user_profile, self.food_df)
        weekly_plan = meal_planner.generate_weekly_plan()
        
        # Display results
        meal_planner.display_weekly_plan(weekly_plan)
        
        # Offer additional features
        self._offer_additional_features(user_profile, weekly_plan)
        
        return user_profile, weekly_plan
    
    def _display_user_profile(self, user_profile):
        """Display user profile summary"""
        print("\n" + "="*60)
        print("USER PROFILE SUMMARY")
        print("="*60)
        print(f"Name: {user_profile.get('name', 'User')}")
        print(f"Age: {user_profile.get('age')} years")
        print(f"Gender: {user_profile.get('gender', '').title()}")
        print(f"Height: {user_profile.get('height')} cm")
        print(f"Weight: {user_profile.get('weight')} kg")
        print(f"BMI: {user_profile.get('bmi', 0):.1f} ({user_profile.get('bmi_category', '').title()})")
        print(f"Activity Level: {user_profile.get('activity_level', '').replace('_', ' ').title()}")
        print(f"Health Goal: {user_profile.get('health_goal', '').replace('_', ' ').title()}")
        print(f"Food Type: {user_profile.get('food_type', '')}")
        print(f"Regional Preferences: {', '.join(user_profile.get('regional_preferences', []))}")
        
        dietary_restrictions = user_profile.get('dietary_restrictions', [])
        if dietary_restrictions:
            readable_restrictions = [r.replace('is_', '').replace('_', ' ').title() for r in dietary_restrictions]
            print(f"Dietary Restrictions: {', '.join(readable_restrictions)}")
        
        print(f"\n📊 CALCULATED NUTRITIONAL NEEDS:")
        print(f"BMR (Basal Metabolic Rate): {user_profile.get('bmr', 0):.0f} kcal/day")
        print(f"TDEE (Total Daily Energy): {user_profile.get('tdee', 0):.0f} kcal/day")
        print(f"Target Daily Calories: {user_profile.get('target_calories', 0):.0f} kcal/day")
        print(f"Target Daily Protein: {user_profile.get('protein_target', 0):.0f}g")
        print(f"Target Daily Carbohydrates: {user_profile.get('carb_target', 0):.0f}g")
        print(f"Target Daily Fats: {user_profile.get('fat_target', 0):.0f}g")
        print()
    
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
        
        if 'is_keto_friendly' in restrictions:
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
        print("3. Get detailed nutritional analysis")
        print("4. Export meal plan to file")
        print("5. Recipe suggestions")
        print("6. Alternative meal options")
        
        while True:
            try:
                choice = input("\nSelect an option (1-6) or 'q' to quit: ").strip()
                
                if choice.lower() == 'q':
                    break
                elif choice == '1':
                    self._modify_meals(weekly_plan)
                elif choice == '2':
                    self._generate_shopping_list(weekly_plan)
                elif choice == '3':
                    self._detailed_nutrition_analysis(weekly_plan, user_profile)
                elif choice == '4':
                    self._export_meal_plan(weekly_plan, user_profile)
                elif choice == '5':
                    self._suggest_recipes(user_profile)
                elif choice == '6':
                    self._show_alternatives(weekly_plan, user_profile)
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
            print(f"{i}. {meal.replace('_', ' ').title()}: {meal_info['dish_name']} ({meal_info['calories']:.0f} kcal)")
        
        try:
            meal_choice = int(input("Select meal to modify (number): ")) - 1
            selected_meal = meals[meal_choice]
            
            print(f"\nCurrent meal: {weekly_plan[day][selected_meal]['dish_name']}")
            
            # Show alternatives from dataset
            current_calories = weekly_plan[day][selected_meal]['calories']
            alternatives = self.food_df[
                (self.food_df['calories_(kcal)'] >= current_calories * 0.8) &
                (self.food_df['calories_(kcal)'] <= current_calories * 1.2)
            ].head(5)
            
            if len(alternatives) > 0:
                print("\nSuggested alternatives:")
                for i, (_, food) in enumerate(alternatives.iterrows(), 1):
                    print(f"{i}. {food['dish_name']} ({food['calories_(kcal)']:.0f} kcal)")
                
                alt_choice = input("Select alternative (number) or enter custom dish name: ").strip()
                
                if alt_choice.isdigit() and 1 <= int(alt_choice) <= len(alternatives):
                    selected_alt = alternatives.iloc[int(alt_choice) - 1]
                    weekly_plan[day][selected_meal].update({
                        'dish_name': selected_alt['dish_name'],
                        'calories': selected_alt['calories_(kcal)'],
                        'protein': selected_alt['protein_(g)'],
                        'carbs': selected_alt['carbohydrates_(g)'],
                        'fats': selected_alt['fats_(g)']
                    })
                    print(f"✅ Updated {selected_meal} to {selected_alt['dish_name']}")
                elif alt_choice:
                    weekly_plan[day][selected_meal]['dish_name'] = alt_choice
                    print(f"✅ Updated {selected_meal} to {alt_choice}")
            else:
                new_dish = input("Enter new dish name: ").strip()
                if new_dish:
                    weekly_plan[day][selected_meal]['dish_name'] = new_dish
                    print(f"✅ Updated {selected_meal} to {new_dish}")
            
        except (ValueError, IndexError):
            print("Invalid selection.")
    
    def _generate_shopping_list(self, weekly_plan):
        """Generate comprehensive grocery shopping list"""
        print("\n🛒 COMPREHENSIVE GROCERY SHOPPING LIST")
        print("=" * 50)
        
        all_dishes = []
        dish_counts = {}
        
        for daily_plan in weekly_plan.values():
            for meal_info in daily_plan.values():
                dish = meal_info['dish_name']
                all_dishes.append(dish)
                dish_counts[dish] = dish_counts.get(dish, 0) + 1
        
        # Categorize ingredients based on common Indian cooking patterns
        categories = {
            'Grains & Cereals': ['rice', 'roti', 'bread', 'oats', 'poha', 'upma', 'daliya', 'wheat', 'atta'],
            'Dals & Legumes': ['dal', 'rajma', 'chole', 'moong', 'masoor', 'toor', 'urad', 'chana'],
            'Vegetables': ['vegetable', 'potato', 'onion', 'tomato', 'spinach', 'cauliflower', 'okra', 'brinjal'],
            'Proteins': ['chicken', 'fish', 'paneer', 'egg', 'mutton', 'prawn', 'tofu'],
            'Dairy & Alternatives': ['milk', 'curd', 'cheese', 'buttermilk', 'ghee', 'butter'],
            'Fruits & Nuts': ['apple', 'banana', 'mango', 'orange', 'almonds', 'cashew', 'dates', 'nuts'],
            'Spices & Condiments': ['masala', 'curry', 'pickle', 'chutney', 'sauce'],
            'Beverages': ['tea', 'coffee', 'juice', 'lassi', 'chaas'],
            'Others': []
        }
        
        shopping_list = {category: {} for category in categories.keys()}
        
        for dish, count in dish_counts.items():
            dish_lower = dish.lower()
            categorized = False
            
            for category, keywords in categories.items():
                for keyword in keywords:
                    if keyword in dish_lower:
                        shopping_list[category][dish] = count
                        categorized = True
                        break
                if categorized:
                    break
            
            if not categorized:
                shopping_list['Others'][dish] = count
        
        # Display organized shopping list
        for category, items in shopping_list.items():
            if items:
                print(f"\n{category.upper()}:")
                for item, count in sorted(items.items()):
                    frequency = f"({count}x this week)" if count > 1 else ""
                    print(f"  • {item} {frequency}")
        
        # Generate estimated quantities
        print(f"\n📦 ESTIMATED WEEKLY QUANTITIES:")
        print(f"  • Rice: 2-3 kg")
        print(f"  • Wheat flour: 1-2 kg") 
        print(f"  • Dal (mixed): 500g")
        print(f"  • Vegetables: 3-4 kg")
        print(f"  • Milk: 3-4 liters")
        print(f"  • Oil: 500ml")
        print(f"  • Onions: 1 kg")
        print(f"  • Tomatoes: 1 kg")
        
    def _detailed_nutrition_analysis(self, weekly_plan, user_profile):
        """Provide detailed nutritional analysis"""
        print("\n📊 DETAILED NUTRITIONAL ANALYSIS")
        print("=" * 60)
        
        # Calculate daily averages
        daily_totals = []
        for day, daily_plan in weekly_plan.items():
            day_total = {
                'day': day,
                'calories': sum(meal.get('calories', 0) for meal in daily_plan.values()),
                'protein': sum(meal.get('protein', 0) for meal in daily_plan.values()),
                'carbs': sum(meal.get('carbs', 0) for meal in daily_plan.values()),
                'fats': sum(meal.get('fats', 0) for meal in daily_plan.values()),
                'fiber': sum(meal.get('fiber', 0) for meal in daily_plan.values()),
                'sodium': sum(meal.get('sodium', 0) for meal in daily_plan.values()),
                'calcium': sum(meal.get('calcium', 0) for meal in daily_plan.values()),
                'iron': sum(meal.get('iron', 0) for meal in daily_plan.values()),
                'vitamin_c': sum(meal.get('vitamin_c', 0) for meal in daily_plan.values())
            }
            daily_totals.append(day_total)
        
        # Calculate averages
        avg_calories = np.mean([d['calories'] for d in daily_totals])
        avg_protein = np.mean([d['protein'] for d in daily_totals])
        avg_carbs = np.mean([d['carbs'] for d in daily_totals])
        avg_fats = np.mean([d['fats'] for d in daily_totals])
        avg_fiber = np.mean([d['fiber'] for d in daily_totals])
        avg_sodium = np.mean([d['sodium'] for d in daily_totals])
        avg_calcium = np.mean([d['calcium'] for d in daily_totals])
        avg_iron = np.mean([d['iron'] for d in daily_totals])
        avg_vitamin_c = np.mean([d['vitamin_c'] for d in daily_totals])
        
        # Display analysis - use safe division
        target_calories = user_profile['target_calories']
        protein_target = user_profile.get('protein_target', 60)
        
        print(f"MACRONUTRIENT ANALYSIS:")
        print(f"  Average Daily Calories: {avg_calories:.0f} kcal (Target: {target_calories:.0f})")
        if target_calories > 0:
            print(f"  Calorie Variance: {((avg_calories/target_calories-1)*100):+.1f}%")
        else:
            print(f"  Calorie Variance: N/A (invalid target)")
            
        print(f"  Average Daily Protein: {avg_protein:.1f}g (Target: {protein_target:.0f}g)")
        if protein_target > 0:
            print(f"  Protein Variance: {((avg_protein/protein_target-1)*100):+.1f}%")
        else:
            print(f"  Protein Variance: N/A (invalid target)")
            
        if avg_calories > 0:
            print(f"  Average Daily Carbs: {avg_carbs:.1f}g ({(avg_carbs*4/avg_calories*100):.1f}% of calories)")
            print(f"  Average Daily Fats: {avg_fats:.1f}g ({(avg_fats*9/avg_calories*100):.1f}% of calories)")
        else:
            print(f"  Average Daily Carbs: {avg_carbs:.1f}g (N/A% of calories)")
            print(f"  Average Daily Fats: {avg_fats:.1f}g (N/A% of calories)")
        
        print(f"\nMICRONUTRIENT ANALYSIS:")
        print(f"  Average Daily Fiber: {avg_fiber:.1f}g (Recommended: 25-30g)")
        print(f"  Average Daily Sodium: {avg_sodium:.0f}mg (Recommended: <2300mg)")
        print(f"  Average Daily Calcium: {avg_calcium:.0f}mg (Recommended: 1000mg)")
        print(f"  Average Daily Iron: {avg_iron:.1f}mg (Recommended: 8-18mg)")
        print(f"  Average Daily Vitamin C: {avg_vitamin_c:.1f}mg (Recommended: 65-90mg)")
        
        # Health recommendations
        print(f"\n🏥 PERSONALIZED HEALTH RECOMMENDATIONS:")
        
        if protein_target > 0:
            if avg_protein < protein_target * 0.8:
                print("  • ⚠️  PROTEIN: Increase protein intake through dal, paneer, eggs, or lean meats")
            elif avg_protein > protein_target * 1.2:
                print("  • ✅ PROTEIN: Excellent protein intake for your goals")
            else:
                print("  • ✅ PROTEIN: Good protein intake")
        else:
            print("  • ⚠️  PROTEIN: Unable to assess - invalid protein target")
            
        if avg_fiber < 20:
            print("  • ⚠️  FIBER: Add more fruits, vegetables, and whole grains to reach 25-30g daily")
        else:
            print("  • ✅ FIBER: Good fiber intake for digestive health")
            
        if avg_sodium > 2300:
            print("  • ⚠️  SODIUM: Reduce salt intake and choose low-sodium alternatives")
        else:
            print("  • ✅ SODIUM: Sodium intake within healthy limits")
            
        if avg_calcium < 800:
            print("  • ⚠️  CALCIUM: Include more dairy, sesame seeds, or green leafy vegetables")
        else:
            print("  • ✅ CALCIUM: Good calcium intake for bone health")
            
        if avg_iron < 8:
            print("  • ⚠️  IRON: Add iron-rich foods like spinach, lentils, jaggery, or dates")
        else:
            print("  • ✅ IRON: Adequate iron intake")
            
        if avg_vitamin_c < 60:
            print("  • ⚠️  VITAMIN C: Include more citrus fruits, tomatoes, or bell peppers")
        else:
            print("  • ✅ VITAMIN C: Good vitamin C intake for immunity")
        
        # Display daily variations
        print(f"\n📈 DAILY VARIATIONS:")
        for day_data in daily_totals:
            cal_diff = day_data['calories'] - target_calories
            status = "⚠️ " if abs(cal_diff) > 100 else "✅ "
            print(f"  {day_data['day']:<10}: {day_data['calories']:>4.0f} kcal {status}({cal_diff:+.0f})")
    
    def _export_meal_plan(self, weekly_plan, user_profile):
        """Export meal plan to file"""
        print("\n💾 EXPORT MEAL PLAN")
        
        filename = f"meal_plan_{user_profile.get('name', 'user').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("PERSONALIZED WEEKLY MEAL PLAN\n")
                f.write("=" * 50 + "\n\n")
                
                # User profile
                f.write("USER PROFILE:\n")
                f.write(f"Name: {user_profile.get('name', 'User')}\n")
                f.write(f"Age: {user_profile.get('age')} years\n")
                f.write(f"Weight: {user_profile.get('weight')} kg\n")
                f.write(f"Height: {user_profile.get('height')} cm\n")
                f.write(f"BMI: {user_profile.get('bmi', 0):.1f}\n")
                f.write(f"Health Goal: {user_profile.get('health_goal', '').replace('_', ' ').title()}\n")
                f.write(f"Target Daily Calories: {user_profile.get('target_calories', 0):.0f} kcal\n\n")
                
                # Weekly plan
                for day, daily_plan in weekly_plan.items():
                    f.write(f"{day.upper()}\n")
                    f.write("-" * 30 + "\n")
                    
                    for meal_type, meal_info in daily_plan.items():
                        time = meal_info.get('time', '')
                        dish = meal_info.get('dish_name', '')
                        calories = meal_info.get('calories', 0)
                        protein = meal_info.get('protein', 0)
                        
                        meal_display = meal_type.replace('_', ' ').title()
                        f.write(f"{time} - {meal_display}: {dish} ({calories:.0f} kcal, {protein:.1f}g protein)\n")
                    
                    # Daily total
                    daily_calories = sum(meal.get('calories', 0) for meal in daily_plan.values())
                    f.write(f"Daily Total: {daily_calories:.0f} kcal\n\n")
            
            print(f"✅ Meal plan exported to: {filename}")
            
        except Exception as e:
            print(f"❌ Error exporting file: {e}")
    
    def _suggest_recipes(self, user_profile):
        """Suggest detailed recipes based on user preferences"""
        print("\n👨‍🍳 RECIPE SUGGESTIONS")
        print("-" * 40)
        
        food_type = user_profile.get('food_type', 'Non-Vegetarian')
        regional_prefs = user_profile.get('regional_preferences', ['Pan Indian'])
        health_goal = user_profile.get('health_goal', 'maintenance')
        
        # Filter recipes based on preferences
        suitable_foods = self.food_df.copy()
        
        if food_type in ['Vegetarian', 'Vegan']:
            suitable_foods = suitable_foods[suitable_foods['veg_nonveg'] == 'Vegetarian']
        
        if 'Pan Indian' not in regional_prefs:
            suitable_foods = suitable_foods[suitable_foods['region'].isin(regional_prefs)]
        
        # Select random recipes
        if len(suitable_foods) > 0:
            sample_recipes = suitable_foods.sample(min(5, len(suitable_foods)))
            
            for i, (_, recipe) in enumerate(sample_recipes.iterrows(), 1):
                print(f"\n{i}. {recipe['dish_name']}")
                print(f"   Region: {recipe.get('region', 'Unknown')}")
                print(f"   Calories: {recipe.get('calories_(kcal)', 0):.0f} kcal")
                print(f"   Protein: {recipe.get('protein_(g)', 0):.1f}g")
                print(f"   Type: {recipe.get('veg_nonveg', 'Unknown')}")
                
                # Basic recipe suggestions based on dish name
                dish_name = recipe['dish_name'].lower()
                if 'dal' in dish_name:
                    print("   Basic Recipe: Boil lentils with turmeric, add tempering of cumin, garlic, onions")
                elif 'rice' in dish_name:
                    print("   Basic Recipe: Cook rice with whole spices, vegetables, and protein of choice")
                elif 'roti' in dish_name or 'paratha' in dish_name:
                    print("   Basic Recipe: Mix wheat flour with water, roll and cook on tawa with minimal oil")
                elif 'curry' in dish_name:
                    print("   Basic Recipe: Sauté onions, tomatoes, spices; add main ingredient and simmer")
                else:
                    print("   Basic Recipe: Traditional Indian preparation with aromatic spices")
        else:
            print("No suitable recipes found for your preferences.")
    
    def _show_alternatives(self, weekly_plan, user_profile):
        """Show alternative meal options for any day"""
        print("\n🔄 ALTERNATIVE MEAL OPTIONS")
        
        print("Available days:", ", ".join(weekly_plan.keys()))
        day = input("Enter day to see alternatives: ").strip().title()
        
        if day not in weekly_plan:
            print("Invalid day selected.")
            return
        
        print(f"\nAlternative meals for {day}:")
        
        for meal_type, current_meal in weekly_plan[day].items():
            current_calories = current_meal.get('calories', 300)
            
            # Find alternatives with similar calories
            alternatives = self.food_df[
                (self.food_df['calories_(kcal)'] >= current_calories * 0.7) &
                (self.food_df['calories_(kcal)'] <= current_calories * 1.3)
            ]
            
            # Apply user preferences
            food_type = user_profile.get('food_type', 'Non-Vegetarian')
            if food_type in ['Vegetarian', 'Vegan']:
                alternatives = alternatives[alternatives['veg_nonveg'] == 'Vegetarian']
            
            # Remove current meal from alternatives
            alternatives = alternatives[alternatives['dish_name'] != current_meal['dish_name']]
            
            if len(alternatives) >= 3:
                sample_alternatives = alternatives.sample(3)
                
                meal_display = meal_type.replace('_', ' ').title()
                print(f"\n{meal_display} (Current: {current_meal['dish_name']}):")
                
                for i, (_, alt) in enumerate(sample_alternatives.iterrows(), 1):
                    print(f"  {i}. {alt['dish_name']} ({alt['calories_(kcal)']:.0f} kcal, {alt['protein_(g)']:.1f}g protein)")
            else:
                meal_display = meal_type.replace('_', ' ').title()
                print(f"\n{meal_display}: Limited alternatives available")

class UserProfiler:
    """Calculate BMI, BMR, TDEE and other health metrics"""
    
    def calculate_bmi(self, weight, height):
        """Calculate BMI"""
        height_m = height / 100  # Convert cm to meters
        return weight / (height_m ** 2)
    
    def get_bmi_category(self, bmi):
        """Get BMI category"""
        if bmi < 18.5:
            return "underweight"
        elif 18.5 <= bmi < 25:
            return "normal"
        elif 25 <= bmi < 30:
            return "overweight"
        else:
            return "obese"
    
    def calculate_bmr(self, age, gender, weight, height):
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        if gender.lower() == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        return bmr
    
    def calculate_tdee(self, bmr, activity_level):
        """Calculate Total Daily Energy Expenditure"""
        activity_multipliers = {
            'sedentary': 1.2,
            'lightly_active': 1.375,
            'moderately_active': 1.55,
            'very_active': 1.725,
            'extremely_active': 1.9
        }
        
        multiplier = activity_multipliers.get(activity_level, 1.2)
        return bmr * multiplier
    
    def adjust_calories_for_goal(self, tdee, health_goal):
        """Adjust calories based on health goal"""
        if health_goal == 'weight_loss':
            return tdee - 500  # 500 calorie deficit for ~1 pound/week loss
        elif health_goal == 'weight_gain':
            return tdee + 300  # 300 calorie surplus for gradual gain
        elif health_goal == 'muscle_gain':
            return tdee + 200  # Moderate surplus for lean gains
        else:
            return tdee  # Maintenance

# Main execution function
def main():
    """Main function to run the complete system"""
    # try:
        # Initialize the system
    system = EnhancedFoodRecommendationSystem()
    system.initialize_system()
    system.run_complete_system()
        # Run the complete system
        # user_profile, weekly_plan = system.run_complete_system()
        
    print("\n🎉 Thank you for using the Indian Food Nutrition System!")
    print("Stay healthy and enjoy your personalized meal plan!")
        
    # except KeyboardInterrupt:
    #     print("\n\nExiting system...")
    # except Exception as e:
    #     print(f"\n❌ An error occurred: {e}")
    #     print("Please restart the system and try again.")

if __name__ == "__main__":
    main()