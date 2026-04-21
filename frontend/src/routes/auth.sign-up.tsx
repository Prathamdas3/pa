import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { AlertCircle, Lock, Mail, User, UserPlus } from "lucide-react";
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
import { useSignUp } from "@/hooks/use-auth";

export const Route = createFileRoute("/auth/sign-up")({
	component: SignUpPage,
});

function SignUpPage() {
	const [email, setEmail] = useState("");
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");
	const signUp = useSignUp();
	const navigate = useNavigate();

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		const result = await signUp.mutateAsync({ email, username, password });
		if (result) {
			navigate({ to: "/tasks" });
		}
	};

	return (
		<div className="flex min-h-[calc(100vh-64px)] items-center justify-center p-4">
			<Card className="w-full max-w-md shadow-lg transition-all hover:shadow-xl">
				<CardHeader className="space-y-1 text-center">
					<div className="flex justify-center pb-2">
						<Badge variant="outline" className="mb-2">
							Join the Platform
						</Badge>
					</div>
					<CardTitle className="text-3xl font-bold tracking-tight">
						Create Account
					</CardTitle>
					<CardDescription>
						Join PrimeTradeAI and start managing your tasks efficiently
					</CardDescription>
				</CardHeader>
				<form onSubmit={handleSubmit}>
					<CardContent className="space-y-4">
						{signUp.error && (
							<div className="flex items-center gap-2 rounded-md bg-destructive/10 p-3 text-sm text-destructive">
								<AlertCircle className="h-4 w-4" />
								<span>{signUp.error.message}</span>
							</div>
						)}
						<div className="space-y-2">
							<label htmlFor="username" className="text-sm font-medium">
								Username
							</label>
							<div className="relative">
								<User className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
								<Input
									id="username"
									placeholder="johndoe"
									className="pl-10"
									value={username}
									onChange={(e) => setUsername(e.target.value)}
									required
								/>
							</div>
						</div>
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
							<label htmlFor="password" className="text-sm font-medium">
								Password
							</label>
							<div className="relative">
								<Lock className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
								<Input
									id="password"
									type="password"
									className="pl-10"
									value={password}
									onChange={(e) => setPassword(e.target.value)}
									required
									minLength={8}
								/>
							</div>
							<p className="text-[10px] text-muted-foreground uppercase font-semibold">
								Min 8 chars, 1 upper, 1 lower, 1 digit, 1 special char
							</p>
						</div>
					</CardContent>
					<CardFooter className="flex flex-col gap-4">
						<Button
							type="submit"
							className="h-12 w-full text-lg"
							disabled={signUp.isPending}
						>
							{signUp.isPending ? "Creating account..." : "Sign Up"}
							{!signUp.isPending && <UserPlus className="ml-2 h-5 w-5" />}
						</Button>
						<p className="text-center text-sm text-muted-foreground">
							Already have an account?{" "}
							<a
								href="/auth/login"
								className="font-medium text-primary hover:underline"
							>
								Log in
							</a>
						</p>
					</CardFooter>
				</form>
			</Card>
		</div>
	);
}
