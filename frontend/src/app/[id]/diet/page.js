// frontend/src/app/[id]/diet/page.js
"use client";
import React, { useState, useEffect, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import {
  Apple,
  Edit2,
  Download,
  Calendar,
  TrendingDown,
  TrendingUp,
  Target,
  Loader2,
  AlertCircle,
} from "lucide-react";
import {
  getUserProfile,
  getDietaryRestrictions,
  getActiveDietPlan,
  generateAndSaveDietPlan,
  updateUserProfile,
} from "@/lib/supabase";

const NutriAI = () => {
  const params = useParams();
  const router = useRouter();
  const userId = params.id;

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [generating, setGenerating] = useState(false);

  const [step, setStep] = useState("profile");
  const [userProfile, setUserProfile] = useState(null);
  const [profile, setProfile] = useState({
    weight: "",
    height: "",
    age: "",
    gender: "male",
    dietPreference: "vegetarian",
    restrictions: [],
    goal: "maintain",
    meals_per_day: 3,
    activity_level: "moderately_active",
  });

  const [dietPlan, setDietPlan] = useState(null);
  const [selectedDay, setSelectedDay] = useState(0);
  const chartRef = useRef(null);

  const goals = [
    {
      value: "loss",
      label: "Weight Loss",
      icon: TrendingDown,
      apiValue: "Weight Loss",
    },
    {
      value: "gain",
      label: "Weight Gain",
      icon: TrendingUp,
      apiValue: "Muscle Gain",
    },
    {
      value: "maintain",
      label: "Maintain",
      icon: Target,
      apiValue: "Weight Maintenance",
    },
  ];

  const activityLevels = [
    { value: "sedentary", label: "Sedentary", apiValue: "Sedentary" },
    {
      value: "lightly_active",
      label: "Lightly Active",
      apiValue: "Lightly Active",
    },
    {
      value: "moderately_active",
      label: "Moderately Active",
      apiValue: "Moderately Active",
    },
    { value: "very_active", label: "Very Active", apiValue: "Very Active" },
    {
      value: "extremely_active",
      label: "Extremely Active",
      apiValue: "Extremely Active",
    },
  ];

  const dietPreferences = [
    { value: "vegetarian", label: "Vegetarian", apiValue: "Vegetarian" },
    { value: "vegan", label: "Vegan", apiValue: "Vegan" },
    {
      value: "non-vegetarian",
      label: "Non-Vegetarian",
      apiValue: "Non-Vegetarian",
    },
    { value: "eggetarian", label: "Eggetarian", apiValue: "Vegetarian" },
  ];

  const restrictions = [
    "Gluten-Free",
    "Dairy-Free",
    "Nut-Free",
    "Soy-Free",
    "Low-Carb",
  ];

  useEffect(() => {
    loadUserData();
  }, [userId]);

  const loadUserData = async () => {
    try {
      setLoading(true);
      setError(null);

      const { data: profileData, error: profileError } = await getUserProfile(
        userId
      );
      if (profileError) throw profileError;

      if (!profileData) {
        setError("User profile not found");
        return;
      }

      setUserProfile(profileData);

      const { data: restrictionsData } = await getDietaryRestrictions(userId);
      const userRestrictions =
        restrictionsData?.map((r) => r.restriction) || [];

      setProfile({
        weight: profileData.weight || "",
        height: profileData.height || "",
        age: profileData.age || "",
        gender: profileData.gender || "male",
        dietPreference: profileData.diet_preference || "vegetarian",
        restrictions: userRestrictions,
        goal: profileData.goal || "maintain",
        meals_per_day: profileData.meals_per_day || 3,
        activity_level: profileData.activity_level || "moderately_active",
      });

      const { data: existingPlan, error: planError } = await getActiveDietPlan(
        userId
      );

      if (existingPlan && !planError) {
        const formattedPlan = formatSupabasePlanForDisplay(existingPlan);
        setDietPlan(formattedPlan);
        setStep("plan");
      }
    } catch (err) {
      console.error("Error loading user data:", err);
      setError(err.message || "Failed to load user data");
    } finally {
      setLoading(false);
    }
  };

  const formatSupabasePlanForDisplay = (supabasePlan) => {
    const days = supabasePlan.daily_meal_plans.map((dailyPlan) => {
      const dayMeals = {};

      dailyPlan.meals.forEach((meal) => {
        dayMeals[meal.meal_type] = {
          name: meal.meal_name,
          cal: meal.total_meal_calories,
          protein: meal.food_items.reduce(
            (sum, item) => sum + (item.protein || 0),
            0
          ),
          carbs: meal.food_items.reduce(
            (sum, item) => sum + (item.carbs || 0),
            0
          ),
          fat: meal.food_items.reduce((sum, item) => sum + (item.fats || 0), 0),
          food_items: meal.food_items,
          ingredients: meal.ingredients,
          recipe_steps: meal.recipe_steps,
          cooking_time: meal.cooking_time,
          difficulty_level: meal.difficulty_level,
          notes: meal.notes,
        };
      });

      return dayMeals;
    });

    return days;
  };

  const calculateBMI = () => {
    if (!profile.height || !profile.weight) return "N/A";
    const heightM = profile.height / 100;
    const bmi = profile.weight / (heightM * heightM);
    return bmi.toFixed(1);
  };

  const generateDietPlan = async () => {
    try {
      setGenerating(true);
      setError(null);

      const updates = {
        weight: parseFloat(profile.weight),
        height: parseFloat(profile.height),
        age: parseInt(profile.age),
        gender: profile.gender,
        diet_preference: profile.dietPreference,
        goal: profile.goal,
        activity_level: profile.activity_level,
        meals_per_day: profile.meals_per_day,
      };

      await updateUserProfile(userId, updates);

      const goalObj = goals.find((g) => g.value === profile.goal);
      const activityObj = activityLevels.find(
        (a) => a.value === profile.activity_level
      );
      const dietPrefObj = dietPreferences.find(
        (d) => d.value === profile.dietPreference
      );

      const userDataForAPI = {
        goal: goalObj?.apiValue || "Weight Maintenance",
        diet_preference: dietPrefObj?.apiValue || "Vegetarian",
        age: profile.age,
        gender: profile.gender,
        weight: profile.weight,
        height: profile.height,
        activity_level: activityObj?.apiValue || "Moderately Active",
        allergies: profile.restrictions.join(", ") || "None",
        dislikes: "None",
        meals_per_day: profile.meals_per_day,
      };

      const { data: newPlan, error: planError } = await generateAndSaveDietPlan(
        userId,
        userDataForAPI
      );

      if (planError) throw planError;

      const { data: fullPlan } = await getActiveDietPlan(userId);

      if (fullPlan) {
        const formattedPlan = formatSupabasePlanForDisplay(fullPlan);
        setDietPlan(formattedPlan);
        setStep("plan");
      }
    } catch (err) {
      console.error("Error generating diet plan:", err);
      setError(
        err.message || "Failed to generate diet plan. Please try again."
      );
    } finally {
      setGenerating(false);
    }
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

  const downloadChart = () => {
    const dayLabel =
      selectedDay < 7
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
    const mealTimes = Object.keys(dietPlan[selectedDay]);

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
    content += `Total Calories: ${Math.round(totals.cal)} cal\n`;
    content += `Protein: ${Math.round(totals.protein)}g\n`;
    content += `Carbohydrates: ${Math.round(totals.carbs)}g\n`;
    content += `Fat: ${Math.round(totals.fat)}g\n\n`;

    content += `MEAL PLAN\n`;
    content += `${"=".repeat(50)}\n\n`;

    mealTimes.forEach((mealTime) => {
      const meal = dietPlan[selectedDay][mealTime];
      content += `${mealTime.toUpperCase()}\n`;
      content += `${"-".repeat(50)}\n`;
      content += `Meal: ${meal?.name || "Not set"}\n`;
      content += `Calories: ${meal?.cal || 0} cal\n`;
      content += `Protein: ${Math.round(
        meal?.protein || 0
      )}g | Carbs: ${Math.round(meal?.carbs || 0)}g | Fat: ${Math.round(
        meal?.fat || 0
      )}g\n`;

      if (meal?.cooking_time) {
        content += `Cooking Time: ${meal.cooking_time}\n`;
      }
      if (meal?.difficulty_level) {
        content += `Difficulty: ${meal.difficulty_level}\n`;
      }
      content += `\n`;
    });

    content += `\n${"=".repeat(50)}\n`;
    content += `Generated by Nutri.ai - Your AI-Powered Nutrition Assistant\n`;

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

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-emerald-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-emerald-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading your profile...</p>
        </div>
      </div>
    );
  }

  if (error && !userProfile) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-emerald-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-3xl p-8 shadow-xl border border-red-200 max-w-md">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-bold text-gray-900 mb-2 text-center">
            Error
          </h2>
          <p className="text-gray-600 text-center mb-4">{error}</p>
          <button
            onClick={() => router.push("/")}
            className="w-full py-3 bg-emerald-500 hover:bg-emerald-600 text-white rounded-xl font-semibold transition-colors"
          >
            Go to Home
          </button>
        </div>
      </div>
    );
  }

  if (step === "profile") {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-emerald-50 p-4">
        <div className="max-w-2xl mx-auto">
          <div className="flex items-center justify-center gap-3 mb-8 pt-8">
            <div className="w-12 h-12 bg-gradient-to-br from-emerald-500 to-green-600 rounded-2xl flex items-center justify-center shadow-lg">
              <Apple className="w-7 h-7 text-white" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-emerald-600 to-green-600 bg-clip-text text-transparent">
              Nutri.ai
            </h1>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-6 flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
              <p className="text-red-700 text-sm">{error}</p>
            </div>
          )}

          <div className="bg-white rounded-3xl p-6 shadow-xl border border-emerald-100">
            <h2 className="text-2xl font-semibold mb-6 text-emerald-700">
              Your Profile
            </h2>

            <div className="space-y-4">
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

              <div>
                <label className="block text-sm text-gray-700 font-medium mb-2">
                  Activity Level
                </label>
                <select
                  value={profile.activity_level}
                  onChange={(e) =>
                    setProfile({ ...profile, activity_level: e.target.value })
                  }
                  className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                >
                  {activityLevels.map((level) => (
                    <option key={level.value} value={level.value}>
                      {level.label}
                    </option>
                  ))}
                </select>
              </div>

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
                    <option key={pref.value} value={pref.value}>
                      {pref.label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm text-gray-700 font-medium mb-2">
                  Meals Per Day
                </label>
                <select
                  value={profile.meals_per_day}
                  onChange={(e) =>
                    setProfile({
                      ...profile,
                      meals_per_day: parseInt(e.target.value),
                    })
                  }
                  className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                >
                  {[3, 4, 5, 6].map((num) => (
                    <option key={num} value={num}>
                      {num} meals
                    </option>
                  ))}
                </select>
              </div>

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
            </div>

            <button
              onClick={generateDietPlan}
              disabled={
                !profile.weight || !profile.height || !profile.age || generating
              }
              className="w-full mt-6 py-4 bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-600 hover:to-green-700 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed text-white rounded-xl font-semibold text-lg shadow-xl transition-all flex items-center justify-center gap-2"
            >
              {generating ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Generating Your Plan...
                </>
              ) : (
                "Generate My Diet Plan"
              )}
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-emerald-50 pb-20">
      <div className="max-w-6xl mx-auto p-4">
        <div className="flex items-center justify-between mb-6 pt-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-green-600 rounded-xl flex items-center justify-center shadow-lg">
              <Apple className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-emerald-700">Nutri.ai</h1>
              <p className="text-xs text-emerald-600">Your 7-day plan</p>
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

        <div className="mb-6 overflow-x-auto pb-2">
          <div className="flex gap-2 min-w-max">
            {dietPlan &&
              dietPlan.map((_, idx) => {
                const dayLabels = [
                  "Mon",
                  "Tue",
                  "Wed",
                  "Thu",
                  "Fri",
                  "Sat",
                  "Sun",
                ];

                return (
                  <button
                    key={idx}
                    onClick={() => setSelectedDay(idx)}
                    className={`px-6 py-3 rounded-xl transition-all whitespace-nowrap ${
                      selectedDay === idx
                        ? "bg-gradient-to-r from-emerald-500 to-green-500 text-white shadow-lg scale-105"
                        : "bg-white text-gray-700 hover:bg-gray-50 border border-gray-200"
                    }`}
                  >
                    <div className="font-semibold">{dayLabels[idx]}</div>
                    <div className="text-xs opacity-80">
                      {Math.round(getDailyTotals(idx).cal)} cal
                    </div>
                  </button>
                );
              })}
          </div>
        </div>

        <div className="grid grid-cols-4 gap-3 mb-6">
          {[
            {
              label: "Calories",
              value: Math.round(getDailyTotals(selectedDay).cal),
              unit: "cal",
            },
            {
              label: "Protein",
              value: Math.round(getDailyTotals(selectedDay).protein),
              unit: "g",
            },
            {
              label: "Carbs",
              value: Math.round(getDailyTotals(selectedDay).carbs),
              unit: "g",
            },
            {
              label: "Fat",
              value: Math.round(getDailyTotals(selectedDay).fat),
              unit: "g",
            },
          ].map((stat) => (
            <div
              key={stat.label}
              className="bg-white rounded-2xl p-4 border border-emerald-100 shadow-sm"
            >
              <div className="text-xs text-emerald-600 mb-1">{stat.label}</div>
              <div className="text-2xl font-bold text-gray-900">
                {stat.value}
                <span className="text-sm text-emerald-600 ml-1">
                  {stat.unit}
                </span>
              </div>
            </div>
          ))}
        </div>

        <div
          ref={chartRef}
          className="bg-white rounded-3xl p-6 shadow-xl border border-emerald-100"
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-emerald-700">
              {
                [
                  "Monday",
                  "Tuesday",
                  "Wednesday",
                  "Thursday",
                  "Friday",
                  "Saturday",
                  "Sunday",
                ][selectedDay]
              }
            </h2>
            <Calendar className="w-5 h-5 text-emerald-600" />
          </div>

          <div className="space-y-4">
            {dietPlan &&
              dietPlan[selectedDay] &&
              Object.keys(dietPlan[selectedDay]).map((mealTime) => {
                const meal = dietPlan[selectedDay][mealTime];
                return (
                  <div
                    key={mealTime}
                    className="bg-emerald-50 rounded-2xl p-4 border border-emerald-100"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <div className="text-emerald-700 font-semibold mb-1">
                          {mealTime}
                        </div>
                        <div className="text-gray-900 font-medium text-lg">
                          {meal?.name}
                        </div>
                        {meal?.cooking_time && (
                          <div className="text-xs text-gray-600 mt-1">
                            ⏱️ {meal.cooking_time}
                          </div>
                        )}
                      </div>
                    </div>

                    <div className="grid grid-cols-4 gap-3">
                      <div className="bg-white rounded-lg p-2">
                        <div className="text-xs text-emerald-600">Cal</div>
                        <div className="text-sm font-semibold text-gray-900">
                          {Math.round(meal?.cal || 0)}
                        </div>
                      </div>
                      <div className="bg-white rounded-lg p-2">
                        <div className="text-xs text-emerald-600">Protein</div>
                        <div className="text-sm font-semibold text-gray-900">
                          {Math.round(meal?.protein || 0)}g
                        </div>
                      </div>
                      <div className="bg-white rounded-lg p-2">
                        <div className="text-xs text-emerald-600">Carbs</div>
                        <div className="text-sm font-semibold text-gray-900">
                          {Math.round(meal?.carbs || 0)}g
                        </div>
                      </div>
                      <div className="bg-white rounded-lg p-2">
                        <div className="text-xs text-emerald-600">Fat</div>
                        <div className="text-sm font-semibold text-gray-900">
                          {Math.round(meal?.fat || 0)}g
                        </div>
                      </div>
                    </div>

                    {meal?.food_items && meal.food_items.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-emerald-200">
                        <div className="text-xs font-semibold text-emerald-700 mb-2">
                          Food Items:
                        </div>
                        <div className="space-y-1">
                          {meal.food_items.map((item, idx) => (
                            <div key={idx} className="text-xs text-gray-700">
                              • {item.item_name} - {item.quantity}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {meal?.recipe_steps && meal.recipe_steps.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-emerald-200">
                        <div className="text-xs font-semibold text-emerald-700 mb-2">
                          Recipe:
                        </div>
                        <div className="space-y-2">
                          {meal.recipe_steps
                            .sort((a, b) => a.step_number - b.step_number)
                            .map((step) => (
                              <div
                                key={step.step_number}
                                className="text-xs text-gray-700"
                              >
                                <span className="font-semibold">
                                  {step.step_number}.
                                </span>{" "}
                                {step.instruction}
                              </div>
                            ))}
                        </div>
                      </div>
                    )}

                    {meal?.notes && (
                      <div className="mt-3 pt-3 border-t border-emerald-200">
                        <div className="text-xs text-gray-600 italic">
                          💡 {meal.notes}
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default NutriAI;
