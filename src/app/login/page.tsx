"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Mail, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ParticlesBackground } from "@/components/shared/particles-background";
import { useAuth } from "@/context/auth-context";
import { toast } from "@/hooks/use-toast";

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    const ok = login(email);
    if (!ok) {
      toast({
        title: "Invalid email",
        description: "Please enter a valid work email address.",
        variant: "destructive",
      });
      setLoading(false);
      return;
    }

    router.replace("/");
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex min-h-screen items-center justify-center px-4 py-12"
    >
      <div className="relative w-full max-w-md overflow-hidden rounded-2xl border border-white/10 bg-card/60 p-8 shadow-glow-sm backdrop-blur-xl md:p-10">
        <ParticlesBackground />
        <div className="absolute inset-0 bg-hero-glow" aria-hidden />

        <div className="relative z-10">
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="mb-8 flex flex-col items-center text-center"
          >
            <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/20 shadow-glow-sm">
              <Sparkles className="h-7 w-7 text-primary" />
            </div>
            <h1 className="text-2xl font-bold tracking-tight md:text-3xl">
              AI Use Cases Arena
            </h1>
            <p className="mt-2 text-sm text-muted">
              Sign in with your work email to submit and vote on AI use cases at
              Invest-NL.
            </p>
          </motion.div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Work email address</Label>
              <motion.div className="relative">
                <Mail className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted" />
                <Input
                  id="email"
                  type="email"
                  inputMode="email"
                  autoComplete="email"
                  placeholder="you@invest-nl.nl"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="pl-10"
                  required
                />
              </motion.div>
              <p className="text-[11px] leading-relaxed text-muted">
                GDPR notice: your email address is collected and used solely to
                operate the AI Use Cases Arena (identifying your submissions,
                votes, and comments within this tool). It is not used for
                marketing, is not sold to third parties, and is retained only
                for as long as needed for this initiative. You may request
                access to or deletion of your data by contacting your Invest-NL
                programme administrator.
              </p>
            </div>

            <Button type="submit" size="lg" className="w-full" disabled={loading}>
              {loading ? "Signing in..." : "Continue to Arena"}
            </Button>
          </form>
        </div>
      </div>
    </motion.div>
  );
}
