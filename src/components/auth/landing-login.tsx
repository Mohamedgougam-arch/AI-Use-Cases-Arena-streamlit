"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Mail, Sparkles, FileText, ThumbsUp, Trophy } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ParticlesBackground } from "@/components/shared/particles-background";
import { useAuth } from "@/context/auth-context";
import { toast } from "@/hooks/use-toast";

const highlights = [
  {
    icon: FileText,
    title: "Submit ideas",
    description: "Share AI use cases from your team at Invest-NL.",
  },
  {
    icon: ThumbsUp,
    title: "Vote and prioritize",
    description: "Help decide which opportunities move forward.",
  },
  {
    icon: Trophy,
    title: "Track contribution",
    description: "See your impact on the leaderboard.",
  },
];

export function LandingLogin() {
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
  };

  return (
    <div className="relative min-h-screen overflow-hidden">
      <ParticlesBackground />
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="relative z-10 mx-auto flex min-h-screen max-w-6xl flex-col justify-center px-4 py-16 lg:flex-row lg:items-center lg:gap-16 lg:py-20"
      >
        <div className="mb-12 flex-1 text-center lg:mb-0 lg:text-left">
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="mb-6 inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/20 shadow-glow-sm"
          >
            <Sparkles className="h-7 w-7 text-primary" />
          </motion.div>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mb-3 text-sm font-medium uppercase tracking-widest text-primary"
          >
            Invest-NL Innovation Arena
          </motion.p>
          <motion.h1
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-4xl font-bold tracking-tight md:text-5xl lg:text-6xl"
          >
            Shape the future of{" "}
            <span className="text-gradient">AI at Invest-NL</span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.08 }}
            className="mt-4 max-w-xl text-lg text-muted md:text-xl lg:mx-0 mx-auto"
          >
            Submit, explore, vote, and prioritize the AI use cases that can
            transform our organization.
          </motion.p>
          <ul className="mt-10 hidden gap-6 sm:grid sm:grid-cols-3 lg:grid-cols-1 lg:gap-5">
            {highlights.map((item, i) => (
              <motion.li
                key={item.title}
                initial={{ opacity: 0, x: -12 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.15 + i * 0.06 }}
                className="flex gap-3 text-left"
              >
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary/10">
                  <item.icon className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <p className="font-semibold text-sm">{item.title}</p>
                  <p className="text-xs text-muted leading-relaxed">
                    {item.description}
                  </p>
                </div>
              </motion.li>
            ))}
          </ul>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="w-full max-w-md shrink-0"
        >
          <div className="relative overflow-hidden rounded-2xl border border-white/10 bg-card/60 p-8 shadow-glow-sm backdrop-blur-xl md:p-10">
            <div className="absolute inset-0 bg-hero-glow pointer-events-none" aria-hidden />

            <div className="relative z-10">
              <h2 className="text-xl font-bold tracking-tight">Sign in to continue</h2>
              <p className="mt-2 text-sm text-muted">
                Use your work email to access the arena.
              </p>

              <form onSubmit={handleSubmit} className="mt-6 space-y-4">
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
      </motion.div>
    </div>
  );
}
