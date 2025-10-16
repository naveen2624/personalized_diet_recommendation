import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# ================= CONFIG =================
CSV_PATH = r"C:\Users\monis\Downloads\archive\Indian_Food_Nutrition_Processed.csv"
OUTPUT_JSON = "personalized_plan_output.json"
# =========================================

# ================= LOAD DATA =================
df = pd.read_csv(CSV_PATH)

# Map nutrition columns
col_map = {
    "calories": None,
    "carbs": None,
    "protein": None,
    "fat": None,
    "fiber": None
}

for c in df.columns:
    cname = c.lower()
    if "calories" in cname or "(kcal)" in cname:
        col_map["calories"] = c
    elif "carbo" in cname:
        col_map["carbs"] = c
    elif "prot" in cname:
        col_map["protein"] = c
    elif "fat" in cname or "fats" in cname:
        col_map["fat"] = c
    elif "fibre" in cname or "fiber" in cname:
        col_map["fiber"] = c

for key, col in col_map.items():
    if col in df.columns:
        df[key] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    else:
        df[key] = 0

df = df.dropna(subset=[col_map["calories"]]).reset_index(drop=True)

# Detect food name column
if "Item" in df.columns:
    food_name_col = "Item"
elif "Food" in df.columns:
    food_name_col = "Food"
else:
    food_name_col = df.columns[0]

# ================= HELPER FUNCTIONS =================
def calculate_tdee(user):
    if user["gender"] == "male":
        bmr = 10 * user["weight_kg"] + 6.25 * user["height_cm"] - 5 * user["age"] + 5
    else:
        bmr = 10 * user["weight_kg"] + 6.25 * user["height_cm"] - 5 * user["age"] - 161
    activity_factors = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725
    }
    return bmr * activity_factors.get(user["activity_level"], 1.55)

def calorie_goal(tdee, goal):
    if goal == "lose_weight":
        return max(tdee - 500, 1200)
    elif goal == "gain_muscle":
        return tdee + 300
    else:
        return tdee

def macro_split(goal):
    if goal == "lose_weight":
        return {"protein": 0.3, "fat": 0.3, "carbs": 0.4}
    elif goal == "gain_muscle":
        return {"protein": 0.25, "fat": 0.25, "carbs": 0.5}
    else:
        return {"protein": 0.2, "fat": 0.3, "carbs": 0.5}

def recommend_plan(df, user):
    tdee = calculate_tdee(user)
    target_cal = calorie_goal(tdee, user["goal"])
    macros = macro_split(user["goal"])

    # Compute macro ratios
    df["macro_carb_ratio"] = (df["carbs"]*4 / df["calories"]).replace([np.inf,-np.inf],0).fillna(0)
    df["macro_protein_ratio"] = (df["protein"]*4 / df["calories"]).replace([np.inf,-np.inf],0).fillna(0)
    df["macro_fat_ratio"] = (df["fat"]*9 / df["calories"]).replace([np.inf,-np.inf],0).fillna(0)

    X = df[["calories","macro_carb_ratio","macro_protein_ratio","macro_fat_ratio"]]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    nbrs = NearestNeighbors(n_neighbors=3).fit(X_scaled)

    meal_ratios = {"Breakfast":0.25,"Lunch":0.35,"Dinner":0.3,"Snacks":0.1}
    plan = {}

    for meal, ratio in meal_ratios.items():
        meal_cal = target_cal * ratio
        ideal_vec = pd.DataFrame([{
            "calories": meal_cal,
            "macro_carb_ratio": macros["carbs"],
            "macro_protein_ratio": macros["protein"],
            "macro_fat_ratio": macros["fat"]
        }])
        ideal_vec_scaled = scaler.transform(ideal_vec)
        distances, indices = nbrs.kneighbors(ideal_vec_scaled)
        selected_foods = df.iloc[indices[0]][food_name_col].tolist()
        selected_nutrients = df.iloc[indices[0]][["calories","carbs","protein","fat"]].to_dict(orient="records")

        plan[meal] = {
            "target_calories": round(meal_cal,2),
            "recommended_dishes": [
                {"food": f, "nutrition": n}
                for f,n in zip(selected_foods, selected_nutrients)
            ]
        }

    return {"user_info": user, "target_daily_calories": round(target_cal,2), "plan": plan}

