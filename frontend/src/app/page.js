"use client";
import React, { useState, useEffect } from "react";
import {
  ChevronDown,
  Brain,
  Database,
  Zap,
  Shield,
  Users,
  ArrowRight,
  Check,
  Github,
  Cloud,
  Activity,
  Target,
  Heart,
  TrendingUp,
} from "lucide-react";

export default function DietRecommendationLanding() {
  const [isVisible, setIsVisible] = useState(false);
  const [activeFeature, setActiveFeature] = useState(0);

  useEffect(() => {
    setIsVisible(true);
    const interval = setInterval(() => {
      setActiveFeature((prev) => (prev + 1) % 3);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  const features = [
    {
      icon: Brain,
      title: "AI-Powered Recommendations",
      description:
        "Machine learning algorithms analyze your unique profile to create personalized nutrition plans",
      color: "from-purple-500 to-pink-500",
    },
    {
      icon: Database,
      title: "Secure Data Management",
      description:
        "Supabase-powered backend ensures your health data is stored securely and accessed efficiently",
      color: "from-blue-500 to-cyan-500",
    },
    {
      icon: Zap,
      title: "Real-time Processing",
      description:
        "FastAPI and Flask deliver instant diet recommendations through optimized ML model deployment",
      color: "from-green-500 to-teal-500",
    },
  ];

  const techStack = [
    { name: "Next.js", description: "Modern React framework" },
    { name: "Supabase", description: "Backend & Database" },
    { name: "GitHub Actions", description: "CI/CD Pipeline" },
    { name: "Vercel", description: "Deployment Platform" },
    { name: "Flask/FastAPI", description: "ML Model APIs" },
    { name: "Render", description: "Cloud Hosting" },
  ];

  const benefits = [
    "Personalized nutrition based on your unique profile",
    "Evidence-based recommendations from ML algorithms",
    "Secure health data management",
    "Real-time diet adjustments",
    "Scalable DevOps infrastructure",
    "Continuous system improvements",
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-black/20 backdrop-blur-lg border-b border-white/10 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                <Heart className="w-4 h-4 text-white" />
              </div>
              <span className="text-xl font-bold text-white">NutriAI</span>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <a
                href="#features"
                className="text-gray-300 hover:text-white transition-colors"
              >
                Features
              </a>
              <a
                href="#technology"
                className="text-gray-300 hover:text-white transition-colors"
              >
                Technology
              </a>
              <a
                href="#benefits"
                className="text-gray-300 hover:text-white transition-colors"
              >
                Benefits
              </a>
              <button className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-2 rounded-full hover:from-purple-600 hover:to-pink-600 transition-all transform hover:scale-105">
                Get Started
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-24 pb-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div
            className={`text-center transition-all duration-1000 ${
              isVisible
                ? "opacity-100 translate-y-0"
                : "opacity-0 translate-y-10"
            }`}
          >
            <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
              <span className="bg-gradient-to-r from-purple-400 via-pink-400 to-cyan-400 bg-clip-text text-transparent">
                Personalized
              </span>
              <br />
              <span className="text-white">Diet Intelligence</span>
            </h1>
            <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
              Revolutionize your nutrition journey with AI-powered
              recommendations tailored to your unique health profile, goals, and
              preferences. Built with cutting-edge DevOps practices for
              scalable, secure, and intelligent diet guidance.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
              <button className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-8 py-4 rounded-full text-lg font-semibold hover:from-purple-600 hover:to-pink-600 transition-all transform hover:scale-105 shadow-2xl">
                Start Your Journey
                <ArrowRight className="inline-block ml-2 w-5 h-5" />
              </button>
              <button className="border border-white/30 text-white px-8 py-4 rounded-full text-lg font-semibold hover:bg-white/10 transition-all backdrop-blur-sm">
                View Demo
              </button>
            </div>
          </div>

          {/* Animated Feature Cards */}
          <div className="grid md:grid-cols-3 gap-8 mt-16">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div
                  key={index}
                  className={`relative p-8 rounded-2xl backdrop-blur-lg border border-white/10 transition-all duration-500 ${
                    activeFeature === index
                      ? "bg-white/10 scale-105"
                      : "bg-white/5"
                  }`}
                >
                  <div
                    className={`w-16 h-16 bg-gradient-to-r ${feature.color} rounded-2xl flex items-center justify-center mb-6`}
                  >
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-2xl font-bold text-white mb-4">
                    {feature.title}
                  </h3>
                  <p className="text-gray-300 leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Technology Stack */}
      <section
        id="technology"
        className="py-20 px-4 sm:px-6 lg:px-8 bg-black/20"
      >
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              <span className="bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
                Enterprise-Grade
              </span>{" "}
              Technology Stack
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Built with modern DevOps practices ensuring scalability, security,
              and continuous delivery
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {techStack.map((tech, index) => (
              <div
                key={index}
                className="group relative p-6 bg-white/5 backdrop-blur-lg rounded-xl border border-white/10 hover:bg-white/10 transition-all hover:scale-105"
              >
                <div className="flex items-center space-x-3 mb-3">
                  <div className="w-3 h-3 bg-gradient-to-r from-green-400 to-cyan-400 rounded-full"></div>
                  <h3 className="text-lg font-semibold text-white">
                    {tech.name}
                  </h3>
                </div>
                <p className="text-gray-400 text-sm">{tech.description}</p>
                <div className="absolute inset-0 bg-gradient-to-r from-purple-500/10 to-pink-500/10 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
              </div>
            ))}
          </div>

          {/* DevOps Pipeline Visualization */}
          <div className="mt-16 p-8 bg-gradient-to-r from-slate-800/50 to-slate-900/50 rounded-2xl border border-white/10">
            <h3 className="text-2xl font-bold text-white mb-6 text-center">
              DevOps Pipeline
            </h3>
            <div className="flex flex-wrap justify-center items-center gap-4 text-sm">
              <div className="flex items-center space-x-2 bg-white/10 px-4 py-2 rounded-full">
                <Github className="w-4 h-4 text-white" />
                <span className="text-white">GitHub</span>
              </div>
              <ArrowRight className="w-4 h-4 text-gray-400" />
              <div className="flex items-center space-x-2 bg-blue-500/20 px-4 py-2 rounded-full">
                <Zap className="w-4 h-4 text-blue-400" />
                <span className="text-blue-400">GitHub Actions</span>
              </div>
              <ArrowRight className="w-4 h-4 text-gray-400" />
              <div className="flex items-center space-x-2 bg-green-500/20 px-4 py-2 rounded-full">
                <Cloud className="w-4 h-4 text-green-400" />
                <span className="text-green-400">Vercel Deploy</span>
              </div>
              <ArrowRight className="w-4 h-4 text-gray-400" />
              <div className="flex items-center space-x-2 bg-purple-500/20 px-4 py-2 rounded-full">
                <Activity className="w-4 h-4 text-purple-400" />
                <span className="text-purple-400">Production</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section id="benefits" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-4xl md:text-5xl font-bold text-white mb-8">
                Transform Your{" "}
                <span className="bg-gradient-to-r from-green-400 to-cyan-400 bg-clip-text text-transparent">
                  Health Journey
                </span>
              </h2>
              <p className="text-xl text-gray-300 mb-8 leading-relaxed">
                Experience the power of personalized nutrition backed by machine
                learning, secure data management, and continuous system
                optimization.
              </p>
              <div className="space-y-4">
                {benefits.map((benefit, index) => (
                  <div key={index} className="flex items-center space-x-3">
                    <div className="w-6 h-6 bg-gradient-to-r from-green-400 to-cyan-400 rounded-full flex items-center justify-center flex-shrink-0">
                      <Check className="w-3 h-3 text-white" />
                    </div>
                    <span className="text-gray-300">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="relative">
              <div className="bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-3xl p-8 backdrop-blur-lg border border-white/10">
                <div className="grid grid-cols-2 gap-6">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-white mb-2">
                      97%
                    </div>
                    <div className="text-sm text-gray-400">
                      User Satisfaction
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-white mb-2">
                      24/7
                    </div>
                    <div className="text-sm text-gray-400">AI Availability</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-white mb-2">
                      100%
                    </div>
                    <div className="text-sm text-gray-400">Data Security</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-white mb-2">∞</div>
                    <div className="text-sm text-gray-400">Scalability</div>
                  </div>
                </div>
              </div>
              <div className="absolute -top-4 -right-4 w-24 h-24 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full opacity-20"></div>
              <div className="absolute -bottom-4 -left-4 w-16 h-16 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full opacity-20"></div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-purple-900/50 to-pink-900/50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Ready to Revolutionize Your Nutrition?
          </h2>
          <p className="text-xl text-gray-300 mb-8">
            Join thousands of users who have transformed their health with
            AI-powered personalized diet recommendations.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-10 py-4 rounded-full text-lg font-semibold hover:from-purple-600 hover:to-pink-600 transition-all transform hover:scale-105 shadow-2xl">
              Start Free Trial
              <ArrowRight className="inline-block ml-2 w-5 h-5" />
            </button>
            <button className="border border-white/30 text-white px-10 py-4 rounded-full text-lg font-semibold hover:bg-white/10 transition-all backdrop-blur-sm">
              Contact Sales
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 sm:px-6 lg:px-8 bg-black/40 border-t border-white/10">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                <Heart className="w-4 h-4 text-white" />
              </div>
              <span className="text-xl font-bold text-white">NutriAI</span>
            </div>
            <div className="text-center md:text-right">
              <p className="text-gray-400 mb-2">
                Powered by Machine Learning & DevOps Excellence
              </p>
              <div className="flex justify-center md:justify-end space-x-6 text-sm text-gray-500">
                <span>Built with Next.js</span>
                <span>•</span>
                <span>Deployed on Vercel</span>
                <span>•</span>
                <span>Secured by Supabase</span>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
