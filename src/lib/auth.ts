export const AUTH_STORAGE_KEY = "ai-use-cases-arena-auth";

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function isValidEmail(email: string): boolean {
  return EMAIL_PATTERN.test(email.trim().toLowerCase());
}

export function normalizeEmail(email: string): string {
  return email.trim().toLowerCase();
}

export function getDisplayNameFromEmail(email: string): string {
  const local = normalizeEmail(email).split("@")[0] ?? email;
  const name = local.replace(/[._-]+/g, " ").trim();
  if (!name) return email;
  return name
    .split(" ")
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export function getAvatarFromEmail(email: string): string {
  const local = normalizeEmail(email).split("@")[0] ?? "";
  const parts = local.replace(/[._-]+/g, " ").trim().split(/\s+/).filter(Boolean);
  if (parts.length >= 2) {
    return `${parts[0][0] ?? ""}${parts[1][0] ?? ""}`.toUpperCase();
  }
  return local.slice(0, 2).toUpperCase() || "??";
}