# ================= GUI =================
def generate_plan():
    try:
        user = {
            "age": int(age_entry.get()),
            "gender": gender_var.get(),
            "height_cm": float(height_entry.get()),
            "weight_kg": float(weight_entry.get()),
            "activity_level": activity_var.get(),
            "goal": goal_var.get()
        }
    except Exception as e:
        messagebox.showerror("Input Error", "Please enter valid inputs.")
        return

    result = recommend_plan(df, user)
    with open(OUTPUT_JSON,"w") as f:
        json.dump(result,f,indent=4)

    # Build human-readable output
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"🎯 Personalized Diet Plan for {user['gender'].capitalize()} ({user['age']} yrs)\n")
    output_text.insert(tk.END, f"Target Daily Calories: {result['target_daily_calories']} kcal\n")
    output_text.insert(tk.END, "-"*50 + "\n\n")

    for meal, info in result["plan"].items():
        output_text.insert(tk.END, f"🍽 {meal} (Target: {info['target_calories']} kcal)\n")
        for dish in info["recommended_dishes"]:
            n = dish["nutrition"]
            output_text.insert(tk.END, f"   • {dish['food']} — {n['calories']} kcal | Protein: {n['protein']}g | Carbs: {n['carbs']}g | Fat: {n['fat']}g\n")
        output_text.insert(tk.END, "\n")
    output_text.insert(tk.END, "✅ Enjoy your meals! Stay healthy! 🍎\n")

# ================= TKINTER WINDOW =================
root = tk.Tk()
root.title("🍽 Personalized Diet Recommender 🍽")
root.geometry("700x700")
root.configure(bg="#f0f8ff")

# Create a frame for inputs
frame_inputs = tk.Frame(root, bg="#f0f8ff", padx=20, pady=20)
frame_inputs.pack(fill=tk.X)

labels = ["Age:", "Gender:", "Height (cm):", "Weight (kg):", "Activity Level:", "Goal:"]
for i, text in enumerate(labels):
    tk.Label(frame_inputs, text=text, anchor='w', width=15, bg="#f0f8ff", font=("Arial",10,"bold")).grid(row=i,column=0,pady=5)
    
age_entry = tk.Entry(frame_inputs, width=20)
age_entry.grid(row=0,column=1, pady=5)
gender_var = tk.StringVar(value="male")
gender_menu = ttk.Combobox(frame_inputs, textvariable=gender_var, values=["male","female"], state="readonly", width=18)
gender_menu.grid(row=1,column=1, pady=5)

height_entry = tk.Entry(frame_inputs, width=20)
height_entry.grid(row=2,column=1, pady=5)
weight_entry = tk.Entry(frame_inputs, width=20)
weight_entry.grid(row=3,column=1, pady=5)

activity_var = tk.StringVar(value="moderate")
activity_menu = ttk.Combobox(frame_inputs, textvariable=activity_var, values=["sedentary","light","moderate","active"], state="readonly", width=18)
activity_menu.grid(row=4,column=1, pady=5)

goal_var = tk.StringVar(value="lose_weight")
goal_menu = ttk.Combobox(frame_inputs, textvariable=goal_var, values=["lose_weight","gain_muscle","maintain"], state="readonly", width=18)
goal_menu.grid(row=5,column=1, pady=5)

generate_btn = tk.Button(frame_inputs, text="Generate Plan", command=generate_plan, bg="#4caf50", fg="white", font=("Arial",11,"bold"))
generate_btn.grid(row=6,column=0,columnspan=2, pady=15)

# Scrolled text for output
output_text = scrolledtext.ScrolledText(root, width=80, height=25, font=("Arial",10))
output_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

# Run the GUI
root.mainloop()
