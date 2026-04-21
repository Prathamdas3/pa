import { Link, useNavigate } from "@tanstack/react-router";
import { LogOut, User as UserIcon } from "lucide-react";
import { useLogout } from "#/hooks/auth";
import { useGetMe } from "#/hooks/user";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export function Navbar() {
	const { data: user, isLoading } = useGetMe();
	const logout = useLogout();
	const navigate = useNavigate();

	const handleLogout = async () => {
		await logout.mutateAsync();
		navigate({ to: "/" });
	};

	return (
		<nav className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
			<div className="container mx-auto flex h-16 items-center justify-between px-4">
				<div className="flex items-center gap-6">
					<Link to="/" className="flex items-center space-x-2">
						<span className="text-xl font-bold tracking-tight">
							PrimeTrade<span className="text-primary">AI</span>
						</span>
					</Link>
					{user && (
						<div className="hidden space-x-4 md:flex">
							<Link
								to="/tasks"
								className="text-sm font-medium transition-colors hover:text-primary"
								activeProps={{ className: "text-primary font-bold" }}
							>
								Tasks
							</Link>
						</div>
					)}
				</div>

				<div className="flex items-center gap-4">
					{isLoading ? (
						<div className="h-8 w-8 animate-pulse rounded-full bg-muted" />
					) : user ? (
						<div className="flex items-center gap-4">
							<div className="hidden flex-col items-end md:flex">
								<span className="text-sm font-medium">{user.username}</span>
								<Badge variant="secondary" className="text-[10px] uppercase">
									{user.role}
								</Badge>
							</div>
							<Link to="/profile">
								<Button variant="ghost" size="icon" className="rounded-full">
									<UserIcon className="h-5 w-5" />
								</Button>
							</Link>
							<Button
								variant="ghost"
								size="icon"
								onClick={handleLogout}
								disabled={logout.isPending}
							>
								<LogOut className="h-5 w-5 text-destructive" />
							</Button>
						</div>
					) : (
						<div className="flex items-center gap-2">
							<Link to="/auth/login">
								<Button variant="ghost">Login</Button>
							</Link>
							<Link to="/auth/sign-up">
								<Button>Sign Up</Button>
							</Link>
						</div>
					)}
				</div>
			</div>
		</nav>
	);
}
