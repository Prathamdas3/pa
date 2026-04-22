import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

export const Route = createFileRoute("/")({ component: Home });

function Home() {
  const navigate = useNavigate();

  return (
    <div className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden bg-background px-6">
      {/* Subtle background grid */}
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage:
            "linear-gradient(to right, currentColor 1px, transparent 1px), linear-gradient(to bottom, currentColor 1px, transparent 1px)",
          backgroundSize: "48px 48px",
        }}
      />

      {/* Glow */}
      <div className="pointer-events-none absolute left-1/2 top-1/2 h-[500px] w-[500px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-primary/5 blur-3xl" />

      <div className="relative z-10 flex flex-col items-center gap-8 text-center">
        <span className="rounded-full border border-border bg-muted px-4 py-1 text-xs font-semibold uppercase tracking-widest text-muted-foreground">
          PrimeTradeAI
        </span>

        <h1 className="max-w-3xl text-5xl font-extrabold tracking-tight lg:text-7xl">
          Trade smarter.{" "}
          <span className="text-primary">Move faster.</span>
        </h1>

        <p className="max-w-xl text-lg text-muted-foreground">
          Your intelligent trading companion. Manage tasks, track signals, and
          stay ahead of the market — all in one place.
        </p>

        <Button
          size="lg"
          className="h-12 px-8 text-base font-semibold"
          onClick={() => navigate({ to: "/tasks" })}
        >
          Get Started
          <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
      </div>

      <footer className="absolute bottom-6 text-xs text-muted-foreground">
        © {new Date().getFullYear()} PrimeTradeAI. All rights reserved.
      </footer>
    </div>
  );
}