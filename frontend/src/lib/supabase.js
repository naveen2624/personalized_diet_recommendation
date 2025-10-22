// frontend/src/lib/supabase.js
import { createClient } from "@supabase/supabase-js";

// Initialize Supabase client
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// ============================================
// AUTHENTICATION FUNCTIONS
// ============================================

/**
 * Sign up with email and password
 */
/**
 * Sign up with email and password
 */
export const signUpWithEmail = async (email, password, name) => {
  try {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          name: name || "",
        },
      },
    });

    if (error) throw error;

    // Create minimal user profile
    if (data.user) {
      const { error: profileError } = await supabase
        .from("user_profiles")
        .insert({
          id: data.user.id,
          email: email,
          name: name || null,
        });

      if (profileError) {
        console.error("Profile creation error:", profileError);
        // Don't throw here - the auth account was created successfully
        // The profile can be created later
      }
    }

    return { data, error: null };
  } catch (error) {
    console.error("Sign up error:", error);
    return { data: null, error };
  }
};

/**
 * Sign in with email and password
 */
export const signInWithEmail = async (email, password) => {
  try {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) throw error;
    return { data, error: null };
  } catch (error) {
    console.error("Sign in error:", error);
    return { data: null, error };
  }
};

/**
 * Sign in with Google
 */
export const signInWithGoogle = async () => {
  try {
    const { data, error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    });

    if (error) throw error;
    return { data, error: null };
  } catch (error) {
    console.error("Google sign in error:", error);
    return { data: null, error };
  }
};

/**
 * Sign out
 */
export const signOut = async () => {
  try {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
    return { error: null };
  } catch (error) {
    console.error("Sign out error:", error);
    return { error };
  }
};

/**
 * Get current user
 */
export const getCurrentUser = async () => {
  try {
    const {
      data: { user },
      error,
    } = await supabase.auth.getUser();
    if (error) throw error;
    return { user, error: null };
  } catch (error) {
    console.error("Get user error:", error);
    return { user: null, error };
  }
};

/**
 * Reset password
 */
