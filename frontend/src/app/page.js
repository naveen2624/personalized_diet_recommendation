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
  Link as LinkIcon,
  Container,
  Settings,
  BarChart3,
  Lock,
  GitBranch,
  Play,
} from "lucide-react";

export default function DietRecommendationLanding() {
  const [isVisible, setIsVisible] = useState(false);
  const [activeFeature, setActiveFeature] = useState(0);
  const [activeDevOps, setActiveDevOps] = useState(0);

  useEffect(() => {
    setIsVisible(true);
    const interval = setInterval(() => {
      setActiveFeature((prev) => (prev + 1) % 3);
    }, 4000);

    const devopsInterval = setInterval(() => {
      setActiveDevOps((prev) => (prev + 1) % 7);
    }, 2000);

    return () => {
      clearInterval(interval);
      clearInterval(devopsInterval);
    };
  }, []);

  const features = [
    {
      icon: Brain,
      title: "AI-Powered Recommendations",
      description:
        "Machine learning algorithms analyze your unique profile to create personalized nutrition plans",
      color: "from-green-500 to-emerald-500",
    },
    {
      icon: Database,
      title: "Secure Data Management",
      description:
        "Supabase-powered backend ensures your health data is stored securely with built-in authentication",
      color: "from-teal-500 to-cyan-500",
    },
    {
      icon: Zap,
      title: "Real-time Processing",
      description:
        "FastAPI and Flask deliver instant diet recommendations through optimized ML model deployment",
      color: "from-lime-500 to-green-500",
    },
  ];

  const devopsPipeline = [
    {
      icon: Github,
      name: "GitHub",
      description: "Developer pushes code",
      color: "bg-gray-700",
      textColor: "text-white",
    },
    {
      icon: Settings,
      name: "Jenkins",
      description: "Pipeline triggers → build + test",
      color: "bg-red-600",
      textColor: "text-white",
    },
    {
      icon: Container,
      name: "Docker",
      description: "Builds image → push to ECR",
      color: "bg-blue-500",
      textColor: "text-white",
    },
    {
      icon: Cloud,
      name: "Terraform",
      description: "Provisions infrastructure",
      color: "bg-purple-600",
      textColor: "text-white",
    },
    {
      icon: Settings,
      name: "Ansible",
      description: "Configures EC2 / K8s nodes",
      color: "bg-red-500",
      textColor: "text-white",
    },
    {
      icon: Play,
      name: "Deploy",
      description: "EKS or Beanstalk",
      color: "bg-orange-500",
      textColor: "text-white",
    },
    {
      icon: Activity,
      name: "Monitor",
      description: "CloudWatch, Prometheus, Grafana",
      color: "bg-green-600",
      textColor: "text-white",
    },
  ];

  const techStack = [
    {
      icon: Github,
      name: "GitHub",
      description: "Version Control & Collaboration",
      category: "Source Control",
    },
    {
      icon: Settings,
      name: "Jenkins",
      description: "CI/CD Automation",
      category: "Build",
    },
    {
      icon: Container,
      name: "Docker",
      description: "Containerization",
      category: "Container",
    },
    {
      icon: Cloud,
      name: "AWS ECR",
      description: "Container Registry",
      category: "Registry",
    },
    {
      icon: Settings,
      name: "Terraform",
      description: "Infrastructure as Code",
      category: "IaC",
    },
    {
      icon: Settings,
      name: "Ansible",
      description: "Configuration Management",
      category: "Config",
    },
    {
      icon: Cloud,
      name: "AWS EKS",
      description: "Kubernetes Orchestration",
      category: "Orchestration",
    },
    {
      icon: Cloud,
      name: "Elastic Beanstalk",
      description: "Platform as a Service",
      category: "PaaS",
    },
    {
      icon: Activity,
      name: "CloudWatch",
      description: "AWS Native Monitoring",
      category: "Monitoring",
    },
    {
      icon: BarChart3,
      name: "Prometheus",
      description: "Metrics & Alerting",
      category: "Monitoring",
    },
    {
      icon: BarChart3,
      name: "Grafana",
      description: "Visualization Dashboard",
      category: "Monitoring",
    },
    {
      icon: Database,
      name: "Supabase",
      description: "PostgreSQL Database",
      category: "Database",
    },
    {
      icon: Lock,
      name: "Supabase Auth",
      description: "Authentication & Authorization",
      category: "Auth",
    },
  ];

  const benefits = [
    "Personalized nutrition based on your unique profile",
    "Evidence-based recommendations from ML algorithms",
    "Secure health data with Supabase Auth",
    "Real-time diet adjustments",
    "Enterprise-grade DevOps infrastructure",
    "Continuous monitoring and improvements",
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-green-900 to-slate-900">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-black/20 backdrop-blur-lg border-b border-white/10 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg flex items-center justify-center">
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
                href="#devops"
                className="text-gray-300 hover:text-white transition-colors"
              >
                DevOps
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
              <a
                href="/auth"
                className="bg-gradient-to-r from-green-500 to-emerald-500 text-white px-6 py-2 rounded-full hover:from-green-600 hover:to-emerald-600 transition-all transform hover:scale-105 flex items-center space-x-2"
              >
                <Lock className="w-4 h-4" />
                <span>Login / Signup</span>
              </a>
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
              <span className="bg-gradient-to-r from-green-400 via-emerald-400 to-teal-400 bg-clip-text text-transparent">
                Personalized
              </span>
              <br />
              <span className="text-white">Diet Intelligence</span>
            </h1>
            <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
              Revolutionize your nutrition journey with AI-powered
              recommendations tailored to your unique health profile. Built with
              enterprise-grade DevOps practices for scalable, secure, and
              intelligent diet guidance.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
              <a
                href="/auth"
                className="bg-gradient-to-r from-green-500 to-emerald-500 text-white px-8 py-4 rounded-full text-lg font-semibold hover:from-green-600 hover:to-emerald-600 transition-all transform hover:scale-105 shadow-2xl inline-flex items-center justify-center"
              >
                Start Your Journey
                <ArrowRight className="inline-block ml-2 w-5 h-5" />
              </a>
              <button className="border border-white/30 text-white px-8 py-4 rounded-full text-lg font-semibold hover:bg-white/10 transition-all backdrop-blur-sm">
                View Demo
              </button>
            </div>
          </div>

          {/* Animated Feature Cards */}
          <div id="features" className="grid md:grid-cols-3 gap-8 mt-16">
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

      {/* DevOps Pipeline Section */}
      <section id="devops" className="py-20 px-4 sm:px-6 lg:px-8 bg-black/30">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              <span className="bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent">
                Enterprise DevOps
              </span>{" "}
              Pipeline
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Automated CI/CD pipeline with Infrastructure as Code, container
              orchestration, and comprehensive monitoring
            </p>
          </div>

          {/* Animated Pipeline Flow */}
          <div className="relative overflow-x-auto pb-8">
            <div className="flex items-center justify-center min-w-max px-4 space-x-4">
              {devopsPipeline.map((step, index) => {
                const Icon = step.icon;
                return (
                  <React.Fragment key={index}>
                    <div
                      className={`relative transition-all duration-500 ${
                        activeDevOps === index ? "scale-110 z-10" : "scale-100"
                      }`}
                    >
                      <div
                        className={`${step.color} ${
                          step.textColor
                        } p-6 rounded-2xl shadow-2xl min-w-[200px] border-2 ${
                          activeDevOps === index
                            ? "border-green-400"
                            : "border-transparent"
                        }`}
                      >
                        <div className="flex flex-col items-center text-center">
                          <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center mb-3">
                            <Icon className="w-6 h-6" />
                          </div>
                          <h3 className="text-lg font-bold mb-2">
                            {step.name}
                          </h3>
                          <p className="text-sm opacity-90">
                            {step.description}
                          </p>
                        </div>
                      </div>
                      {activeDevOps === index && (
                        <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-full">
                          <div className="h-1 bg-gradient-to-r from-green-400 to-emerald-400 rounded-full"></div>
                        </div>
                      )}
                    </div>
                    {index < devopsPipeline.length - 1 && (
                      <div className="flex items-center">
                        <ArrowRight
                          className={`w-8 h-8 transition-colors ${
                            activeDevOps === index
                              ? "text-green-400"
                              : "text-gray-600"
                          }`}
                        />
                      </div>
                    )}
                  </React.Fragment>
                );
              })}
            </div>
          </div>

          {/* Pipeline Steps Explanation */}
          <div className="mt-12 grid md:grid-cols-2 gap-6">
            <div className="bg-gradient-to-br from-green-900/30 to-emerald-900/30 p-6 rounded-2xl border border-green-500/20 backdrop-blur-lg">
              <h3 className="text-xl font-bold text-white mb-4 flex items-center">
                <GitBranch className="w-5 h-5 mr-2 text-green-400" />
                Continuous Integration
              </h3>
              <ul className="space-y-2 text-gray-300">
                <li className="flex items-start">
                  <Check className="w-4 h-4 mr-2 mt-1 text-green-400 flex-shrink-0" />
                  <span>GitHub triggers Jenkins pipeline on code push</span>
                </li>
                <li className="flex items-start">
                  <Check className="w-4 h-4 mr-2 mt-1 text-green-400 flex-shrink-0" />
                  <span>Automated testing and code quality checks</span>
                </li>
                <li className="flex items-start">
                  <Check className="w-4 h-4 mr-2 mt-1 text-green-400 flex-shrink-0" />
                  <span>Docker builds and pushes to AWS ECR</span>
                </li>
              </ul>
            </div>

            <div className="bg-gradient-to-br from-teal-900/30 to-cyan-900/30 p-6 rounded-2xl border border-teal-500/20 backdrop-blur-lg">
              <h3 className="text-xl font-bold text-white mb-4 flex items-center">
                <Cloud className="w-5 h-5 mr-2 text-teal-400" />
                Continuous Deployment
              </h3>
              <ul className="space-y-2 text-gray-300">
                <li className="flex items-start">
                  <Check className="w-4 h-4 mr-2 mt-1 text-teal-400 flex-shrink-0" />
                  <span>Terraform provisions AWS infrastructure</span>
                </li>
                <li className="flex items-start">
                  <Check className="w-4 h-4 mr-2 mt-1 text-teal-400 flex-shrink-0" />
                  <span>Ansible configures EC2 and Kubernetes nodes</span>
                </li>
                <li className="flex items-start">
                  <Check className="w-4 h-4 mr-2 mt-1 text-teal-400 flex-shrink-0" />
                  <span>Deploy to EKS or Elastic Beanstalk</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Monitoring Section */}
          <div className="mt-8 bg-gradient-to-br from-green-800/30 to-lime-900/30 p-8 rounded-2xl border border-green-500/30 backdrop-blur-lg">
            <h3 className="text-2xl font-bold text-white mb-6 flex items-center justify-center">
              <Activity className="w-6 h-6 mr-2 text-green-400" />
              Comprehensive Monitoring & Observability
            </h3>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="w-16 h-16 bg-orange-500/20 rounded-xl flex items-center justify-center mx-auto mb-3">
                  <Activity className="w-8 h-8 text-orange-400" />
                </div>
                <h4 className="text-lg font-semibold text-white mb-2">
                  CloudWatch
                </h4>
                <p className="text-sm text-gray-300">
                  AWS native monitoring, logs, and alerts
                </p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-red-500/20 rounded-xl flex items-center justify-center mx-auto mb-3">
                  <BarChart3 className="w-8 h-8 text-red-400" />
                </div>
                <h4 className="text-lg font-semibold text-white mb-2">
                  Prometheus
                </h4>
                <p className="text-sm text-gray-300">
                  Metrics collection and alerting system
                </p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-orange-600/20 rounded-xl flex items-center justify-center mx-auto mb-3">
                  <BarChart3 className="w-8 h-8 text-orange-500" />
                </div>
                <h4 className="text-lg font-semibold text-white mb-2">
                  Grafana
                </h4>
                <p className="text-sm text-gray-300">
                  Real-time visualization dashboards
                </p>
              </div>
            </div>
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
              <span className="bg-gradient-to-r from-teal-400 to-green-400 bg-clip-text text-transparent">
                Complete Technology
              </span>{" "}
              Stack
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Every tool in our DevOps arsenal working together seamlessly
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {techStack.map((tech, index) => {
              const Icon = tech.icon;
              return (
                <div
                  key={index}
                  className="group relative p-6 bg-white/5 backdrop-blur-lg rounded-xl border border-white/10 hover:bg-white/10 transition-all hover:scale-105"
                >
                  <div className="flex items-start space-x-3">
                    <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg flex items-center justify-center flex-shrink-0">
                      <Icon className="w-5 h-5 text-white" />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-lg font-semibold text-white">
                          {tech.name}
                        </h3>
                        <span className="text-xs px-2 py-1 bg-green-500/20 text-green-400 rounded-full">
                          {tech.category}
                        </span>
                      </div>
                      <p className="text-gray-400 text-sm">
                        {tech.description}
                      </p>
                    </div>
                  </div>
                  <div className="absolute inset-0 bg-gradient-to-r from-green-500/10 to-emerald-500/10 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
                </div>
              );
            })}
          </div>

          {/* Database & Auth Highlight */}
          <div className="mt-12 grid md:grid-cols-2 gap-8">
            <div className="bg-gradient-to-br from-green-900/40 to-teal-900/40 p-8 rounded-2xl border border-green-500/30">
              <div className="flex items-center mb-4">
                <Database className="w-8 h-8 text-green-400 mr-3" />
                <h3 className="text-2xl font-bold text-white">
                  Supabase Database
                </h3>
              </div>
              <p className="text-gray-300 mb-4">
                PostgreSQL-powered backend with real-time subscriptions, instant
                APIs, and automatic schema migrations
              </p>
              <div className="flex flex-wrap gap-2">
                <span className="px-3 py-1 bg-green-500/20 text-green-300 rounded-full text-sm">
                  PostgreSQL
                </span>
                <span className="px-3 py-1 bg-green-500/20 text-green-300 rounded-full text-sm">
                  Real-time
                </span>
                <span className="px-3 py-1 bg-green-500/20 text-green-300 rounded-full text-sm">
                  Auto APIs
                </span>
              </div>
            </div>

            <div className="bg-gradient-to-br from-emerald-900/40 to-teal-900/40 p-8 rounded-2xl border border-emerald-500/30">
              <div className="flex items-center mb-4">
                <Lock className="w-8 h-8 text-emerald-400 mr-3" />
                <h3 className="text-2xl font-bold text-white">Supabase Auth</h3>
              </div>
              <p className="text-gray-300 mb-4">
                Enterprise-grade authentication with social logins, MFA, and
                row-level security policies
              </p>
              <div className="flex flex-wrap gap-2">
                <span className="px-3 py-1 bg-emerald-500/20 text-emerald-300 rounded-full text-sm">
                  OAuth
                </span>
                <span className="px-3 py-1 bg-emerald-500/20 text-emerald-300 rounded-full text-sm">
                  MFA
                </span>
                <span className="px-3 py-1 bg-emerald-500/20 text-emerald-300 rounded-full text-sm">
                  RLS
                </span>
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
                <span className="bg-gradient-to-r from-green-400 to-teal-400 bg-clip-text text-transparent">
                  Health Journey
                </span>
              </h2>
              <p className="text-xl text-gray-300 mb-8 leading-relaxed">
                Experience the power of personalized nutrition backed by machine
                learning, secure authentication, and enterprise DevOps
                infrastructure.
              </p>
              <div className="space-y-4">
                {benefits.map((benefit, index) => (
                  <div key={index} className="flex items-center space-x-3">
                    <div className="w-6 h-6 bg-gradient-to-r from-green-400 to-emerald-400 rounded-full flex items-center justify-center flex-shrink-0">
                      <Check className="w-3 h-3 text-white" />
                    </div>
                    <span className="text-gray-300">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="relative">
              <div className="bg-gradient-to-r from-green-500/20 to-emerald-500/20 rounded-3xl p-8 backdrop-blur-lg border border-white/10">
                <div className="grid grid-cols-2 gap-6">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-white mb-2">
                      99.9%
                    </div>
                    <div className="text-sm text-gray-400">Uptime SLA</div>
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
              <div className="absolute -top-4 -right-4 w-24 h-24 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full opacity-20 blur-xl"></div>
              <div className="absolute -bottom-4 -left-4 w-16 h-16 bg-gradient-to-r from-teal-500 to-cyan-500 rounded-full opacity-20 blur-xl"></div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-green-900/50 to-emerald-900/50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Ready to Revolutionize Your Nutrition?
          </h2>
          <p className="text-xl text-gray-300 mb-8">
            Join thousands of users who have transformed their health with
            AI-powered personalized diet recommendations.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="/auth"
              className="bg-gradient-to-r from-green-500 to-emerald-500 text-white px-10 py-4 rounded-full text-lg font-semibold hover:from-green-600 hover:to-emerald-600 transition-all transform hover:scale-105 shadow-2xl inline-flex items-center justify-center"
            >
              Start Free Trial
              <ArrowRight className="inline-block ml-2 w-5 h-5" />
            </a>
            <button className="border border-white/30 text-white px-10 py-4 rounded-full text-lg font-semibold hover:bg-white/10 transition-all backdrop-blur-sm">
              Contact Sales
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 sm:px-6 lg:px-8 bg-black/40 border-t border-white/10">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-3 gap-8 mb-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg flex items-center justify-center">
                  <Heart className="w-4 h-4 text-white" />
                </div>
                <span className="text-xl font-bold text-white">NutriAI</span>
              </div>
              <p className="text-gray-400 mb-4">
                Empowering healthier lives through AI-driven personalized
                nutrition and enterprise-grade infrastructure.
              </p>
              <div className="flex space-x-4">
                <a
                  href="#"
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  <Github className="w-5 h-5" />
                </a>
                <a
                  href="#"
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  <LinkIcon className="w-5 h-5" />
                </a>
              </div>
            </div>

            <div>
              <h4 className="text-white font-semibold mb-4">Product</h4>
              <ul className="space-y-2">
                <li>
                  <a
                    href="#features"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    Features
                  </a>
                </li>
                <li>
                  <a
                    href="#devops"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    DevOps Pipeline
                  </a>
                </li>
                <li>
                  <a
                    href="#technology"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    Technology Stack
                  </a>
                </li>
                <li>
                  <a
                    href="#benefits"
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    Benefits
                  </a>
                </li>
              </ul>
            </div>

            <div>
              <h4 className="text-white font-semibold mb-4">Technology</h4>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li>Jenkins CI/CD</li>
                <li>Docker + Kubernetes</li>
                <li>AWS EKS + ECR</li>
                <li>Terraform + Ansible</li>
                <li>Supabase Auth + DB</li>
                <li>CloudWatch + Grafana</li>
              </ul>
            </div>
          </div>

          <div className="border-t border-white/10 pt-8">
            <div className="text-center text-gray-400 text-sm">
              <p>
                &copy; 2025 NutriAI. All rights reserved. Built with modern
                DevOps practices.
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
