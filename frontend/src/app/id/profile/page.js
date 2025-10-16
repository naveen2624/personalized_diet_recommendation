"use client";
import { useState } from "react";
import { Camera, Edit2, X, Plus, Check } from "lucide-react";

export default function DietProfile() {
  const [isEditing, setIsEditing] = useState(false);
  const [profile, setProfile] = useState({
    name: "Alex Johnson",
    height: 170,
    weight: 68,
    profilePic: null,
    dietPreference: "vegetarian",
    restrictions: ["onion", "spinach"],
    goal: "weightloss",
  });

  const [tempProfile, setTempProfile] = useState({ ...profile });
  const [newRestriction, setNewRestriction] = useState("");
  const [showRestrictionInput, setShowRestrictionInput] = useState(false);

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
      !tempProfile.restrictions.includes(newRestriction.trim().toLowerCase())
    ) {
      setTempProfile({
        ...tempProfile,
        restrictions: [
          ...tempProfile.restrictions,
          newRestriction.trim().toLowerCase(),
        ],
      });
      setNewRestriction("");
      setShowRestrictionInput(false);
    }
  };

  const removeRestriction = (restriction) => {
    setTempProfile({
      ...tempProfile,
      restrictions: tempProfile.restrictions.filter((r) => r !== restriction),
    });
  };

  const handleSave = () => {
    setProfile({ ...tempProfile });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setTempProfile({ ...profile });
    setIsEditing(false);
    setShowRestrictionInput(false);
    setNewRestriction("");
  };

  const currentData = isEditing ? tempProfile : profile;

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
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-all"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                className="flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-all shadow-md"
              >
                <Check size={18} />
                Save
              </button>
            </div>
          )}
        </div>

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
                      {currentData.name.charAt(0)}
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
                />
              ) : (
                <h2 className="mt-4 text-2xl md:text-3xl font-bold text-white">
                  {currentData.name}
                </h2>
              )}
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
                    value={currentData.height}
                    onChange={(e) =>
                      setTempProfile({
                        ...tempProfile,
                        height: parseInt(e.target.value),
                      })
                    }
                    className="w-full text-2xl font-bold text-emerald-900 bg-white rounded-lg px-3 py-2 border-2 border-emerald-200 focus:outline-none focus:border-emerald-500"
                  />
                ) : (
                  <div className="text-2xl font-bold text-emerald-900">
                    {currentData.height}
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
                    value={currentData.weight}
                    onChange={(e) =>
                      setTempProfile({
                        ...tempProfile,
                        weight: parseInt(e.target.value),
                      })
                    }
                    className="w-full text-2xl font-bold text-emerald-900 bg-white rounded-lg px-3 py-2 border-2 border-emerald-200 focus:outline-none focus:border-emerald-500"
                  />
                ) : (
                  <div className="text-2xl font-bold text-emerald-900">
                    {currentData.weight}
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
                  {
                    dietPreferences.find(
                      (p) => p.value === currentData.dietPreference
                    )?.label
                  }
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
                  {goals.find((g) => g.value === currentData.goal)?.label}
                </div>
              )}
            </div>

            {/* Dietary Restrictions */}
            <div>
              <label className="text-sm text-emerald-700 font-semibold mb-3 block">
                Dietary Restrictions
              </label>
              <div className="flex flex-wrap gap-2">
                {currentData.restrictions.map((restriction) => (
                  <div
                    key={restriction}
                    className="inline-flex items-center gap-2 px-3 py-2 bg-red-50 text-red-700 rounded-lg border border-red-200"
                  >
                    <span className="font-medium capitalize">
                      {restriction}
                    </span>
                    {isEditing && (
                      <button
                        onClick={() => removeRestriction(restriction)}
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
              {currentData.restrictions.length === 0 && !isEditing && (
                <p className="text-gray-400 italic">No restrictions added</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