export const resetPassword = async (email) => {
  try {
    const { data, error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/auth/reset-password`,
    });

    if (error) throw error;
    return { data, error: null };
  } catch (error) {
    console.error("Reset password error:", error);
    return { data: null, error };
  }
};

// ============================================
// USER PROFILE FUNCTIONS
// ============================================

/**
 * Create or update user profile
 */
export const createUserProfile = async (profileData) => {
  try {
    const { data, error } = await supabase
      .from("user_profiles")
      .upsert({
        id: profileData.id,
        email: profileData.email,
        name: profileData.name,
        height: profileData.height,
        weight: profileData.weight,
        age: profileData.age,
        gender: profileData.gender,
        diet_preference: profileData.diet_preference,
        goal: profileData.goal,
        activity_level: profileData.activity_level,
        meals_per_day: profileData.meals_per_day || 3,
        profile_pic: profileData.profile_pic,
        updated_at: new Date().toISOString(),
      })
      .select()
      .single();

    if (error) throw error;
    return { data, error: null };
  } catch (error) {
    console.error("Create profile error:", error);
    return { data: null, error };
  }
};

/**
 * Get user profile
 */
export const getUserProfile = async (userId) => {
  try {
    const { data, error } = await supabase
      .from("user_profiles")
      .select("*")
      .eq("id", userId)
      .single();

    if (error) throw error;
    return { data, error: null };
  } catch (error) {
    console.error("Get profile error:", error);
    return { data: null, error };
  }
};

/**
 * Update user profile
 */
/**
 * Update user profile (with upsert to handle missing profiles)
 */
/**
 * Update user profile (with upsert to handle missing profiles)
 */
/**
 * Update user profile (with proper upsert handling)
 */
export const updateUserProfile = async (userId, updates) => {
  try {
    if (!userId) {
      throw new Error("User ID is required");
    }

    // Clean up the updates object - remove null/undefined values
    const cleanUpdates = Object.entries(updates).reduce((acc, [key, value]) => {
      if (value !== undefined && value !== null && value !== "") {
        acc[key] = value;
      }
      return acc;
    }, {});

    console.log("Updating profile with:", cleanUpdates);

    // Use upsert to handle both insert and update cases
    const { data, error } = await supabase
      .from("user_profiles")
      .upsert(
        {
          id: userId,
          ...cleanUpdates,
          updated_at: new Date().toISOString(),
        },
        {
          onConflict: "id",
        }
      )
      .select()
      .single();

    if (error) {
      console.error("Supabase update error:", error);
      throw error;
    }

    return { data, error: null };
  } catch (error) {
    console.error("Update profile error:", error);
    return {
      data: null,
      error: {
        message: error.message || "Failed to update profile",
        details: error,
      },
    };
  }
};

// ============================================
// DIETARY RESTRICTIONS FUNCTIONS
// ============================================

/**
 * Add dietary restriction
 */
export const addDietaryRestriction = async (
  userId,
  restriction,
  type = "dislike"
) => {
  try {
    const { data, error } = await supabase
      .from("dietary_restrictions")
      .insert({
        user_id: userId,
        restriction,
        type,
      })
      .select()
      .single();

    if (error) throw error;
    return { data, error: null };
  } catch (error) {
    console.error("Add restriction error:", error);
    return { data: null, error };
  }
};

/**
 * Get user dietary restrictions
 */
export const getDietaryRestrictions = async (userId) => {
  try {
    const { data, error } = await supabase
      .from("dietary_restrictions")
      .select("*")
      .eq("user_id", userId);

    if (error) throw error;
    return { data, error: null };
  } catch (error) {
    console.error("Get restrictions error:", error);
    return { data: null, error };
  }
};

/**
 * Delete dietary restriction
 */
export const deleteDietaryRestriction = async (restrictionId) => {
  try {
    const { error } = await supabase
      .from("dietary_restrictions")
      .delete()
      .eq("id", restrictionId);

    if (error) throw error;
    return { error: null };
  } catch (error) {
    console.error("Delete restriction error:", error);
    return { error };
  }
};

// ============================================
// DIET PLAN FUNCTIONS
// ============================================

/**
 * Generate and save diet plan from API
 */
// Add this to your supabase.js file - REPLACE the existing generateAndSaveDietPlan function

/**
 * Generate and save diet plan from API
 */
export const generateAndSaveDietPlan = async (userId, userProfile) => {
  try {
    // Fetch diet plan from your Flask API
    const response = await fetch("http://localhost:6060/api/diet-plan", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        goal: userProfile.goal,
        diet_preference: userProfile.diet_preference,
        age: userProfile.age,
        gender: userProfile.gender,
        weight: userProfile.weight,
        height: userProfile.height,
        activity_level: userProfile.activity_level,
        allergies: userProfile.allergies || "None",
        dislikes: userProfile.dislikes || "None",
        meals_per_day: userProfile.meals_per_day || 3,
      }),
    });

    if (!response.ok) {
      throw new Error("Failed to generate diet plan from API");
    }

    const apiData = await response.json();
    const dietPlanData = apiData.diet_plan;

    // Deactivate old plans
    await supabase
      .from("diet_plans")
      .update({ is_active: false })
      .eq("user_id", userId);

    // Create new diet plan
    const startDate = new Date();
    const endDate = new Date();
    endDate.setDate(endDate.getDate() + 6); // 7-day plan

    const { data: dietPlan, error: dietPlanError } = await supabase
      .from("diet_plans")
      .insert({
        user_id: userId,
        plan_name: `Diet Plan - ${startDate.toLocaleDateString()}`,
        start_date: startDate.toISOString().split("T")[0],
        end_date: endDate.toISOString().split("T")[0],
        daily_calorie_target: Math.round(
          dietPlanData.daily_calorie_target || 0
        ),
        bmr: parseFloat(dietPlanData.bmr || 0),
        tdee: parseFloat(dietPlanData.tdee || 0),
        calorie_adjustment: Math.round(dietPlanData.calorie_adjustment || 0),
        protein_grams: parseFloat(
          dietPlanData.macronutrient_breakdown?.protein_grams || 0
        ),
        protein_percentage: parseFloat(
          dietPlanData.macronutrient_breakdown?.protein_percentage || 0
        ),
        carbs_grams: parseFloat(
          dietPlanData.macronutrient_breakdown?.carbs_grams || 0
        ),
        carbs_percentage: parseFloat(
          dietPlanData.macronutrient_breakdown?.carbs_percentage || 0
        ),
        fats_grams: parseFloat(
          dietPlanData.macronutrient_breakdown?.fats_grams || 0
        ),
        fats_percentage: parseFloat(
          dietPlanData.macronutrient_breakdown?.fats_percentage || 0
        ),
        is_active: true,
      })
      .select()
      .single();

    if (dietPlanError) throw dietPlanError;

    // Save daily meal plans
    for (const day of dietPlanData.meal_plan) {
      const planDate = new Date(startDate);
      planDate.setDate(planDate.getDate() + (day.day - 1));

      const { data: dailyPlan, error: dailyError } = await supabase
        .from("daily_meal_plans")
        .insert({
          diet_plan_id: dietPlan.id,
          user_id: userId,
          day_number: day.day,
          day_name: day.day_name,
          plan_date: planDate.toISOString().split("T")[0],
          daily_total_calories: Math.round(day.daily_total_calories || 0),
        })
        .select()
        .single();

      if (dailyError) throw dailyError;

      // Save meals for each day
      for (const meal of day.meals) {
        const { data: mealData, error: mealError } = await supabase
          .from("meals")
          .insert({
            daily_meal_plan_id: dailyPlan.id,
            meal_type: meal.meal_type,
            meal_time: meal.time,
            meal_name: meal.meal_name,
            total_meal_calories: Math.round(meal.total_meal_calories || 0),
            cooking_time: meal.cooking_time,
            difficulty_level: meal.difficulty_level,
            notes: meal.notes,
          })
          .select()
          .single();

        if (mealError) throw mealError;

        // Save food items
        if (meal.food_items && Array.isArray(meal.food_items)) {
          const foodItems = meal.food_items.map((item) => ({
            meal_id: mealData.id,
            item_name: item.item,
            quantity: item.quantity,
            calories: parseFloat(item.calories || 0),
            protein: parseFloat(item.protein || 0),
            carbs: parseFloat(item.carbs || 0),
            fats: parseFloat(item.fats || 0),
          }));

          const { error: foodError } = await supabase
            .from("food_items")
            .insert(foodItems);

          if (foodError) console.error("Food items error:", foodError);
        }

        // Save ingredients
        if (meal.ingredients && Array.isArray(meal.ingredients)) {
          const ingredients = meal.ingredients.map((ing) => ({
            meal_id: mealData.id,
            ingredient_name: ing.ingredient,
            quantity: ing.quantity,
            unit: ing.unit,
          }));

          const { error: ingError } = await supabase
            .from("ingredients")
            .insert(ingredients);

          if (ingError) console.error("Ingredients error:", ingError);
        }

        // Save recipe steps
        if (meal.recipe_steps && Array.isArray(meal.recipe_steps)) {
          const steps = meal.recipe_steps.map((step) => ({
            meal_id: mealData.id,
            step_number: parseInt(step.step_number || 0),
            instruction: step.instruction,
          }));

          const { error: stepsError } = await supabase
            .from("recipe_steps")
            .insert(steps);

          if (stepsError) console.error("Recipe steps error:", stepsError);
        }
      }
    }

    // Save snack options
    if (
      dietPlanData.snack_options &&
      Array.isArray(dietPlanData.snack_options)
    ) {
      const snacks = dietPlanData.snack_options.map((snack) => ({
        diet_plan_id: dietPlan.id,
        snack_name: snack.snack_name,
        ingredients: snack.ingredients,
        calories: Math.round(snack.calories || 0),
        protein: parseFloat(snack.protein || 0),
      }));

      const { error: snacksError } = await supabase
        .from("snack_options")
        .insert(snacks);

      if (snacksError) console.error("Snacks error:", snacksError);
    }

    // Save supplement recommendations
    if (
      dietPlanData.supplement_recommendations &&
      Array.isArray(dietPlanData.supplement_recommendations)
    ) {
      const supplements = dietPlanData.supplement_recommendations.map(
        (supp) => ({
          diet_plan_id: dietPlan.id,
          supplement_name: supp.supplement_name,
          dosage: supp.dosage,
          timing: supp.timing,
          benefit: supp.benefit,
        })
      );

      const { error: suppsError } = await supabase
        .from("supplement_recommendations")
        .insert(supplements);

      if (suppsError) console.error("Supplements error:", suppsError);
    }

    // Save nutrition tips
    if (
      dietPlanData.nutrition_tips &&
      Array.isArray(dietPlanData.nutrition_tips)
    ) {
      const tips = dietPlanData.nutrition_tips.map((tip) => ({
        diet_plan_id: dietPlan.id,
        tip: tip,
      }));

      const { error: tipsError } = await supabase
        .from("nutrition_tips")
        .insert(tips);

      if (tipsError) console.error("Nutrition tips error:", tipsError);
    }

    // Initialize hydration tracking
    const { error: hydrationError } = await supabase
      .from("hydration_tracking")
      .insert({
        user_id: userId,
        date: startDate.toISOString().split("T")[0],
        target_liters: parseFloat(
          dietPlanData.hydration_guidelines?.daily_water_liters || 2.5
        ),
        consumed_liters: 0,
        water_intake_schedule:
          dietPlanData.hydration_guidelines?.water_intake_schedule || {},
      });

    if (hydrationError) console.error("Hydration error:", hydrationError);

    return { data: dietPlan, error: null };
  } catch (error) {
    console.error("Generate diet plan error:", error);
    return { data: null, error };
  }
};

/**
 * Get active diet plan
 */
export const getActiveDietPlan = async (userId) => {
  try {
    const { data, error } = await supabase
      .from("diet_plans")
      .select(
        `
        *,
        daily_meal_plans (
          *,
          meals (
            *,
            food_items (*),
            ingredients (*),
            recipe_steps (*)
          )
        ),
        snack_options (*),
        supplement_recommendations (*),
        nutrition_tips (*)
      `
      )
      .eq("user_id", userId)
      .eq("is_active", true)
      .single();

    if (error) throw error;
    return { data, error: null };
  } catch (error) {
    console.error("Get active diet plan error:", error);
    return { data: null, error };
  }
};

/**
 * Get diet plan by ID
 */
export const getDietPlanById = async (planId) => {
  try {
    const { data, error } = await supabase
      .from("diet_plans")
      .select(
        `
        *,
        daily_meal_plans (
          *,
          meals (
            *,
            food_items (*),
            ingredients (*),
            recipe_steps (*)
          )
        )
      `
      )
      .eq("id", planId)
      .single();

    if (error) throw error;
    return { data, error: null };
  } catch (error) {
    console.error("Get diet plan error:", error);
    return { data: null, error };
  }
};

/**
 * Mark meal as completed
 */
export const markMealCompleted = async (
  userId,
  mealId,
  rating = null,
  feedback = null
) => {
  try {
    // Update meal completion status
    await supabase
      .from("meals")
      .update({ is_completed: true })
      .eq("id", mealId);

    // Log completion
    const { data, error } = await supabase
      .from("meal_completion_log")
      .insert({
        user_id: userId,
        meal_id: mealId,
        rating,
        feedback,
      })
      .select()
      .single();

    if (error) throw error;
    return { data, error: null };
  } catch (error) {
    console.error("Mark meal completed error:", error);
    return { data: null, error };
  }
};

// ============================================
// WEIGHT TRACKING FUNCTIONS
// ============================================

/**
 * Add weight entry
 */
export const addWeightEntry = async (
  userId,
  weight,
  date = new Date(),
  notes = null
) => {
  try {
    const { data, error } = await supabase
      .from("weight_tracking")
      .insert({
        user_id: userId,
        weight,
        date: date.toISOString().split("T")[0],
        notes,
      })
      .select()
      .single();

    if (error) throw error;
    return { data, error: null };
  } catch (error) {
    console.error("Add weight entry error:", error);
    return { data: null, error };
  }
};

/**
 * Get weight history
 */
export const getWeightHistory = async (userId, limit = 30) => {
  try {
    const { data, error } = await supabase
      .from("weight_tracking")
      .select("*")
      .eq("user_id", userId)
      .order("date", { ascending: false })
      .limit(limit);

    if (error) throw error;
    return { data, error: null };
  } catch (error) {
    console.error("Get weight history error:", error);
    return { data: null, error };
  }
};

// ============================================
// HYDRATION TRACKING FUNCTIONS
// ============================================

/**
 * Update hydration for today
 */
export const updateHydration = async (userId, consumedLiters) => {
  try {
    const today = new Date().toISOString().split("T")[0];

    const { data, error } = await supabase
      .from("hydration_tracking")
      .upsert({
        user_id: userId,
        date: today,
        consumed_liters: consumedLiters,
      })
      .select()
      .single();

    if (error) throw error;
    return { data, error: null };
  } catch (error) {
    console.error("Update hydration error:", error);
    return { data: null, error };
  }
};

/**
 * Get today's hydration
 */
export const getTodayHydration = async (userId) => {
  try {
    const today = new Date().toISOString().split("T")[0];

    const { data, error } = await supabase
      .from("hydration_tracking")
      .select("*")
      .eq("user_id", userId)
      .eq("date", today)
      .single();

    if (error && error.code !== "PGRST116") throw error;
    return { data, error: null };
  } catch (error) {
    console.error("Get hydration error:", error);
    return { data: null, error };
  }
};

export default supabase;
