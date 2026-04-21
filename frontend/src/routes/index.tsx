import { createFileRoute } from "@tanstack/react-router";
import { GitBranch, Rocket, Terminal } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
	Card,
	CardContent,
	CardDescription,
	CardFooter,
	CardHeader,
	CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";

export const Route = createFileRoute("/")({ component: Home });

function Home() {
	return (
		<div className="min-h-screen bg-background p-8 font-sans">
			<div className="mx-auto max-w-4xl space-y-12">
				<header className="space-y-4 text-center">
					<Badge variant="outline" className="px-3 py-1 text-sm">
						<Rocket className="mr-2 h-4 w-4" />
						Tailwind CSS v4 + Shadcn UI
					</Badge>
					<h1 className="text-5xl font-extrabold tracking-tight lg:text-6xl">
						PrimeTradeAI Frontend
					</h1>
					<p className="mx-auto max-w-2xl text-xl text-muted-foreground">
						A high-performance trading interface built with TanStack Router,
						Tailwind CSS v4, and Shadcn UI.
					</p>
					<div className="flex justify-center gap-4 pt-4">
						<Button size="lg" className="h-12 px-8 text-lg font-medium">
							Get Started
						</Button>
						<Button
							size="lg"
							variant="outline"
							className="h-12 px-8 text-lg font-medium"
						>
							<GitBranch className="mr-2 h-5 w-5" />
							Github Repo
						</Button>
					</div>
				</header>

				<Separator />

				<div className="grid gap-6 md:grid-cols-2">
					<Card>
						<CardHeader>
							<CardTitle className="flex items-center gap-2">
								<Terminal className="h-5 w-5" />
								Quick Actions
							</CardTitle>
							<CardDescription>
								Test the new Shadcn input and button components.
							</CardDescription>
						</CardHeader>
						<CardContent className="space-y-4">
							<div className="space-y-2">
								<label
									htmlFor="search-markets"
									className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
								>
									Search Markets
								</label>
								<Input
									id="search-markets"
									placeholder="Enter symbol (e.g. BTC/USD)..."
								/>
							</div>
						</CardContent>
						<CardFooter>
							<Button variant="secondary" className="w-full">
								Search
							</Button>
						</CardFooter>
					</Card>

					<Card>
						<CardHeader>
							<CardTitle>System Status</CardTitle>
							<CardDescription>
								Real-time monitoring of connectivity.
							</CardDescription>
						</CardHeader>
						<CardContent className="space-y-4">
							<div className="flex items-center justify-between">
								<span className="text-sm font-medium">API Connection</span>
								<Badge className="bg-emerald-500 font-semibold hover:bg-emerald-600">
									Stable
								</Badge>
							</div>
							<div className="flex items-center justify-between">
								<span className="text-sm font-medium">Latency</span>
								<span className="font-mono text-sm">12ms</span>
							</div>
							<div className="flex items-center justify-between">
								<span className="text-sm font-medium">Version</span>
								<Badge variant="outline">v0.1.0-alpha</Badge>
							</div>
						</CardContent>
					</Card>
				</div>

				<footer className="pt-12 text-center text-sm text-muted-foreground">
					Built with precision using the latest modern web technologies.
				</footer>
			</div>
		</div>
	);
}
