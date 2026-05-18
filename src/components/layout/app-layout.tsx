"use client";

import { useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import { Navigation } from "./navigation";
import { useAuth } from "@/context/auth-context";

function AuthenticatedShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      <main className="lg:pl-64">
        <div className="min-h-screen px-4 pb-12 pt-20 lg:px-8 lg:pt-8">{children}</div>
      </main>
    </div>
  );
}

export function AppLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { isAuthenticated, isReady } = useAuth();
  const isHome = pathname === "/";

  useEffect(() => {
    if (!isReady) return;
    if (pathname === "/login") {
      router.replace("/");
      return;
    }
    if (!isAuthenticated && !isHome) {
      router.replace("/");
    }
  }, [isReady, isAuthenticated, isHome, pathname, router]);

  if (!isReady) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <>{children}</>;
  }

  return <AuthenticatedShell>{children}</AuthenticatedShell>;
}
