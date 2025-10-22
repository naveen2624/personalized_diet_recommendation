"use client";
import { useState, useEffect } from "react";
import { Camera, Edit2, X, Plus, Check, Loader2 } from "lucide-react";
import {
  getCurrentUser,
  getUserProfile,
  updateUserProfile,
  getDietaryRestrictions,
  addDietaryRestriction,
  deleteDietaryRestriction,
} from "@/lib/supabase";

export default function DietProfile() {
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [userId, setUserId] = useState(null);
  const [profile, setProfile] = useState({
    name: "",
    email: "",
    height: 0,
    weight: 0,
    profilePic: null,
    dietPreference: "",
    goal: "",
  });
  const [restrictions, setRestrictions] = useState([]);
  const [tempProfile, setTempProfile] = useState({ ...profile });
  const [tempRestrictions, setTempRestrictions] = useState([]);
  const [newRestriction, setNewRestriction] = useState("");
  const [showRestrictionInput, setShowRestrictionInput] = useState(false);
  const [error, setError] = useState(null);

  const dietPreferences = [
    { value: "vegetarian", label: "Vegetarian" },
    { value: "non-veg", label: "Non-Vegetarian" },
    { value: "eggetarian", label: "Eggetarian" },
    { value: "vegan", label: "Vegan" },
  ];

  const goals = [
    { value: "weightloss", label: "Weight Loss" },
    { value: "weightgain", label: "Weight Gain" },
    { value: "musclegain", label: "Muscle Gain" },
    { value: "musclemaintain", label: "Muscle Maintain" },
    { value: "weightmaintain", label: "Weight Maintain" },
  ];

  // Load user data on mount
  useEffect(() => {
    loadUserData();
  }, []);

  const loadUserData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Get current user
      const { user, error: userError } = await getCurrentUser();
      if (userError) throw userError;
      if (!user) {
        setError("Please log in to view your profile");
        setLoading(false);
        return;
      }

      setUserId(user.id);

      // Get user profile
      const { data: profileData, error: profileError } = await getUserProfile(
        user.id
      );
      if (profileError) throw profileError;

      if (profileData) {
        const loadedProfile = {
          name: profileData.name || "",
          email: profileData.email || user.email,
          height: profileData.height || 0,
          weight: profileData.weight || 0,
          profilePic: profileData.profile_pic || null,
          dietPreference: profileData.diet_preference || "",
          goal: profileData.goal || "",
        };
        setProfile(loadedProfile);
        setTempProfile(loadedProfile);
      }

      // Get dietary restrictions
      const { data: restrictionsData, error: restrictionsError } =
        await getDietaryRestrictions(user.id);
      if (restrictionsError) throw restrictionsError;

      const loadedRestrictions =
        restrictionsData?.map((r) => ({
          id: r.id,
          name: r.restriction,
        })) || [];
      setRestrictions(loadedRestrictions);
      setTempRestrictions([...loadedRestrictions]);
    } catch (err) {
      console.error("Error loading user data:", err);
      setError(err.message || "Failed to load profile data");
    } finally {
      setLoading(false);
    }
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setTempProfile({ ...tempProfile, profilePic: reader.result });
      };
      reader.readAsDataURL(file);
    }
  };

  const addRestriction = () => {
    if (
      newRestriction.trim() &&
      !tempRestrictions.some(
        (r) => r.name === newRestriction.trim().toLowerCase()
      )
    ) {
      setTempRestrictions([
        ...tempRestrictions,
        { id: `temp-${Date.now()}`, name: newRestriction.trim().toLowerCase() },
      ]);
      setNewRestriction("");
      setShowRestrictionInput(false);
    }
  };

  const removeRestriction = (restrictionId) => {
    setTempRestrictions(tempRestrictions.filter((r) => r.id !== restrictionId));
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      setError(null);

      // Prepare update data with proper type conversions
      const updateData = {
        name: tempProfile.name || null,
        email: tempProfile.email || null,
        height:
          tempProfile.height && tempProfile.height > 0
            ? parseFloat(tempProfile.height)
            : null,
        weight:
          tempProfile.weight && tempProfile.weight > 0
            ? parseFloat(tempProfile.weight)
            : null,
        profile_pic: tempProfile.profilePic || null,
        diet_preference: tempProfile.dietPreference || null,
        goal: tempProfile.goal || null,
      };

      console.log("Saving profile for user:", userId);
      console.log("Update data:", updateData);

      // Update user profile
      const { data: updatedProfile, error: updateError } =
        await updateUserProfile(userId, updateData);

      if (updateError) {
        console.error("Update error:", updateError);
        throw new Error(updateError.message || "Failed to update profile");
      }

      console.log("Profile updated successfully:", updatedProfile);

      // Handle dietary restrictions changes
      // Find deleted restrictions
      const deletedRestrictions = restrictions.filter(
        (r) => !tempRestrictions.some((tr) => tr.id === r.id)
      );

      // Find new restrictions
      const newRestrictions = tempRestrictions.filter((tr) =>
        tr.id.startsWith("temp-")
      );

      // Delete removed restrictions
      for (const restriction of deletedRestrictions) {
        const { error } = await deleteDietaryRestriction(restriction.id);
        if (error) {
          console.error("Error deleting restriction:", error);
        }
      }

      // Add new restrictions
      const addedRestrictions = [];
      for (const restriction of newRestrictions) {
        const { data, error } = await addDietaryRestriction(
          userId,
          restriction.name,
          "dislike"
        );
        if (!error && data) {
          addedRestrictions.push({ id: data.id, name: data.restriction });
        } else if (error) {
          console.error("Error adding restriction:", error);
        }
      }

      // Update local state with real IDs
      const updatedRestrictions = [
        ...tempRestrictions.filter((tr) => !tr.id.startsWith("temp-")),
        ...addedRestrictions,
      ];

      setProfile({ ...tempProfile });
      setRestrictions(updatedRestrictions);
      setTempRestrictions(updatedRestrictions);
      setIsEditing(false);
      setError(null); // Clear any previous errors
    } catch (err) {
      console.error("Error saving profile:", err);
      setError(err.message || "Failed to save profile");
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setTempProfile({ ...profile });
    setTempRestrictions([...restrictions]);
    setIsEditing(false);
    setShowRestrictionInput(false);
    setNewRestriction("");
    setError(null);
  };

  const currentData = isEditing ? tempProfile : profile;
  const currentRestrictions = isEditing ? tempRestrictions : restrictions;

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-green-50 to-teal-50 flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="w-12 h-12 text-emerald-600 animate-spin" />
          <p className="text-emerald-700 font-medium">
            Loading your profile...
          </p>
        </div>
      </div>
    );
  }

  if (error && !userId) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-green-50 to-teal-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full text-center">
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <X className="w-8 h-8 text-red-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Authentication Required
          </h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={() => (window.location.href = "/login")}
            className="px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-all font-medium"
          >
            Go to Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-green-50 to-teal-50 p-4 md:p-8">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl md:text-3xl font-bold text-emerald-900">
            My Profile
          </h1>
          {!isEditing ? (
            <button
              onClick={() => setIsEditing(true)}
              className="flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-all shadow-md hover:shadow-lg"
            >
              <Edit2 size={18} />
              <span className="hidden sm:inline">Edit</span>
            </button>
          ) : (
            <div className="flex gap-2">
              <button
                onClick={handleCancel}
                disabled={saving}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-all disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                disabled={saving}
                className="flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-all shadow-md disabled:opacity-50"
              >
                {saving ? (
                  <>
                    <Loader2 size={18} className="animate-spin" />
                    Saving...
                  </>
                ) : (
                  <>
                    <Check size={18} />
                    Save
                  </>
                )}
              </button>
            </div>
          )}
        </div>

        {/* Error Message */}
        {error && userId && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
            <X className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
            <p className="text-red-800 text-sm">{error}</p>
          </div>
        )}

        {/* Profile Card */}
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          {/* Profile Header */}
          <div className="bg-gradient-to-r from-emerald-600 to-teal-600 p-6 md:p-8">
            <div className="flex flex-col items-center">
              <div className="relative">
                <div className="w-28 h-28 md:w-32 md:h-32 rounded-full bg-white/20 backdrop-blur-sm border-4 border-white/30 flex items-center justify-center overflow-hidden">
                  {currentData.profilePic ? (
                    <img
                      src={currentData.profilePic}
                      alt="Profile"
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <span className="text-5xl text-white font-bold">
                      {currentData.name
                        ? currentData.name.charAt(0).toUpperCase()
                        : "?"}
                    </span>
                  )}
                </div>
                {isEditing && (
                  <label className="absolute bottom-0 right-0 w-10 h-10 bg-emerald-500 rounded-full flex items-center justify-center cursor-pointer hover:bg-emerald-400 transition-all shadow-lg">
                    <Camera size={20} className="text-white" />
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImageUpload}
                      className="hidden"
                    />
                  </label>
                )}
              </div>
              {isEditing ? (
                <input
                  type="text"
                  value={currentData.name}
                  onChange={(e) =>
                    setTempProfile({ ...tempProfile, name: e.target.value })
                  }
                  className="mt-4 text-2xl font-bold text-center bg-white/20 backdrop-blur-sm text-white px-4 py-2 rounded-lg border-2 border-white/30 focus:outline-none focus:border-white"
                  placeholder="Your Name"
                />
              ) : (
                <h2 className="mt-4 text-2xl md:text-3xl font-bold text-white">
                  {currentData.name || "User"}
                </h2>
              )}
              <p className="text-sm text-white/80">
                {currentData.email || "user@example.com"}
              </p>
            </div>
          </div>

          {/* Profile Details */}
          <div className="p-6 md:p-8 space-y-6">
            {/* Physical Stats */}
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-emerald-50 rounded-xl p-4 border-2 border-emerald-100">
                <label className="text-sm text-emerald-700 font-medium mb-2 block">
                  Height (cm)
                </label>
                {isEditing ? (
                  <input
                    type="number"
                    value={currentData.height || ""}
                    onChange={(e) =>
                      setTempProfile({
                        ...tempProfile,
                        height: parseFloat(e.target.value) || 0,
                      })
                    }
                    className="w-full text-2xl font-bold text-emerald-900 bg-white rounded-lg px-3 py-2 border-2 border-emerald-200 focus:outline-none focus:border-emerald-500"
                    placeholder="170"
                  />
                ) : (
                  <div className="text-2xl font-bold text-emerald-900">
                    {currentData.height || "-"}
                  </div>
                )}
              </div>
              <div className="bg-emerald-50 rounded-xl p-4 border-2 border-emerald-100">
                <label className="text-sm text-emerald-700 font-medium mb-2 block">
                  Weight (kg)
                </label>
                {isEditing ? (
                  <input
                    type="number"
                    value={currentData.weight || ""}
                    onChange={(e) =>
                      setTempProfile({
                        ...tempProfile,
                        weight: parseFloat(e.target.value) || 0,
                      })
                    }
                    className="w-full text-2xl font-bold text-emerald-900 bg-white rounded-lg px-3 py-2 border-2 border-emerald-200 focus:outline-none focus:border-emerald-500"
                    placeholder="68"
                  />
                ) : (
                  <div className="text-2xl font-bold text-emerald-900">
                    {currentData.weight || "-"}
                  </div>
                )}
              </div>
            </div>

            {/* Diet Preference */}
            <div>
              <label className="text-sm text-emerald-700 font-semibold mb-3 block">
                Diet Preference
              </label>
              {isEditing ? (
                <div className="grid grid-cols-2 gap-2">
                  {dietPreferences.map((pref) => (
                    <button
                      key={pref.value}
                      onClick={() =>
                        setTempProfile({
                          ...tempProfile,
                          dietPreference: pref.value,
                        })
                      }
                      className={`p-3 rounded-lg font-medium transition-all ${
                        currentData.dietPreference === pref.value
                          ? "bg-emerald-600 text-white shadow-md"
                          : "bg-emerald-50 text-emerald-700 hover:bg-emerald-100"
                      }`}
                    >
                      {pref.label}
                    </button>
                  ))}
                </div>
              ) : (
                <div className="inline-block px-4 py-2 bg-emerald-100 text-emerald-800 rounded-lg font-medium">
                  {dietPreferences.find(
                    (p) => p.value === currentData.dietPreference
                  )?.label || "Not set"}
                </div>
              )}
            </div>

            {/* Goal */}
            <div>
              <label className="text-sm text-emerald-700 font-semibold mb-3 block">
                Goal
              </label>
              {isEditing ? (
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                  {goals.map((goal) => (
                    <button
                      key={goal.value}
                      onClick={() =>
                        setTempProfile({ ...tempProfile, goal: goal.value })
                      }
                      className={`p-3 rounded-lg font-medium text-sm transition-all ${
                        currentData.goal === goal.value
                          ? "bg-teal-600 text-white shadow-md"
                          : "bg-teal-50 text-teal-700 hover:bg-teal-100"
                      }`}
                    >
                      {goal.label}
                    </button>
                  ))}
                </div>
              ) : (
                <div className="inline-block px-4 py-2 bg-teal-100 text-teal-800 rounded-lg font-medium">
                  {goals.find((g) => g.value === currentData.goal)?.label ||
                    "Not set"}
                </div>
              )}
            </div>

            {/* Dietary Restrictions */}
            <div>
              <label className="text-sm text-emerald-700 font-semibold mb-3 block">
                Dietary Restrictions
              </label>
              <div className="flex flex-wrap gap-2">
                {currentRestrictions.map((restriction) => (
                  <div
                    key={restriction.id}
                    className="inline-flex items-center gap-2 px-3 py-2 bg-red-50 text-red-700 rounded-lg border border-red-200"
                  >
                    <span className="font-medium capitalize">
                      {restriction.name}
                    </span>
                    {isEditing && (
                      <button
                        onClick={() => removeRestriction(restriction.id)}
                        className="hover:bg-red-200 rounded-full p-1 transition-colors"
                      >
                        <X size={14} />
                      </button>
                    )}
                  </div>
                ))}
                {isEditing && (
                  <>
                    {showRestrictionInput ? (
                      <div className="flex gap-2 w-full sm:w-auto">
                        <input
                          type="text"
                          value={newRestriction}
                          onChange={(e) => setNewRestriction(e.target.value)}
                          onKeyPress={(e) =>
                            e.key === "Enter" && addRestriction()
                          }
                          placeholder="Add restriction..."
                          className="px-3 py-2 border-2 border-emerald-300 rounded-lg focus:outline-none focus:border-emerald-500 flex-1"
                          autoFocus
                        />
                        <button
                          onClick={addRestriction}
                          className="px-3 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
                        >
                          <Check size={18} />
                        </button>
                      </div>
                    ) : (
                      <button
                        onClick={() => setShowRestrictionInput(true)}
                        className="inline-flex items-center gap-2 px-3 py-2 border-2 border-dashed border-emerald-300 text-emerald-600 rounded-lg hover:bg-emerald-50 transition-colors"
                      >
                        <Plus size={16} />
                        <span className="font-medium">Add Restriction</span>
                      </button>
                    )}
                  </>
                )}
              </div>
              {currentRestrictions.length === 0 && !isEditing && (
                <p className="text-gray-400 italic">No restrictions added</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
