"use client";
import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import {
  Calendar,
  Clock,
  TrendingDown,
  Droplet,
  Apple,
  AlertCircle,
  X,
  Loader,
  RefreshCw,
} from "lucide-react";

export default function DietLandingPage() {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [showWaterAlert, setShowWaterAlert] = useState(false);
  const [lastWaterAlert, setLastWaterAlert] = useState(Date.now());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // State for real data
  const [userData, setUserData] = useState(null);
  const [weightData, setWeightData] = useState([]);
  const [currentMeal, setCurrentMeal] = useState(null);
  const [nextMeal, setNextMeal] = useState(null);
  const [hydrationData, setHydrationData] = useState(null);
  const [nutritionTip, setNutritionTip] = useState("");
  const [userId, setUserId] = useState(null);

  // Calculate BMI
  const calculateBMI = (weight, height) => {
    if (!weight || !height) return 0;
    const heightInMeters = height / 100;
    return (weight / (heightInMeters * heightInMeters)).toFixed(1);
  };

  // Format meal data for display
  const formatMealForDisplay = (meal) => {
    if (!meal) return null;

    const ingredients =
      meal.ingredients?.map(
        (ing) => `${ing.ingredient_name} (${ing.quantity}${ing.unit || ""})`
      ) || [];

    const foodItems = meal.food_items?.map((item) => item.item_name) || [];

    const allIngredients = [...ingredients, ...foodItems];

    return {
      meal: meal.meal_name,
      time: meal.meal_time ? meal.meal_time.substring(0, 5) : "N/A",
      calories: meal.total_meal_calories || 0,
      ingredients:
        allIngredients.length > 0 ? allIngredients : ["No ingredients listed"],
    };
  };

  // Get current and next meal based on time
  const getMealsFromDailyPlan = (meals) => {
    if (!meals || meals.length === 0) return { current: null, next: null };

    const sortedMeals = [...meals].sort((a, b) => {
      const timeA = a.meal_time || "00:00";
      const timeB = b.meal_time || "00:00";
      return timeA.localeCompare(timeB);
    });

    const currentHour = currentTime.getHours();
    const currentMinute = currentTime.getMinutes();
    const currentTimeInMinutes = currentHour * 60 + currentMinute;

    let currentMealIndex = -1;

    for (let i = 0; i < sortedMeals.length; i++) {
      const mealTime = sortedMeals[i].meal_time || "00:00";
      const [hour, minute] = mealTime.split(":").map(Number);
      const mealTimeInMinutes = hour * 60 + minute;

      if (currentTimeInMinutes >= mealTimeInMinutes) {
        currentMealIndex = i;
      } else {
        break;
      }
    }

    const current =
      currentMealIndex >= 0 ? sortedMeals[currentMealIndex] : sortedMeals[0];
    const nextIndex = (currentMealIndex + 1) % sortedMeals.length;
    const next = sortedMeals[nextIndex];

    return { current, next };
  };

  // Load all data - this is where you'll integrate with your Supabase functions
  const loadData = async () => {
    setLoading(true);
    setError(null);

    try {
      // Import your supabase functions
      const {
        getCurrentUser,
        getUserProfile,
        getWeightHistory,
        getActiveDietPlan,
        getTodayHydration,
      } = await import("@/lib/supabase"); // Adjust path to your supabase client file

      // Get current user
      const { user, error: userError } = await getCurrentUser();

      if (userError || !user) {
        setError("Please log in to view your diet plan");
        setLoading(false);
        return;
      }

      setUserId(user.id);

      // Fetch user profile
      const { data: profile, error: profileError } = await getUserProfile(
        user.id
      );

      if (profile) {
        const bmi = calculateBMI(profile.weight, profile.height);
        const targetWeight =
          profile.goal === "weight_loss"
            ? profile.weight - 5
            : profile.goal === "muscle_gain"
            ? profile.weight + 3
            : profile.weight;

        setUserData({
          weight: profile.weight || 0,
          height: profile.height || 0,
          bmi: bmi,
          targetWeight: targetWeight,
          name: profile.name,
        });
      }

      // Fetch weight history
      const { data: weightHistory, error: weightError } =
        await getWeightHistory(user.id, 5);

      if (weightHistory && weightHistory.length > 0) {
        const formattedWeightData = weightHistory
          .reverse()
          .map((entry, index) => ({
            date: `Week ${index + 1}`,
            weight: parseFloat(entry.weight),
          }));
        setWeightData(formattedWeightData);
      }

      // Fetch active diet plan with meals
      const { data: dietPlan, error: planError } = await getActiveDietPlan(
        user.id
      );

      if (dietPlan && dietPlan.daily_meal_plans) {
        // Get today's meals
        const today = new Date().toISOString().split("T")[0];
        const todayPlan = dietPlan.daily_meal_plans.find(
          (plan) => plan.plan_date === today
        );

        if (todayPlan && todayPlan.meals) {
          const { current, next } = getMealsFromDailyPlan(todayPlan.meals);
          setCurrentMeal(formatMealForDisplay(current));
          setNextMeal(formatMealForDisplay(next));
        }

        // Get nutrition tip
        if (dietPlan.nutrition_tips && dietPlan.nutrition_tips.length > 0) {
          const randomTip =
            dietPlan.nutrition_tips[
              Math.floor(Math.random() * dietPlan.nutrition_tips.length)
            ];
          setNutritionTip(randomTip.tip);
        } else {
          setNutritionTip(
            "Stay consistent with your meal timing for better results!"
          );
        }
      }

      // Fetch hydration data
      const { data: hydration, error: hydrationError } =
        await getTodayHydration(user.id);

      if (hydration) {
        setHydrationData(hydration);
      } else {
        // Initialize default hydration data
        setHydrationData({
          consumed_liters: 0,
          target_liters: 2.5,
        });
      }
    } catch (err) {
      console.error("Load data error:", err);
      setError(
        "Failed to load data. Make sure you have imported supabaseClient properly."
      );
    } finally {
      setLoading(false);
    }
  };

  // Update hydration
  const updateHydration = async (amount) => {
    if (!userId) return;

    try {
      const { updateHydration: updateHydrationAPI } = await import(
        "@/lib/supabase"
      );

      const newAmount = (hydrationData?.consumed_liters || 0) + amount;

      const { data, error } = await updateHydrationAPI(userId, newAmount);

      if (!error && data) {
        setHydrationData(data);
      }
    } catch (err) {
      console.error("Update hydration error:", err);
    }
  };

  // Initial load
  useEffect(() => {
    loadData();
  }, []);

  // Water alert timer
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
      const now = Date.now();
      if (now - lastWaterAlert >= 2 * 60 * 60 * 1000) {
        setShowWaterAlert(true);
        setLastWaterAlert(now);
      }
    }, 60000);

    return () => clearInterval(timer);
  }, [lastWaterAlert]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-green-50 to-teal-50 flex items-center justify-center">
        <div className="text-center">
          <Loader className="w-12 h-12 text-emerald-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600 text-lg font-medium">
            Loading your diet plan...
          </p>
          <p className="text-gray-400 text-sm mt-2">
            Fetching data from Supabase
          </p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-green-50 to-teal-50 flex items-center justify-center p-4">
        <div className="text-center bg-white rounded-2xl p-8 shadow-lg max-w-md w-full">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <h3 className="text-xl font-bold text-gray-800 mb-2">Error</h3>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={loadData}
            className="bg-emerald-600 text-white px-6 py-3 rounded-lg hover:bg-emerald-700 transition-colors flex items-center space-x-2 mx-auto"
          >
            <RefreshCw className="w-4 h-4" />
            <span>Retry</span>
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-green-50 to-teal-50">
      {/* Water Alert Modal */}
      {showWaterAlert && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-3xl p-6 max-w-sm w-full shadow-2xl">
            <div className="flex justify-between items-start mb-4">
              <div className="bg-gradient-to-br from-blue-400 to-cyan-500 p-3 rounded-2xl">
                <Droplet className="w-8 h-8 text-white" />
              </div>
              <button
                onClick={() => {
                  setShowWaterAlert(false);
                  updateHydration(0.25);
                }}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            <h3 className="text-2xl font-bold text-gray-800 mb-2">
              Hydration Time!
            </h3>
            <p className="text-gray-600 mb-4">
              It`&apos;`s been 2 hours. Time to drink some water and stay
              hydrated! 💧
            </p>
            <button
              onClick={() => {
                setShowWaterAlert(false);
                updateHydration(0.25);
              }}
              className="w-full bg-gradient-to-r from-blue-500 to-cyan-500 text-white py-3 rounded-xl font-semibold hover:shadow-lg transition-all"
            >
              Got it! I drank water
            </button>
          </div>
        </div>
      )}

      {/* Header */}
      <header className="bg-gradient-to-r from-emerald-600 to-green-600 text-white p-6 shadow-lg">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-white bg-opacity-20 p-2 rounded-xl backdrop-blur-sm">
                <Apple className="w-8 h-8" />
              </div>
              <div>
                <h1 className="text-3xl font-bold">Nutri.ai</h1>
                <p className="text-emerald-100 text-sm">
                  {userData?.name
                    ? `Welcome back, ${userData.name}!`
                    : "Your Personal Diet Companion"}
                </p>
              </div>
            </div>
            <div className="text-right">
              <div className="text-sm text-emerald-100">Today</div>
              <div className="font-semibold">
                {currentTime.toLocaleDateString("en-US", {
                  month: "short",
                  day: "numeric",
                  year: "numeric",
                })}
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto p-4 md:p-6 space-y-6">
        {/* Health Stats Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-white rounded-2xl p-4 shadow-lg hover:shadow-xl transition-shadow">
            <div className="text-gray-500 text-sm mb-1">Current Weight</div>
            <div className="text-3xl font-bold text-emerald-600">
              {userData?.weight || 0}
            </div>
            <div className="text-xs text-gray-400">kg</div>
          </div>
          <div className="bg-white rounded-2xl p-4 shadow-lg hover:shadow-xl transition-shadow">
            <div className="text-gray-500 text-sm mb-1">Height</div>
            <div className="text-3xl font-bold text-emerald-600">
              {userData?.height || 0}
            </div>
            <div className="text-xs text-gray-400">cm</div>
          </div>
          <div className="bg-white rounded-2xl p-4 shadow-lg hover:shadow-xl transition-shadow">
            <div className="text-gray-500 text-sm mb-1">BMI</div>
            <div className="text-3xl font-bold text-emerald-600">
              {userData?.bmi || 0}
            </div>
            <div className="text-xs text-gray-400">
              {userData?.bmi < 18.5
                ? "Underweight"
                : userData?.bmi < 25
                ? "Normal"
                : userData?.bmi < 30
                ? "Overweight"
                : "Obese"}
            </div>
          </div>
          <div className="bg-white rounded-2xl p-4 shadow-lg hover:shadow-xl transition-shadow">
            <div className="text-gray-500 text-sm mb-1">Target Weight</div>
            <div className="text-3xl font-bold text-emerald-600">
              {userData?.targetWeight || 0}
            </div>
            <div className="text-xs text-gray-400">kg</div>
          </div>
        </div>

        {/* Current Meal */}
        {currentMeal ? (
          <div className="bg-gradient-to-br from-emerald-500 to-green-600 rounded-3xl p-6 shadow-2xl text-white">
            <div className="flex items-center space-x-2 mb-4">
              <Clock className="w-5 h-5" />
              <span className="text-emerald-100 text-sm font-medium">
                Current Meal
              </span>
            </div>
            <h2 className="text-3xl md:text-4xl font-bold mb-2">
              {currentMeal.meal}
            </h2>
            <div className="flex items-center space-x-4 text-emerald-100 mb-4">
              <span className="text-sm">{currentMeal.time}</span>
              <span className="text-sm">•</span>
              <span className="text-sm">{currentMeal.calories} cal</span>
            </div>
            <div className="bg-white bg-opacity-20 backdrop-blur-sm rounded-2xl p-4">
              <div className="text-sm font-semibold mb-3 text-white">
                Ingredients
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {currentMeal.ingredients.map((ingredient, idx) => (
                  <div
                    key={idx}
                    className="bg-emerald-50 rounded-lg px-3 py-2 text-sm backdrop-blur-sm border border-emerald-100 hover:bg-opacity-90 transition-all hover:scale-105 flex items-center shadow-md text-gray-800"
                  >
                    {ingredient}
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="bg-white rounded-3xl p-6 shadow-lg text-center">
            <Calendar className="w-12 h-12 text-gray-300 mx-auto mb-3" />
            <p className="text-gray-500">No meal scheduled at this time</p>
            <p className="text-gray-400 text-sm mt-1">
              Check your diet plan or generate a new one
            </p>
          </div>
        )}

        {/* Next Meal */}
        {nextMeal && (
          <div className="bg-white rounded-3xl p-6 shadow-lg">
            <div className="flex items-center space-x-2 mb-4">
              <AlertCircle className="w-5 h-5 text-emerald-600" />
              <span className="text-gray-700 font-semibold">
                Prep for Next: {nextMeal.meal}
              </span>
            </div>
            <div className="text-sm text-gray-500 mb-3">
              {nextMeal.time} • {nextMeal.calories} cal
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {nextMeal.ingredients.map((ingredient, idx) => (
                <div
                  key={idx}
                  className="flex items-center space-x-2 bg-emerald-50 rounded-xl px-4 py-3 hover:bg-emerald-100 transition-colors"
                >
                  <div className="w-2 h-2 bg-emerald-500 rounded-full"></div>
                  <span className="text-gray-700 text-sm">{ingredient}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Weight Progress Chart */}
        {weightData.length > 0 && (
          <div className="bg-white rounded-3xl p-6 shadow-lg">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-2">
                <TrendingDown className="w-5 h-5 text-emerald-600" />
                <h3 className="text-xl font-bold text-gray-800">
                  Weight Progress
                </h3>
              </div>
              <div className="text-sm text-emerald-600 font-semibold">
                {weightData.length > 1
                  ? `${(
                      weightData[0].weight -
                      weightData[weightData.length - 1].weight
                    ).toFixed(1)} kg`
                  : "Tracking..."}
              </div>
            </div>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={weightData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis
                  dataKey="date"
                  stroke="#6b7280"
                  style={{ fontSize: "12px" }}
                />
                <YAxis stroke="#6b7280" style={{ fontSize: "12px" }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#fff",
                    border: "none",
                    borderRadius: "12px",
                    boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="weight"
                  stroke="#10b981"
                  strokeWidth={3}
                  dot={{ fill: "#10b981", r: 5 }}
                  activeDot={{ r: 7 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Hydration Tracking */}
        {hydrationData && (
          <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-3xl p-6 border-2 border-blue-200 shadow-lg">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <Droplet className="w-5 h-5 text-blue-600" />
                <h3 className="text-lg font-bold text-gray-800">
                  Today`&apos;`s Hydration
                </h3>
              </div>
              <span className="text-sm font-semibold text-blue-600">
                {(hydrationData.consumed_liters || 0).toFixed(1)}L /{" "}
                {(hydrationData.target_liters || 2.5).toFixed(1)}L
              </span>
            </div>
            <div className="w-full bg-blue-200 rounded-full h-4 mb-3">
              <div
                className="bg-gradient-to-r from-blue-500 to-cyan-500 h-4 rounded-full transition-all duration-500"
                style={{
                  width: `${Math.min(
                    ((hydrationData.consumed_liters || 0) /
                      (hydrationData.target_liters || 2.5)) *
                      100,
                    100
                  )}%`,
                }}
              ></div>
            </div>
            <button
              onClick={() => updateHydration(0.25)}
              className="w-full bg-gradient-to-r from-blue-500 to-cyan-500 text-white py-2 rounded-xl font-semibold hover:shadow-lg transition-all text-sm"
            >
              + Add 250ml
            </button>
          </div>
        )}

        {/* Daily Tips */}
        <div className="bg-gradient-to-br from-teal-50 to-emerald-50 rounded-3xl p-6 border-2 border-emerald-200">
          <h3 className="text-lg font-bold text-gray-800 mb-3 flex items-center space-x-2">
            <span>Today`&apos;`s Tip</span>
            <span className="text-2xl">💡</span>
          </h3>
          <p className="text-gray-700 leading-relaxed">{nutritionTip}</p>
        </div>
      </main>

      {/* Footer */}
      <footer className="text-center py-8 text-gray-500 text-sm">
        <p>Nutri.ai • Your journey to better health</p>
        <p className="text-xs text-gray-400 mt-1">Connected to Supabase</p>
      </footer>
    </div>
  );
}
