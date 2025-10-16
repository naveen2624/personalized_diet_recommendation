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
} from "lucide-react";

export default function DietLandingPage() {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [showWaterAlert, setShowWaterAlert] = useState(false);
  const [lastWaterAlert, setLastWaterAlert] = useState(Date.now());

  // User health data
  const userData = {
    weight: 72,
    height: 170,
    bmi: 24.9,
    targetWeight: 68,
  };

  // Weight progress data
  const weightData = [
    { date: "Week 1", weight: 76 },
    { date: "Week 2", weight: 75 },
    { date: "Week 3", weight: 74 },
    { date: "Week 4", weight: 73 },
    { date: "Week 5", weight: 72 },
  ];

  // Diet schedule
  const dietSchedule = {
    breakfast: {
      time: "7:00 AM - 9:00 AM",
      meal: "Green Smoothie Bowl",
      calories: 320,
      ingredients: [
        "Spinach",
        "Banana",
        "Almond Milk",
        "Chia Seeds",
        "Berries",
        "Granola",
      ],
    },
    midMorning: {
      time: "10:00 AM - 11:00 AM",
      meal: "Mixed Nuts & Green Tea",
      calories: 180,
      ingredients: ["Almonds", "Walnuts", "Green Tea", "Honey"],
    },
    lunch: {
      time: "12:30 PM - 2:00 PM",
      meal: "Grilled Chicken Salad",
      calories: 450,
      ingredients: [
        "Chicken Breast",
        "Lettuce",
        "Cucumber",
        "Tomatoes",
        "Olive Oil",
        "Lemon",
      ],
    },
    evening: {
      time: "4:00 PM - 5:00 PM",
      meal: "Fruit Salad",
      calories: 150,
      ingredients: ["Apple", "Orange", "Grapes", "Kiwi"],
    },
    dinner: {
      time: "7:00 PM - 8:30 PM",
      meal: "Quinoa & Veggies",
      calories: 400,
      ingredients: [
        "Quinoa",
        "Broccoli",
        "Bell Peppers",
        "Garlic",
        "Olive Oil",
      ],
    },
  };

  // Get current meal based on time
  const getCurrentMeal = () => {
    const hour = currentTime.getHours();
    if (hour >= 7 && hour < 10) return { key: "breakfast", next: "midMorning" };
    if (hour >= 10 && hour < 12) return { key: "midMorning", next: "lunch" };
    if (hour >= 12 && hour < 16) return { key: "lunch", next: "evening" };
    if (hour >= 16 && hour < 19) return { key: "evening", next: "dinner" };
    return { key: "dinner", next: "breakfast" };
  };

  const currentMealInfo = getCurrentMeal();
  const currentMeal = dietSchedule[currentMealInfo.key];
  const nextMeal = dietSchedule[currentMealInfo.next];

  // Water alert every 2 hours
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-green-50 to-teal-50">
      {/* Water Alert Modal */}
      {showWaterAlert && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-3xl p-6 max-w-sm w-full shadow-2xl transform animate-bounce">
            <div className="flex justify-between items-start mb-4">
              <div className="bg-gradient-to-br from-blue-400 to-cyan-500 p-3 rounded-2xl">
                <Droplet className="w-8 h-8 text-white" />
              </div>
              <button
                onClick={() => setShowWaterAlert(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            <h3 className="text-2xl font-bold text-gray-800 mb-2">
              Hydration Time!
            </h3>
            <p className="text-gray-600 mb-4">
              It's been 2 hours. Time to drink some water and stay hydrated! 💧
            </p>
            <button
              onClick={() => setShowWaterAlert(false)}
              className="w-full bg-gradient-to-r from-blue-500 to-cyan-500 text-white py-3 rounded-xl font-semibold hover:shadow-lg transition-all"
            >
              Got it!
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
                  Your Personal Diet Companion
                </p>
              </div>
            </div>
            <div className="text-right">
              <div className="text-sm text-emerald-100">Today</div>
              <div className="font-semibold">
                {currentTime.toLocaleDateString("en-US", {
                  month: "short",
                  day: "numeric",
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
            <div className="text-gray-500 text-sm mb-1">Weight</div>
            <div className="text-3xl font-bold text-emerald-600">
              {userData.weight}
            </div>
            <div className="text-xs text-gray-400">kg</div>
          </div>
          <div className="bg-white rounded-2xl p-4 shadow-lg hover:shadow-xl transition-shadow">
            <div className="text-gray-500 text-sm mb-1">Height</div>
            <div className="text-3xl font-bold text-emerald-600">
              {userData.height}
            </div>
            <div className="text-xs text-gray-400">cm</div>
          </div>
          <div className="bg-white rounded-2xl p-4 shadow-lg hover:shadow-xl transition-shadow">
            <div className="text-gray-500 text-sm mb-1">BMI</div>
            <div className="text-3xl font-bold text-emerald-600">
              {userData.bmi}
            </div>
            <div className="text-xs text-gray-400">Normal</div>
          </div>
          <div className="bg-white rounded-2xl p-4 shadow-lg hover:shadow-xl transition-shadow">
            <div className="text-gray-500 text-sm mb-1">Target</div>
            <div className="text-3xl font-bold text-emerald-600">
              {userData.targetWeight}
            </div>
            <div className="text-xs text-gray-400">kg</div>
          </div>
        </div>

        {/* Current Meal */}
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
          <div className="bg-white bg-opacity-20 backdrop-blur-sm rounded-2xl p-4 text-gray-800">
            <div className="text-sm font-semibold mb-3">Ingredients</div>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2 ">
              {currentMeal.ingredients.map((ingredient, idx) => (
                <div
                  key={idx}
                  className="bg-opacity-20 rounded-lg px-3 py-2 text-sm backdrop-blur-sm border mb-3 border-emerald-50 hover:bg-opacity-30 transition-colors hover:scale-105 flex items-center justify-center shadow-md bg-emerald-50 text-gray-800"
                >
                  {ingredient}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Next Meal Ingredients */}
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
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
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

        {/* Weight Progress Chart */}
        <div className="bg-white rounded-3xl p-6 shadow-lg">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-2">
              <TrendingDown className="w-5 h-5 text-emerald-600" />
              <h3 className="text-xl font-bold text-gray-800">
                Weight Progress
              </h3>
            </div>
            <div className="text-sm text-emerald-600 font-semibold">-4 kg</div>
          </div>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={weightData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis
                dataKey="date"
                stroke="#6b7280"
                style={{ fontSize: "12px" }}
              />
              <YAxis
                stroke="#6b7280"
                style={{ fontSize: "12px" }}
                domain={[70, 78]}
              />
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

        {/* Daily Tips */}
        <div className="bg-gradient-to-br from-teal-50 to-emerald-50 rounded-3xl p-6 border-2 border-emerald-200">
          <h3 className="text-lg font-bold text-gray-800 mb-3">
            Today's Tip 💡
          </h3>
          <p className="text-gray-700">
            Stay consistent with your meal timing. Eating at regular intervals
            helps maintain metabolism and energy levels throughout the day.
          </p>
        </div>
      </main>

      {/* Footer */}
      <footer className="text-center py-8 text-gray-500 text-sm">
        <p>NutriFlow • Your journey to better health</p>
      </footer>
    </div>
  );
}
