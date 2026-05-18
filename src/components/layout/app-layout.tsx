"use client";

import { useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import { Navigation } from "./navigation";
import { useAuth } from "@/context/auth-context";

export function AppLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { isAuthenticated, isReady } = useAuth();
  const isLoginPage = pathname === "/login";

  useEffect(() => {
    if (!isReady) return;
    if (isLoginPage && isAuthenticated) {
      router.replace("/");
      return;
    }
    if (!isLoginPage && !isAuthenticated) {
      router.replace("/login");
    }
  }, [isReady, isAuthenticated, isLoginPage, router]);

  if (!isReady) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />
      </div>
    );
  }

  if (isLoginPage) {
    return <>{children}</>;
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      <main className="lg:pl-64">
        <div className="min-h-screen px-4 pb-12 pt-20 lg:px-8 lg:pt-8">
          {children}
        </div>
      </main>
    </div>
  );
}
