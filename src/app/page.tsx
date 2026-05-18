"use client";

import { LandingLogin } from "@/components/auth/landing-login";
import { DashboardHome } from "@/components/dashboard/dashboard-home";
import { useAuth } from "@/context/auth-context";

export default function HomePage() {
  const { isAuthenticated, isReady } = useAuth();

  if (!isReady) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <LandingLogin />;
  }

  return <DashboardHome />;
}
