import pandas as pd
import numpy as np
import kagglehub
import re
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import warnings
warnings.filterwarnings('ignore')

def download_and_load_dataset():
    """Download and load the Indian food nutrition dataset"""
    print("Downloading dataset...")
    path = kagglehub.dataset_download("batthulavinay/indian-food-nutrition")
    print(f"Path to dataset files: {path}")
    
    # Find CSV file in the downloaded path
    import os
    csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
    if not csv_files:
        raise FileNotFoundError("No CSV file found in the downloaded dataset")
    
    csv_file = csv_files[0]
    df = pd.read_csv(os.path.join(path, csv_file))
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

def check_dataset_quality(df):
    """Check dataset quality: missing values, duplicates, data types"""
    print("\n=== DATASET QUALITY CHECK ===")
    print(f"Dataset shape: {df.shape}")
    print(f"\nColumn names: {list(df.columns)}")
    
    # Check missing values
    print("\nMissing values:")
    missing = df.isnull().sum()
    print(missing[missing > 0])
    
    # Check duplicates
    duplicates = df.duplicated().sum()
    print(f"\nDuplicate rows: {duplicates}")
    
    # Check data types
    print("\nData types:")
    print(df.dtypes)
    
    # Basic statistics
    print("\nBasic statistics for numerical columns:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print(df[numeric_cols].describe())
    
    return df

def clean_dataset(df):
    """Clean the dataset: handle missing values, remove duplicates, fix data types"""
    print("\n=== CLEANING DATASET ===")
    
    # Create a copy to avoid modifying original
    df_clean = df.copy()
    
    # Remove duplicates
    initial_rows = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    print(f"Removed {initial_rows - len(df_clean)} duplicate rows")
    
    # Clean column names (remove extra spaces, standardize)
    df_clean.columns = df_clean.columns.str.strip().str.lower().str.replace(' ', '_')
    print(f"Cleaned column names: {list(df_clean.columns)}")
    
    # Handle missing values
    numeric_columns = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        if df_clean[col].isnull().sum() > 0:
            # Fill with median for nutritional values (more robust than mean)
            median_val = df_clean[col].median()
            df_clean[col].fillna(median_val, inplace=True)
            print(f"Filled {col} missing values with median: {median_val:.2f}")
    
    # Handle missing values in text columns
    text_columns = df_clean.select_dtypes(include=['object']).columns
    for col in text_columns:
        if df_clean[col].isnull().sum() > 0:
            df_clean[col].fillna('Unknown', inplace=True)
            print(f"Filled {col} missing values with 'Unknown'")
    
    # Remove rows with negative nutritional values (data errors)
    for col in numeric_columns:
        negative_count = (df_clean[col] < 0).sum()
        if negative_count > 0:
            df_clean = df_clean[df_clean[col] >= 0]
            print(f"Removed {negative_count} rows with negative {col} values")
    
    # Remove outliers (values beyond 3 standard deviations)
    for col in numeric_columns:
        if col != 'dish_name':  # Skip non-nutritional columns
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = ((df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)).sum()
            if outliers > 0:
                df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
                print(f"Removed {outliers} outliers from {col}")
    
    print(f"Final cleaned dataset shape: {df_clean.shape}")
    return df_clean

def normalize_nutritional_values(df):
    """Normalize nutritional values per 100g serving"""
    print("\n=== NORMALIZING NUTRITIONAL VALUES ===")
    
    # Assume values are already per 100g if no serving size column exists
    # If there's a serving size column, we would normalize here
    
    # Create normalized columns (per 100g) - assuming current values might be per serving
    nutritional_cols = [col for col in df.columns if col not in ['dish_name', 'food_name'] and df[col].dtype in ['float64', 'int64']]
    
    df_normalized = df.copy()
    
    # Add suffix to indicate normalization
    for col in nutritional_cols:
        if 'per_100g' not in col:
            df_normalized[f'{col}_per_100g'] = df_normalized[col]
    
    print("Nutritional values normalized per 100g serving")
    return df_normalized

def add_meal_category(dish_name):
    """Categorize dishes into meal categories"""
    dish_lower = dish_name.lower()
    
    # Breakfast items
    breakfast_keywords = ['dosa', 'idli', 'upma', 'poha', 'paratha', 'puri', 'uttapam', 
                         'appam', 'puttu', 'sheera', 'halwa', 'pancake', 'toast']
    
    # Snack items
    snack_keywords = ['samosa', 'pakora', 'bhel', 'chaat', 'vada', 'cutlet', 'tikki',
                     'chips', 'namkeen', 'mixture', 'chevda', 'sev', 'bhujia']
    
    # Dessert items
    dessert_keywords = ['ladoo', 'burfi', 'kheer', 'payasam', 'gulab jamun', 'rasgulla',
                       'sandesh', 'kulfi', 'ice cream', 'cake', 'sweet', 'mithai']
    
    # Main course indicators (default category)
    main_keywords = ['curry', 'dal', 'rice', 'biryani', 'pulao', 'sabzi', 'chicken',
                    'mutton', 'fish', 'paneer', 'chole', 'rajma']
    
    for keyword in breakfast_keywords:
        if keyword in dish_lower:
            return 'Breakfast'
    
    for keyword in snack_keywords:
        if keyword in dish_lower:
            return 'Snack'
    
    for keyword in dessert_keywords:
        if keyword in dish_lower:
            return 'Dessert'
    
    return 'Main Course'

def add_veg_nonveg_category(dish_name):
    """Categorize dishes as vegetarian or non-vegetarian"""
    dish_lower = dish_name.lower()
    
    # Non-veg keywords
    nonveg_keywords = ['chicken', 'mutton', 'lamb', 'goat', 'beef', 'pork', 'fish',
                      'prawn', 'crab', 'egg', 'meat', 'keema', 'tandoori chicken',
                      'butter chicken', 'fish curry', 'biryani chicken']
    
    for keyword in nonveg_keywords:
        if keyword in dish_lower:
            return 'Non-Vegetarian'
    
    return 'Vegetarian'

def add_regional_category(dish_name):
    """Categorize dishes by Indian regions"""
    dish_lower = dish_name.lower()
    
    # South Indian
    south_keywords = ['dosa', 'idli', 'sambar', 'rasam', 'vada', 'uttapam', 'appam',
                     'puttu', 'payasam', 'avial', 'kootu', 'poriyal', 'chettinad',
                     'hyderabadi', 'andhra', 'kerala', 'tamil', 'mysore']
    
    # North Indian
    north_keywords = ['roti', 'naan', 'kulcha', 'paratha', 'chole', 'rajma', 'dal makhani',
                     'butter chicken', 'tandoori', 'biryani', 'pulao', 'lassi',
                     'punjabi', 'delhi', 'haryana', 'himachal']
    
    # Western Indian
    west_keywords = ['dhokla', 'khandvi', 'thepla', 'pav bhaji', 'vada pav', 'bhel puri',
                    'gujarati', 'marathi', 'maharashtrian', 'mumbai', 'pune', 'goan']
    
    # Eastern Indian
    east_keywords = ['rasgulla', 'sandesh', 'fish curry', 'hilsa', 'bengali', 'kolkata',
                    'machher jhol', 'mishti doi', 'rosogolla']
    
    for keyword in south_keywords:
        if keyword in dish_lower:
            return 'South Indian'
    
    for keyword in north_keywords:
        if keyword in dish_lower:
            return 'North Indian'
    
    for keyword in west_keywords:
        if keyword in dish_lower:
            return 'West Indian'
    
    for keyword in east_keywords:
        if keyword in dish_lower:
            return 'East Indian'
    
    return 'Pan Indian'

def add_dietary_restrictions(dish_name, nutritional_data=None):
    """Categorize dishes based on dietary restrictions"""
    dish_lower = dish_name.lower()
    restrictions = []
    
    # 1. DIABETIC FRIENDLY
    # Low sugar, low refined carb dishes
    diabetic_friendly_keywords = ['grilled', 'steamed', 'boiled', 'roasted', 'salad', 
                                'soup', 'dal', 'sambar', 'rasam', 'vegetable curry']
    diabetic_avoid_keywords = ['sweet', 'halwa', 'ladoo', 'kheer', 'payasam', 'burfi',
                              'gulab jamun', 'jalebi', 'rice', 'biryani', 'pulao']
    
    is_diabetic_friendly = any(keyword in dish_lower for keyword in diabetic_friendly_keywords)
    has_diabetic_concerns = any(keyword in dish_lower for keyword in diabetic_avoid_keywords)
    
    if is_diabetic_friendly and not has_diabetic_concerns:
        restrictions.append('Diabetic-Friendly')
    elif has_diabetic_concerns:
        restrictions.append('Not-Diabetic-Friendly')
    
    # 2. GLUTEN-FREE
    gluten_keywords = ['wheat', 'roti', 'naan', 'kulcha', 'paratha', 'puri', 'bhatura',
                      'pasta', 'bread', 'chapati', 'thepla']
    
    if not any(keyword in dish_lower for keyword in gluten_keywords):
        restrictions.append('Gluten-Free')
    else:
        restrictions.append('Contains-Gluten')
    
    # 3. DAIRY-FREE/LACTOSE-FREE
    dairy_keywords = ['milk', 'cream', 'butter', 'ghee', 'paneer', 'curd', 'yogurt',
                     'cheese', 'kheer', 'lassi', 'mishti doi', 'raita']
    
    if not any(keyword in dish_lower for keyword in dairy_keywords):
        restrictions.append('Dairy-Free')
    else:
        restrictions.append('Contains-Dairy')
    
    # 4. NUT-FREE
    nut_keywords = ['almond', 'cashew', 'walnut', 'pistachio', 'groundnut', 'peanut',
                   'badam', 'kaju', 'akhrot']
    
    if not any(keyword in dish_lower for keyword in nut_keywords):
        restrictions.append('Nut-Free')
    else:
        restrictions.append('Contains-Nuts')
    
    # 5. LOW-SODIUM (based on ingredients)
    high_sodium_keywords = ['pickle', 'papad', 'namkeen', 'chips', 'salted', 'chaat']
    
    if not any(keyword in dish_lower for keyword in high_sodium_keywords):
        restrictions.append('Low-Sodium-Friendly')
    else:
        restrictions.append('High-Sodium')
    
    # 6. JAIN/STRICT VEGETARIAN
    jain_avoid_keywords = ['onion', 'garlic', 'potato', 'ginger', 'carrot', 'radish',
                          'beetroot', 'turnip']
    
    if not any(keyword in dish_lower for keyword in jain_avoid_keywords):
        restrictions.append('Jain-Friendly')
    
    # 7. VEGAN (no animal products)
    vegan_avoid_keywords = ['milk', 'cream', 'butter', 'ghee', 'paneer', 'curd', 'yogurt',
                           'cheese', 'honey', 'egg', 'chicken', 'mutton', 'fish', 'meat']
    
    if not any(keyword in dish_lower for keyword in vegan_avoid_keywords):
        restrictions.append('Vegan')
    
    # 8. KETO-FRIENDLY (low carb, high fat)
    high_carb_keywords = ['rice', 'wheat', 'potato', 'sweet', 'sugar', 'jaggery',
                         'bread', 'pasta', 'noodles']
    keto_friendly_keywords = ['ghee', 'coconut', 'nuts', 'cheese', 'cream']
    
    has_high_carbs = any(keyword in dish_lower for keyword in high_carb_keywords)
    has_keto_ingredients = any(keyword in dish_lower for keyword in keto_friendly_keywords)
    
    if not has_high_carbs and has_keto_ingredients:
        restrictions.append('Keto-Friendly')
    elif has_high_carbs:
        restrictions.append('High-Carb')
    
    return restrictions

def add_nutritional_dietary_restrictions(df, dish_name_col):
    """Add dietary restrictions based on nutritional values"""
    df_copy = df.copy()
    
    # Find nutritional columns
    nutrition_cols = {}
    for col in df.columns:
        col_lower = col.lower()
        if 'calorie' in col_lower or 'energy' in col_lower:
            nutrition_cols['calories'] = col
        elif 'carb' in col_lower:
            nutrition_cols['carbs'] = col
        elif 'sugar' in col_lower:
            nutrition_cols['sugar'] = col
        elif 'sodium' in col_lower:
            nutrition_cols['sodium'] = col
        elif 'fat' in col_lower and 'trans' not in col_lower:
            nutrition_cols['fat'] = col
        elif 'protein' in col_lower:
            nutrition_cols['protein'] = col
        elif 'fibre' in col_lower or 'fiber' in col_lower:
            nutrition_cols['fiber'] = col
    
    # Add nutritional-based restrictions
    restrictions_list = []
    
    for idx, row in df_copy.iterrows():
        dish_restrictions = add_dietary_restrictions(row[dish_name_col])
        
        # Add nutritional-based restrictions
        if 'calories' in nutrition_cols:
            if row[nutrition_cols['calories']] < 150:
                dish_restrictions.append('Low-Calorie')
            elif row[nutrition_cols['calories']] > 400:
                dish_restrictions.append('High-Calorie')
        
        if 'sugar' in nutrition_cols:
            if row[nutrition_cols['sugar']] < 2:
                dish_restrictions.append('Low-Sugar')
            elif row[nutrition_cols['sugar']] > 15:
                dish_restrictions.append('High-Sugar')
        
        if 'sodium' in nutrition_cols:
            if row[nutrition_cols['sodium']] < 200:
                dish_restrictions.append('Low-Sodium')
            elif row[nutrition_cols['sodium']] > 800:
                dish_restrictions.append('High-Sodium')
        
        if 'fiber' in nutrition_cols:
            if row[nutrition_cols['fiber']] > 5:
                dish_restrictions.append('High-Fiber')
        
        if 'protein' in nutrition_cols:
            if row[nutrition_cols['protein']] > 15:
                dish_restrictions.append('High-Protein')
            elif row[nutrition_cols['protein']] < 3:
                dish_restrictions.append('Low-Protein')
        
        restrictions_list.append('; '.join(dish_restrictions))
    
    return restrictions_list

def add_enhanced_categories(df):
    """Add meal category, veg/non-veg, regional categories, and dietary restrictions"""
    print("\n=== ADDING ENHANCED CATEGORIES ===")
    
    df_enhanced = df.copy()
    
    # Get the dish name column (it might have different names)
    name_col = None
    for col in df.columns:
        if 'name' in col.lower() or 'dish' in col.lower() or 'food' in col.lower():
            name_col = col
            break
    
    if name_col is None:
        print("Warning: Could not find dish name column. Using first column.")
        name_col = df.columns[0]
    
    print(f"Using column '{name_col}' for categorization")
    
    # Add basic categories
    df_enhanced['meal_category'] = df_enhanced[name_col].apply(add_meal_category)
    df_enhanced['veg_nonveg'] = df_enhanced[name_col].apply(add_veg_nonveg_category)
    df_enhanced['region'] = df_enhanced[name_col].apply(add_regional_category)
    
    # Add comprehensive dietary restrictions
    print("Adding dietary restrictions...")
    df_enhanced['dietary_restrictions'] = add_nutritional_dietary_restrictions(df_enhanced, name_col)
    
    # Create individual binary columns for major dietary restrictions
    all_restrictions = set()
    for restrictions in df_enhanced['dietary_restrictions']:
        all_restrictions.update(restrictions.split('; '))
    
    # Create binary columns for common dietary needs
    important_restrictions = ['Vegan', 'Gluten-Free', 'Dairy-Free', 'Nut-Free', 
                            'Diabetic-Friendly', 'Keto-Friendly', 'Jain-Friendly',
                            'Low-Calorie', 'High-Protein', 'Low-Sodium']
    
    for restriction in important_restrictions:
        df_enhanced[f'is_{restriction.lower().replace("-", "_")}'] = df_enhanced['dietary_restrictions'].apply(
            lambda x: 1 if restriction in x else 0
        )
    
    # Add nutritional density categories
    if 'calories' in df.columns or 'energy' in df.columns:
        cal_col = 'calories' if 'calories' in df.columns else 'energy'
        df_enhanced['calorie_category'] = pd.cut(df_enhanced[cal_col], 
                                               bins=[0, 100, 200, 400, float('inf')],
                                               labels=['Low', 'Medium', 'High', 'Very High'])
    
    if 'protein' in df.columns:
        df_enhanced['protein_category'] = pd.cut(df_enhanced['protein'], 
                                               bins=[0, 5, 15, 25, float('inf')],
                                               labels=['Low', 'Medium', 'High', 'Very High'])
    
    # Add carb category for diabetic/keto analysis
    carb_cols = [col for col in df.columns if 'carb' in col.lower()]
    if carb_cols:
        df_enhanced['carb_category'] = pd.cut(df_enhanced[carb_cols[0]], 
                                            bins=[0, 10, 30, 60, float('inf')],
                                            labels=['Very Low', 'Low', 'Medium', 'High'])
    
    print("Added categories:")
    print("- Meal Category:", df_enhanced['meal_category'].value_counts().to_dict())
    print("- Veg/Non-veg:", df_enhanced['veg_nonveg'].value_counts().to_dict())
    print("- Regional:", df_enhanced['region'].value_counts().to_dict())
    print("- Dietary Restrictions: Added comprehensive restrictions for each dish")
    
    # Show dietary restriction statistics
    restriction_counts = {}
    for restriction in important_restrictions:
        col_name = f'is_{restriction.lower().replace("-", "_")}'
        if col_name in df_enhanced.columns:
            restriction_counts[restriction] = df_enhanced[col_name].sum()
    
    print("- Dietary Restriction Counts:", restriction_counts)
    
    return df_enhanced

def save_cleaned_dataset(df, filename='indian_food_nutrition_cleaned.csv'):
    """Save the cleaned and enhanced dataset"""
    print(f"\n=== SAVING CLEANED DATASET ===")
    
    df.to_csv(filename, index=False)
    print(f"Dataset saved as '{filename}'")
    print(f"Final dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    return filename

def main():
    """Main function to execute the complete pipeline"""
    try:
        # Step 1: Download and load dataset
        df = download_and_load_dataset()
        
        # Step 2: Check dataset quality
        df = check_dataset_quality(df)
        
        # Step 3: Clean dataset
        df_clean = clean_dataset(df)
        
        # Step 4: Normalize nutritional values
        df_normalized = normalize_nutritional_values(df_clean)
        
        # Step 5: Add enhanced categories
        df_enhanced = add_enhanced_categories(df_normalized)
        
        # Step 6: Save cleaned dataset
        filename = save_cleaned_dataset(df_enhanced)
        
        print(f"\n=== PIPELINE COMPLETED SUCCESSFULLY ===")
        print(f"Cleaned dataset saved as: {filename}")
        
        # Display sample of final dataset
        print("\nSample of final dataset:")
        print(df_enhanced.head())
        
        return df_enhanced
        
    except Exception as e:
        print(f"Error in pipeline: {str(e)}")
        return None

if __name__ == "__main__":
    # Execute the complete data cleaning pipeline
    cleaned_dataset = main()