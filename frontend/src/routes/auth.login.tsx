import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { AlertCircle, Lock, LogIn, Mail } from "lucide-react";
import { useState } from "react";
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
import { useLogin } from "@/hooks/use-auth";

export const Route = createFileRoute("/auth/login")({
	component: LoginPage,
});

function LoginPage() {
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const login = useLogin();
	const navigate = useNavigate();

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		const result = await login.mutateAsync({ email, password });
		if (result) {
			navigate({ to: "/tasks" });
		}
	};

	return (
		<div className="flex h-[calc(100vh-64px)] items-center justify-center p-4">
			<Card className="w-full max-w-md shadow-lg transition-all hover:shadow-xl">
				<CardHeader className="space-y-1 text-center">
					<div className="flex justify-center pb-2">
						<Badge variant="outline" className="mb-2">
							Account Access
						</Badge>
					</div>
					<CardTitle className="text-3xl font-bold tracking-tight">
						Welcome Back
					</CardTitle>
					<CardDescription>
						Enter your credentials to access your dashboard
					</CardDescription>
				</CardHeader>
				<form onSubmit={handleSubmit}>
					<CardContent className="space-y-4">
						{login.error && (
							<div className="flex items-center gap-2 rounded-md bg-destructive/10 p-3 text-sm text-destructive">
								<AlertCircle className="h-4 w-4" />
								<span>{login.error.message}</span>
							</div>
						)}
						<div className="space-y-2">
							<label htmlFor="email" className="text-sm font-medium">
								Email
							</label>
							<div className="relative">
								<Mail className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
								<Input
									id="email"
									type="email"
									placeholder="name@example.com"
									className="pl-10"
									value={email}
									onChange={(e) => setEmail(e.target.value)}
									required
								/>
							</div>
						</div>
						<div className="space-y-2">
							<div className="flex items-center justify-between">
								<label htmlFor="password" className="text-sm font-medium">
									Password
								</label>
							</div>
							<div className="relative">
								<Lock className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
								<Input
									id="password"
									type="password"
									className="pl-10"
									value={password}
									onChange={(e) => setPassword(e.target.value)}
									required
								/>
							</div>
						</div>
					</CardContent>
					<CardFooter className="flex flex-col gap-4">
						<Button
							type="submit"
							className="h-12 w-full text-lg"
							disabled={login.isPending}
						>
							{login.isPending ? "Logging in..." : "Login"}
							{!login.isPending && <LogIn className="ml-2 h-5 w-5" />}
						</Button>
						<p className="text-center text-sm text-muted-foreground">
							Don't have an account?{" "}
							<a
								href="/auth/sign-up"
								className="font-medium text-primary hover:underline"
							>
								Sign up
							</a>
						</p>
					</CardFooter>
				</form>
			</Card>
		</div>
	);
}
