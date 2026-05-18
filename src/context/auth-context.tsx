"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import {
  AUTH_STORAGE_KEY,
  isValidEmail,
  normalizeEmail,
} from "@/lib/auth";

interface AuthContextValue {
  email: string | null;
  isAuthenticated: boolean;
  isReady: boolean;
  login: (email: string) => boolean;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

function loadSession(): string | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(AUTH_STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as { email?: string };
    if (parsed.email && isValidEmail(parsed.email)) {
      return normalizeEmail(parsed.email);
    }
    return null;
  } catch {
    return null;
  }
}

function saveSession(email: string | null) {
  if (typeof window === "undefined") return;
  if (!email) {
    localStorage.removeItem(AUTH_STORAGE_KEY);
    return;
  }
  localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify({ email }));
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [email, setEmail] = useState<string | null>(null);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    setEmail(loadSession());
    setIsReady(true);
  }, []);

  const login = useCallback((rawEmail: string) => {
    const normalized = normalizeEmail(rawEmail);
    if (!isValidEmail(normalized)) return false;
    setEmail(normalized);
    saveSession(normalized);
    return true;
  }, []);

  const logout = useCallback(() => {
    setEmail(null);
    saveSession(null);
  }, []);

  const value = useMemo(
    () => ({
      email,
      isAuthenticated: Boolean(email),
      isReady,
      login,
      logout,
    }),
    [email, isReady, login, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
