import { createFileRoute } from "@tanstack/react-router";
import {
	AlertCircle,
	Calendar,
	CheckCircle2,
	Clock,
	Plus,
	Tag,
	Trash2,
} from "lucide-react";
import { useState } from "react";
import type { TasksPriority, TasksStatus } from "@/api/types";
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
import { useCreateTask, useDeleteTask, useGetTasks } from "#/hooks/task";

export const Route = createFileRoute("/tasks")({
	component: TasksPage,
});

function TasksPage() {
	const { data: tasks, isLoading, error } = useGetTasks();
	const createTask = useCreateTask();
	const deleteTask = useDeleteTask();

	const [newTitle, setNewTitle] = useState("");
	const [newDescription, setNewDescription] = useState("");

	const handleCreateTask = async (e: React.FormEvent) => {
		e.preventDefault();
		if (!newTitle.trim()) return;
		await createTask.mutateAsync({
			title: newTitle,
			description: newDescription,
			priority: "medium",
			status: "pending",
		});
		setNewTitle("");
		setNewDescription("");
	};

	const getStatusIcon = (status: TasksStatus) => {
		switch (status) {
			case "completed":
				return <CheckCircle2 className="h-4 w-4 text-emerald-500" />;
			case "in_progress":
				return <Clock className="h-4 w-4 text-blue-500" />;
			default:
				return <AlertCircle className="h-4 w-4 text-amber-500" />;
		}
	};

	const getPriorityColor = (priority: TasksPriority) => {
		switch (priority) {
			case "high":
				return "destructive";
			case "medium":
				return "secondary";
			default:
				return "outline";
		}
	};

	if (isLoading)
		return <div className="p-8 text-center">Loading your tasks...</div>;
	if (error)
		return (
			<div className="p-8 text-center text-destructive">
				Error loading tasks: {error.message}
			</div>
		);

	return (
		<div className="container mx-auto max-w-5xl space-y-8 p-6 lg:p-10">
			<header className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
				<div>
					<h1 className="text-3xl font-extrabold tracking-tight">Tasks</h1>
					<p className="text-muted-foreground">
						Manage and track your active trading tasks
					</p>
				</div>
				<Badge variant="outline" className="w-fit px-3 py-1 text-sm">
					{tasks?.length || 0} Total Tasks
				</Badge>
			</header>

			<div className="grid gap-8 lg:grid-cols-3">
				{/* Sidebar: Add Task Form */}
				<aside className="lg:col-span-1">
					<Card className="sticky top-24 border-primary/20 shadow-sm transition-all hover:border-primary/40">
						<CardHeader>
							<CardTitle className="text-xl">Create New Task</CardTitle>
							<CardDescription>
								Define a new task to track your progress
							</CardDescription>
						</CardHeader>
						<form onSubmit={handleCreateTask}>
							<CardContent className="space-y-4">
								<div className="space-y-2">
									<label htmlFor="title" className="text-sm font-medium">
										Title
									</label>
									<Input
										id="title"
										placeholder="Review BTC daily candle..."
										value={newTitle}
										onChange={(e) => setNewTitle(e.target.value)}
										required
									/>
								</div>
								<div className="space-y-2">
									<label htmlFor="description" className="text-sm font-medium">
										Description
									</label>
									<Input
										id="description"
										placeholder="Optional details..."
										value={newDescription}
										onChange={(e) => setNewDescription(e.target.value)}
									/>
								</div>
							</CardContent>
							<CardFooter>
								<Button
									type="submit"
									className="w-full"
									disabled={createTask.isPending}
								>
									{createTask.isPending ? "Adding..." : "Add Task"}
									<Plus className="ml-2 h-4 w-4" />
								</Button>
							</CardFooter>
						</form>
					</Card>
				</aside>

				{/* Main Content: Tasks List */}
				<div className="space-y-4 lg:col-span-2">
					{tasks?.length === 0 ? (
						<div className="flex h-48 flex-col items-center justify-center rounded-xl border border-dashed text-muted-foreground shadow-sm">
							<ClipboardList className="mb-2 h-10 w-10 opacity-20" />
							<p>No tasks found. Create one to get started!</p>
						</div>
					) : (
						tasks?.map((task) => (
							<Card
								key={task.id}
								className="group relative overflow-hidden transition-all hover:bg-muted/30"
							>
								<div className="p-6">
									<div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
										<div className="space-y-1">
											<div className="flex items-center gap-2">
												{getStatusIcon(task.status)}
												<h3 className="font-bold uppercase tracking-wide">
													{task.title}
												</h3>
											</div>
											<p className="text-sm text-muted-foreground">
												{task.description || "No description provided."}
											</p>
										</div>
										<div className="flex items-center gap-2">
											<Badge
												variant={getPriorityColor(task.priority)}
												className="capitalize"
											>
												{task.priority}
											</Badge>
											<Button
												variant="ghost"
												size="icon"
												className="h-8 w-8 text-muted-foreground opacity-0 transition-opacity group-hover:opacity-100 hover:text-destructive"
												onClick={() => deleteTask.mutate(task.id)}
												disabled={deleteTask.isPending}
											>
												<Trash2 className="h-4 w-4" />
											</Button>
										</div>
									</div>

									<Separator className="my-4" />

									<div className="flex flex-wrap items-center gap-4 text-[10px] uppercase font-bold text-muted-foreground">
										<div className="flex items-center gap-1.5">
											<Calendar className="h-3 w-3" />
											<span>
												Created {new Date(task.created_at).toLocaleDateString()}
											</span>
										</div>
										{task.tags.length > 0 && (
											<div className="flex items-center gap-1.5">
												<Tag className="h-3 w-3" />
												<div className="flex gap-1">
													{task.tags.map((tag) => (
														<span
															key={tag}
															className="rounded bg-muted px-1.5 py-0.5"
														>
															{tag}
														</span>
													))}
												</div>
											</div>
										)}
									</div>
								</div>
							</Card>
						))
					)}
				</div>
			</div>
		</div>
	);
}

function ClipboardList(props: React.SVGProps<SVGSVGElement>) {
	return (
		<svg
			{...props}
			xmlns="http://www.w3.org/2000/svg"
			width="24"
			height="24"
			viewBox="0 0 24 24"
			fill="none"
			stroke="currentColor"
			strokeWidth="2"
			strokeLinecap="round"
			strokeLinejoin="round"
		>
			<title>Clipboard List Icon</title>
			<rect width="8" height="4" x="8" y="2" rx="1" ry="1" />
			<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" />
			<path d="M12 11h4" />
			<path d="M12 16h4" />
			<path d="M8 11h.01" />
			<path d="M8 16h.01" />
		</svg>
	);
}
