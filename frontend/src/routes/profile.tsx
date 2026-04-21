import { useQueryClient } from "@tanstack/react-query";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { AlertCircle, Mail, Save, Shield, Trash2, User } from "lucide-react";
import { useEffect, useState } from "react";
import { usersApi } from "@/api/client";
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
import { useUser } from "@/hooks/use-auth";

export const Route = createFileRoute("/profile")({
	component: ProfilePage,
});

function ProfilePage() {
	const { data: user, isLoading } = useUser();
	const [username, setUsername] = useState("");
	const [isUpdating, setIsUpdating] = useState(false);
	const [status, setStatus] = useState<{
		type: "success" | "error";
		msg: string;
	} | null>(null);
	const queryClient = useQueryClient();
	const navigate = useNavigate();

	useEffect(() => {
		if (user) {
			setUsername(user.username);
		}
	}, [user]);

	const handleUpdate = async (e: React.FormEvent) => {
		e.preventDefault();
		setIsUpdating(true);
		setStatus(null);

		const { data, error } = await usersApi.updateMe({ username });

		if (error) {
			setStatus({ type: "error", msg: error.message });
		} else {
			setStatus({
				type: "success",
				msg: data?.data?.message || "Username updated!",
			});
			queryClient.invalidateQueries({ queryKey: ["user"] });
		}
		setIsUpdating(false);
	};

	const handleDeleteAccount = async () => {
		if (
			window.confirm(
				"Are you sure you want to delete your account? This action cannot be undone.",
			)
		) {
			const { error } = await usersApi.deleteMe();
			if (!error) {
				queryClient.clear();
				navigate({ to: "/" });
			}
		}
	};

	if (isLoading)
		return <div className="p-8 text-center">Loading profile...</div>;
	if (!user)
		return (
			<div className="p-8 text-center text-destructive">User not found</div>
		);

	return (
		<div className="container mx-auto max-w-2xl p-6 lg:p-10">
			<div className="mb-8 space-y-2">
				<h1 className="text-3xl font-extrabold tracking-tight">
					Account Settings
				</h1>
				<p className="text-muted-foreground">
					Manage your profile and account preferences
				</p>
			</div>

			<Card className="shadow-sm">
				<CardHeader className="flex flex-row items-center justify-between space-y-0">
					<div className="space-y-1">
						<CardTitle>Personal Information</CardTitle>
						<CardDescription>Update your public username</CardDescription>
					</div>
					<Badge variant="outline" className="h-6 gap-1 px-2">
						<Shield className="h-3 w-3" />
						{user.role}
					</Badge>
				</CardHeader>
				<form onSubmit={handleUpdate}>
					<CardContent className="space-y-6">
						{status && (
							<div
								className={`flex items-center gap-2 rounded-md p-3 text-sm ${
									status.type === "success"
										? "bg-emerald-500/10 text-emerald-500"
										: "bg-destructive/10 text-destructive"
								}`}
							>
								<AlertCircle className="h-4 w-4" />
								<span>{status.msg}</span>
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
									placeholder="Username"
									className="pl-10"
									value={username}
									onChange={(e) => setUsername(e.target.value)}
									required
								/>
							</div>
						</div>

						<div className="space-y-2">
							<label htmlFor="email" className="text-sm font-medium">
								Email Address
							</label>
							<div className="relative">
								<Mail className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
								<Input
									id="email"
									value={user.email}
									disabled
									className="cursor-not-allowed bg-muted pl-10 opacity-70"
								/>
							</div>
							<p className="text-[10px] text-muted-foreground uppercase font-bold">
								Email cannot be changed
							</p>
						</div>
					</CardContent>
					<Separator />
					<CardFooter className="flex justify-between pt-6">
						<Button
							type="submit"
							className="gap-2"
							disabled={isUpdating || username === user.username}
						>
							<Save className="h-4 w-4" />
							{isUpdating ? "Saving..." : "Save Changes"}
						</Button>
					</CardFooter>
				</form>
			</Card>

			<div className="mt-12 space-y-4">
				<h2 className="text-xl font-bold text-destructive">Danger Zone</h2>
				<Card className="border-destructive/20 bg-destructive/5">
					<CardHeader>
						<CardTitle className="text-lg">Delete Account</CardTitle>
						<CardDescription>
							Permanently remove your account and all associated data.
						</CardDescription>
					</CardHeader>
					<CardFooter>
						<Button
							variant="destructive"
							className="gap-2"
							onClick={handleDeleteAccount}
						>
							<Trash2 className="h-4 w-4" />
							Delete Account
						</Button>
					</CardFooter>
				</Card>
			</div>
		</div>
	);
}
