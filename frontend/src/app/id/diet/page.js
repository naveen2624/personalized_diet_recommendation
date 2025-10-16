"use client";
import React, { useState, useRef } from "react";
import {
  Apple,
  Plus,
  Edit2,
  Download,
  Calendar,
  TrendingDown,
  TrendingUp,
  Target,
  X,
  Check,
  ChevronDown,
  Trash2,
  Utensils,
} from "lucide-react";

const NutriAI = () => {
  const [step, setStep] = useState("profile");
  const [profile, setProfile] = useState({
    weight: "",
    height: "",
    age: "",
    gender: "male",
    dietPreference: "vegetarian",
    restrictions: [],
    goal: "maintain",
    preferredMeals: [],
  });
  const [dietPlan, setDietPlan] = useState(null);
  const [selectedDay, setSelectedDay] = useState(0);
  const [editingMeal, setEditingMeal] = useState(null);
  const [viewMode, setViewMode] = useState("week");
  const [showAddMeal, setShowAddMeal] = useState(false);
  const [newMealData, setNewMealData] = useState({ meal: "", days: 1 });
  const chartRef = useRef(null);

  const mealTimes = [
    "Breakfast",
    "Morning Snack",
    "Lunch",
    "Evening Snack",
    "Dinner",
    "Post Dinner",
  ];

  const dietPreferences = [
    "vegetarian",
    "vegan",
    "non-vegetarian",
    "eggetarian",
  ];
  const goals = [
    { value: "loss", label: "Weight Loss", icon: TrendingDown },
    { value: "gain", label: "Weight Gain", icon: TrendingUp },
    { value: "maintain", label: "Maintain", icon: Target },
  ];

  const restrictions = [
    "Gluten-Free",
    "Dairy-Free",
    "Nut-Free",
    "Soy-Free",
    "Low-Carb",
  ];

  const sampleMeals = {
    vegetarian: {
      Breakfast: [
        {
          name: "Oatmeal with Berries",
          cal: 320,
          protein: 12,
          carbs: 58,
          fat: 6,
        },
        { name: "Avocado Toast", cal: 280, protein: 8, carbs: 32, fat: 14 },
        {
          name: "Greek Yogurt Parfait",
          cal: 250,
          protein: 15,
          carbs: 35,
          fat: 5,
        },
      ],
      "Morning Snack": [
        {
          name: "Apple with Almond Butter",
          cal: 180,
          protein: 4,
          carbs: 22,
          fat: 9,
        },
        { name: "Mixed Nuts", cal: 170, protein: 6, carbs: 8, fat: 14 },
      ],
      Lunch: [
        {
          name: "Quinoa Buddha Bowl",
          cal: 450,
          protein: 18,
          carbs: 62,
          fat: 14,
        },
        {
          name: "Paneer Tikka Wrap",
          cal: 420,
          protein: 22,
          carbs: 48,
          fat: 16,
        },
        {
          name: "Vegetable Stir Fry",
          cal: 380,
          protein: 14,
          carbs: 52,
          fat: 12,
        },
      ],
      "Evening Snack": [
        {
          name: "Hummus with Carrots",
          cal: 150,
          protein: 5,
          carbs: 18,
          fat: 7,
        },
        { name: "Green Smoothie", cal: 200, protein: 8, carbs: 32, fat: 4 },
      ],
      Dinner: [
        {
          name: "Grilled Tofu with Veggies",
          cal: 400,
          protein: 25,
          carbs: 35,
          fat: 18,
        },
        {
          name: "Dal Tadka with Brown Rice",
          cal: 480,
          protein: 20,
          carbs: 68,
          fat: 12,
        },
        { name: "Mushroom Risotto", cal: 440, protein: 16, carbs: 58, fat: 16 },
      ],
      "Post Dinner": [
        { name: "Chamomile Tea", cal: 5, protein: 0, carbs: 1, fat: 0 },
        {
          name: "Dark Chocolate Square",
          cal: 60,
          protein: 1,
          carbs: 7,
          fat: 4,
        },
      ],
    },
  };

  const calculateBMI = () => {
    const heightM = profile.height / 100;
    const bmi = profile.weight / (heightM * heightM);
    return bmi.toFixed(1);
  };

  const generateDietPlan = () => {
    const days = viewMode === "week" ? 7 : viewMode === "day" ? 1 : 30;
    const plan = [];

    for (let i = 0; i < days; i++) {
      const dayPlan = {};
      mealTimes.forEach((mealTime) => {
        const meals = sampleMeals[profile.dietPreference]?.[mealTime] || [];
        dayPlan[mealTime] = meals[Math.floor(Math.random() * meals.length)];
      });
      plan.push(dayPlan);
    }

    // Add preferred meals
    profile.preferredMeals.forEach((pref) => {
      for (let i = 0; i < Math.min(pref.days, days); i++) {
        if (plan[i] && sampleMeals[profile.dietPreference]?.[pref.meal]) {
          const meals = sampleMeals[profile.dietPreference][pref.meal];
          plan[i][pref.meal] = meals[Math.floor(Math.random() * meals.length)];
        }
      }
    });

    setDietPlan(plan);
    setStep("plan");
  };

  const getDailyTotals = (day) => {
    if (!dietPlan || !dietPlan[day])
      return { cal: 0, protein: 0, carbs: 0, fat: 0 };

    return Object.values(dietPlan[day]).reduce(
      (acc, meal) => ({
        cal: acc.cal + (meal?.cal || 0),
        protein: acc.protein + (meal?.protein || 0),
        carbs: acc.carbs + (meal?.carbs || 0),
        fat: acc.fat + (meal?.fat || 0),
      }),
      { cal: 0, protein: 0, carbs: 0, fat: 0 }
    );
  };

  const replaceMeal = (dayIndex, mealTime, newMeal) => {
    const updatedPlan = [...dietPlan];
    updatedPlan[dayIndex][mealTime] = newMeal;
    setDietPlan(updatedPlan);
    setEditingMeal(null);
  };

  const downloadChart = () => {
    const dayLabel =
      viewMode === "week"
        ? [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
          ][selectedDay]
        : `Day ${selectedDay + 1}`;

    const totals = getDailyTotals(selectedDay);

    // Create text content for download
    let content = `NUTRI.AI - PERSONALIZED MEAL PLAN\n`;
    content += `${"=".repeat(50)}\n\n`;
    content += `Date: ${new Date().toLocaleDateString("en-US", {
      month: "long",
      day: "numeric",
      year: "numeric",
    })}\n`;
    content += `Day: ${dayLabel}\n\n`;

    content += `DAILY SUMMARY\n`;
    content += `${"-".repeat(50)}\n`;
    content += `Total Calories: ${totals.cal} cal\n`;
    content += `Protein: ${totals.protein}g\n`;
    content += `Carbohydrates: ${totals.carbs}g\n`;
    content += `Fat: ${totals.fat}g\n\n`;

    content += `MEAL PLAN\n`;
    content += `${"=".repeat(50)}\n\n`;

    mealTimes.forEach((mealTime) => {
      const meal = dietPlan[selectedDay][mealTime];
      content += `${mealTime.toUpperCase()}\n`;
      content += `${"-".repeat(50)}\n`;
      content += `Meal: ${meal?.name || "Not set"}\n`;
      content += `Calories: ${meal?.cal || 0} cal\n`;
      content += `Protein: ${meal?.protein || 0}g | Carbs: ${
        meal?.carbs || 0
      }g | Fat: ${meal?.fat || 0}g\n\n`;
    });

    content += `\n${"=".repeat(50)}\n`;
    content += `Generated by Nutri.ai - Your AI-Powered Nutrition Assistant\n`;

    // Create and download text file
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `nutri-ai-${dayLabel.toLowerCase().replace(" ", "-")}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const addPreferredMeal = () => {
    if (newMealData.meal && newMealData.days > 0) {
      setProfile({
        ...profile,
        preferredMeals: [...profile.preferredMeals, newMealData],
      });
      setNewMealData({ meal: "", days: 1 });
      setShowAddMeal(false);
    }
  };

  const removePreferredMeal = (index) => {
    setProfile({
      ...profile,
      preferredMeals: profile.preferredMeals.filter((_, i) => i !== index),
    });
  };

  if (step === "profile") {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-emerald-50 p-4">
        <div className="max-w-2xl mx-auto">
          {/* Header */}
          <div className="flex items-center justify-center gap-3 mb-8 pt-8">
            <div className="w-12 h-12 bg-gradient-to-br from-emerald-500 to-green-600 rounded-2xl flex items-center justify-center shadow-lg">
              <Apple className="w-7 h-7 text-white" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-emerald-600 to-green-600 bg-clip-text text-transparent">
              Nutri.ai
            </h1>
          </div>

          {/* Profile Form */}
          <div className="bg-white rounded-3xl p-6 shadow-xl border border-emerald-100">
            <h2 className="text-2xl font-semibold mb-6 text-emerald-700">
              Your Profile
            </h2>

            <div className="space-y-4">
              {/* Physical Stats */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm text-gray-700 font-medium mb-2">
                    Weight (kg)
                  </label>
                  <input
                    type="number"
                    value={profile.weight}
                    onChange={(e) =>
                      setProfile({ ...profile, weight: e.target.value })
                    }
                    className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                    placeholder="70"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-700 font-medium mb-2">
                    Height (cm)
                  </label>
                  <input
                    type="number"
                    value={profile.height}
                    onChange={(e) =>
                      setProfile({ ...profile, height: e.target.value })
                    }
                    className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                    placeholder="170"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm text-gray-700 font-medium mb-2">
                    Age
                  </label>
                  <input
                    type="number"
                    value={profile.age}
                    onChange={(e) =>
                      setProfile({ ...profile, age: e.target.value })
                    }
                    className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                    placeholder="25"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-700 font-medium mb-2">
                    Gender
                  </label>
                  <select
                    value={profile.gender}
                    onChange={(e) =>
                      setProfile({ ...profile, gender: e.target.value })
                    }
                    className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                  >
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>
              </div>

              {profile.weight && profile.height && (
                <div className="bg-gradient-to-br from-emerald-50 to-green-50 rounded-xl p-4 border border-emerald-200">
                  <div className="text-sm text-emerald-700 font-medium">
                    Your BMI
                  </div>
                  <div className="text-3xl font-bold text-emerald-600">
                    {calculateBMI()}
                  </div>
                </div>
              )}

              {/* Goal */}
              <div>
                <label className="block text-sm text-gray-700 font-medium mb-3">
                  Your Goal
                </label>
                <div className="grid grid-cols-3 gap-3">
                  {goals.map(({ value, label, icon: Icon }) => (
                    <button
                      key={value}
                      onClick={() => setProfile({ ...profile, goal: value })}
                      className={`p-4 rounded-xl border-2 transition-all ${
                        profile.goal === value
                          ? "bg-emerald-500 border-emerald-500 shadow-lg text-white"
                          : "bg-white border-gray-200 hover:border-emerald-300 text-gray-700"
                      }`}
                    >
                      <Icon
                        className={`w-6 h-6 mx-auto mb-2 ${
                          profile.goal === value
                            ? "text-white"
                            : "text-emerald-600"
                        }`}
                      />
                      <div className="text-xs text-center font-medium">
                        {label}
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Diet Preference */}
              <div>
                <label className="block text-sm text-gray-700 font-medium mb-2">
                  Diet Preference
                </label>
                <select
                  value={profile.dietPreference}
                  onChange={(e) =>
                    setProfile({ ...profile, dietPreference: e.target.value })
                  }
                  className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                >
                  {dietPreferences.map((pref) => (
                    <option key={pref} value={pref}>
                      {pref.charAt(0).toUpperCase() + pref.slice(1)}
                    </option>
                  ))}
                </select>
              </div>

              {/* Restrictions */}
              <div>
                <label className="block text-sm text-gray-700 font-medium mb-3">
                  Dietary Restrictions
                </label>
                <div className="flex flex-wrap gap-2">
                  {restrictions.map((restriction) => (
                    <button
                      key={restriction}
                      onClick={() => {
                        const isSelected =
                          profile.restrictions.includes(restriction);
                        setProfile({
                          ...profile,
                          restrictions: isSelected
                            ? profile.restrictions.filter(
                                (r) => r !== restriction
                              )
                            : [...profile.restrictions, restriction],
                        });
                      }}
                      className={`px-4 py-2 rounded-full text-sm transition-all font-medium ${
                        profile.restrictions.includes(restriction)
                          ? "bg-emerald-500 text-white shadow-md"
                          : "bg-gray-100 border border-gray-200 text-gray-700 hover:border-emerald-300"
                      }`}
                    >
                      {restriction}
                    </button>
                  ))}
                </div>
              </div>

              {/* Preferred Meals */}
              <div>
                <label className="block text-sm text-gray-700 font-medium mb-3">
                  Preferred Meals (Optional)
                </label>

                {profile.preferredMeals.length > 0 && (
                  <div className="space-y-2 mb-3">
                    {profile.preferredMeals.map((pref, idx) => (
                      <div
                        key={idx}
                        className="flex items-center justify-between bg-emerald-50 rounded-xl p-3 border border-emerald-100"
                      >
                        <div>
                          <div className="text-gray-900 font-medium">
                            {pref.meal}
                          </div>
                          <div className="text-xs text-emerald-600">
                            {pref.days} day{pref.days > 1 ? "s" : ""}
                          </div>
                        </div>
                        <button
                          onClick={() => removePreferredMeal(idx)}
                          className="p-2 hover:bg-red-50 rounded-lg transition-colors"
                        >
                          <Trash2 className="w-4 h-4 text-red-500" />
                        </button>
                      </div>
                    ))}
                  </div>
                )}

                {!showAddMeal ? (
                  <button
                    onClick={() => setShowAddMeal(true)}
                    className="w-full py-3 bg-gray-50 border border-dashed border-gray-300 rounded-xl text-emerald-600 hover:border-emerald-500 hover:bg-emerald-50 transition-colors flex items-center justify-center gap-2 font-medium"
                  >
                    <Plus className="w-4 h-4" />
                    Add Preferred Meal
                  </button>
                ) : (
                  <div className="bg-emerald-50 rounded-xl p-4 border border-emerald-200 space-y-3">
                    <select
                      value={newMealData.meal}
                      onChange={(e) =>
                        setNewMealData({ ...newMealData, meal: e.target.value })
                      }
                      className="w-full bg-white border border-gray-200 rounded-xl px-4 py-3 text-gray-900 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                    >
                      <option value="">Select meal time</option>
                      {mealTimes.map((meal) => (
                        <option key={meal} value={meal}>
                          {meal}
                        </option>
                      ))}
                    </select>
                    <input
                      type="number"
                      min="1"
                      value={newMealData.days}
                      onChange={(e) =>
                        setNewMealData({
                          ...newMealData,
                          days: parseInt(e.target.value) || 1,
                        })
                      }
                      className="w-full bg-white border border-gray-200 rounded-xl px-4 py-3 text-gray-900 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                      placeholder="Number of days"
                    />
                    <div className="flex gap-2">
                      <button
                        onClick={addPreferredMeal}
                        className="flex-1 py-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded-xl transition-colors flex items-center justify-center gap-2 font-medium"
                      >
                        <Check className="w-4 h-4" />
                        Add
                      </button>
                      <button
                        onClick={() => {
                          setShowAddMeal(false);
                          setNewMealData({ meal: "", days: 1 });
                        }}
                        className="flex-1 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-xl transition-colors flex items-center justify-center gap-2 font-medium"
                      >
                        <X className="w-4 h-4" />
                        Cancel
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {/* View Mode */}
              <div>
                <label className="block text-sm text-gray-700 font-medium mb-3">
                  Plan Duration
                </label>
                <div className="grid grid-cols-3 gap-3">
                  {["day", "week", "month"].map((mode) => (
                    <button
                      key={mode}
                      onClick={() => setViewMode(mode)}
                      className={`py-3 rounded-xl transition-all capitalize font-medium ${
                        viewMode === mode
                          ? "bg-emerald-500 text-white shadow-lg"
                          : "bg-gray-100 border border-gray-200 text-gray-700 hover:border-emerald-300"
                      }`}
                    >
                      {mode}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            <button
              onClick={generateDietPlan}
              disabled={!profile.weight || !profile.height || !profile.age}
              className="w-full mt-6 py-4 bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-600 hover:to-green-700 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed text-white rounded-xl font-semibold text-lg shadow-xl transition-all"
            >
              Generate My Diet Plan
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-emerald-50 pb-20">
      <div className="max-w-6xl mx-auto p-4">
        {/* Header */}
        <div className="flex items-center justify-between mb-6 pt-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-green-600 rounded-xl flex items-center justify-center shadow-lg">
              <Apple className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-emerald-700">Nutri.ai</h1>
              <p className="text-xs text-emerald-600">Your {viewMode}ly plan</p>
            </div>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setStep("profile")}
              className="p-2 bg-white hover:bg-gray-50 rounded-xl transition-colors shadow-md border border-gray-200"
            >
              <Edit2 className="w-5 h-5 text-emerald-600" />
            </button>
            <button
              onClick={downloadChart}
              className="p-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded-xl transition-colors shadow-lg"
            >
              <Download className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Day Selector */}
        {viewMode !== "day" && (
          <div className="mb-6 overflow-x-auto pb-2">
            <div className="flex gap-2 min-w-max">
              {dietPlan.map((_, idx) => {
                const dayLabels =
                  viewMode === "week"
                    ? ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                    : Array.from({ length: 30 }, (_, i) => `Day ${i + 1}`);

                return (
                  <button
                    key={idx}
                    onClick={() => setSelectedDay(idx)}
                    className={`px-6 py-3 rounded-xl transition-all whitespace-nowrap ${
                      selectedDay === idx
                        ? "bg-gradient-to-r from-emerald-500 to-green-500 shadow-lg scale-105"
                        : "bg-emerald-900/40 hover:bg-emerald-800/40"
                    }`}
                  >
                    <div className="font-semibold">{dayLabels[idx]}</div>
                    <div className="text-xs opacity-80">
                      {getDailyTotals(idx).cal} cal
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* Daily Totals */}
        <div className="grid grid-cols-4 gap-3 mb-6">
          {[
            {
              label: "Calories",
              value: getDailyTotals(selectedDay).cal,
              unit: "cal",
            },
            {
              label: "Protein",
              value: getDailyTotals(selectedDay).protein,
              unit: "g",
            },
            {
              label: "Carbs",
              value: getDailyTotals(selectedDay).carbs,
              unit: "g",
            },
            { label: "Fat", value: getDailyTotals(selectedDay).fat, unit: "g" },
          ].map((stat) => (
            <div
              key={stat.label}
              className="bg-gradient-to-br from-emerald-900/40 to-green-900/30 rounded-2xl p-4 border border-emerald-700/30"
            >
              <div className="text-xs text-emerald-400 mb-1">{stat.label}</div>
              <div className="text-2xl font-bold text-white">
                {stat.value}
                <span className="text-sm text-emerald-400 ml-1">
                  {stat.unit}
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* Meal Plan - For Download */}
        <div
          ref={chartRef}
          className="bg-gradient-to-br from-emerald-900/40 to-green-900/30 rounded-3xl p-6 shadow-2xl border border-emerald-700/30"
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-emerald-300">
              {viewMode === "week"
                ? [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                  ][selectedDay]
                : `Day ${selectedDay + 1}`}
            </h2>
            <Calendar className="w-5 h-5 text-emerald-400" />
          </div>

          <div className="space-y-4">
            {mealTimes.map((mealTime) => {
              const meal = dietPlan[selectedDay][mealTime];
              return (
                <div
                  key={mealTime}
                  className="bg-emerald-950/30 rounded-2xl p-4 border border-emerald-700/20"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <div className="text-emerald-300 font-semibold mb-1">
                        {mealTime}
                      </div>
                      <div className="text-white font-medium text-lg">
                        {meal?.name}
                      </div>
                    </div>
                    <button
                      onClick={() =>
                        setEditingMeal({ day: selectedDay, mealTime })
                      }
                      className="p-2 hover:bg-emerald-700/30 rounded-lg transition-colors"
                    >
                      <Edit2 className="w-4 h-4 text-emerald-400" />
                    </button>
                  </div>
                  <div className="grid grid-cols-4 gap-3">
                    <div className="bg-emerald-950/50 rounded-lg p-2">
                      <div className="text-xs text-emerald-400">Cal</div>
                      <div className="text-sm font-semibold text-white">
                        {meal?.cal}
                      </div>
                    </div>
                    <div className="bg-emerald-950/50 rounded-lg p-2">
                      <div className="text-xs text-emerald-400">Protein</div>
                      <div className="text-sm font-semibold text-white">
                        {meal?.protein}g
                      </div>
                    </div>
                    <div className="bg-emerald-950/50 rounded-lg p-2">
                      <div className="text-xs text-emerald-400">Carbs</div>
                      <div className="text-sm font-semibold text-white">
                        {meal?.carbs}g
                      </div>
                    </div>
                    <div className="bg-emerald-950/50 rounded-lg p-2">
                      <div className="text-xs text-emerald-400">Fat</div>
                      <div className="text-sm font-semibold text-white">
                        {meal?.fat}g
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Edit Meal Modal */}
        {editingMeal && (
          <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-end md:items-center justify-center p-4 z-50">
            <div className="bg-gradient-to-br from-emerald-900 to-green-900 rounded-3xl p-6 max-w-md w-full max-h-[80vh] overflow-y-auto border border-emerald-700/50">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold text-emerald-300">
                  Replace {editingMeal.mealTime}
                </h3>
                <button
                  onClick={() => setEditingMeal(null)}
                  className="p-2 hover:bg-emerald-700/30 rounded-lg transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="space-y-3">
                {(
                  sampleMeals[profile.dietPreference]?.[editingMeal.mealTime] ||
                  []
                ).map((meal, idx) => (
                  <button
                    key={idx}
                    onClick={() =>
                      replaceMeal(editingMeal.day, editingMeal.mealTime, meal)
                    }
                    className="w-full bg-emerald-950/50 hover:bg-emerald-800/50 rounded-xl p-4 border border-emerald-700/30 transition-all text-left"
                  >
                    <div className="font-medium text-white mb-2">
                      {meal.name}
                    </div>
                    <div className="grid grid-cols-4 gap-2 text-xs">
                      <div>
                        <div className="text-emerald-400">Cal</div>
                        <div className="text-white font-semibold">
                          {meal.cal}
                        </div>
                      </div>
                      <div>
                        <div className="text-emerald-400">Protein</div>
                        <div className="text-white font-semibold">
                          {meal.protein}g
                        </div>
                      </div>
                      <div>
                        <div className="text-emerald-400">Carbs</div>
                        <div className="text-white font-semibold">
                          {meal.carbs}g
                        </div>
                      </div>
                      <div>
                        <div className="text-emerald-400">Fat</div>
                        <div className="text-white font-semibold">
                          {meal.fat}g
                        </div>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default NutriAI;
