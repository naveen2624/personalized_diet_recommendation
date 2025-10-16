"use client";

import { Home, Utensils, User } from "lucide-react";
import { usePathname, useRouter } from "next/navigation";

export default function Layout({ children }) {
  const pathname = usePathname();
  const router = useRouter();

  const navItems = [
    { id: "home", icon: Home, label: "Home", path: "/id/home" },
    { id: "diet", icon: Utensils, label: "Diet", path: "/id/diet" },
    { id: "profile", icon: User, label: "Profile", path: "/id/profile" },
  ];

  const isActive = (path) => pathname === path;

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-50">
      {/* Main Content Area */}
      <div className="pb-32">{children}</div>

      {/* iOS Style Bottom Navigation - Centered */}
      <div className="fixed bottom-0 left-0 right-0 flex justify-center pb-6 pointer-events-none">
        <nav className="bg-white/40 backdrop-blur-2xl rounded-full shadow-2xl border border-white/50 px-4 py-3 pointer-events-auto">
          <div className="flex items-center gap-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const active = isActive(item.path);

              return (
                <button
                  key={item.id}
                  onClick={() => router.push(item.path)}
                  className={`flex flex-col items-center justify-center gap-1 px-6 py-2 rounded-full transition-all duration-300 ${
                    active
                      ? "bg-emerald-500/20 text-emerald-600"
                      : "text-gray-500 hover:text-emerald-500 hover:bg-emerald-500/10"
                  }`}
                >
                  <Icon
                    size={24}
                    strokeWidth={2.5}
                    className={`transition-transform duration-300 ${
                      active ? "scale-110" : "scale-100"
                    }`}
                  />
                  <span
                    className={`text-xs font-medium ${
                      active ? "font-semibold" : "font-normal"
                    }`}
                  >
                    {item.label}
                  </span>
                </button>
              );
            })}
          </div>
        </nav>
      </div>
    </div>
  );
}
