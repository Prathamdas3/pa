export type TasksStatus = "pending" | "in_progress" | "completed";
export type TasksPriority = "low" | "medium" | "high";
export type UserRole = "user" | "admin";

export interface UserCreate {
	email: string;
	username: string;
	password?: string;
}

export interface LoginUser {
	email: string;
	password?: string;
}

export interface UserUpdate {
	username: string;
}

export interface TaskCreate {
	title: string;
	description?: string;
	priority?: TasksPriority;
	status?: TasksStatus;
	due_date?: string;
	tags?: string[];
}

export interface TaskUpdate {
	title?: string;
	description?: string;
	priority?: TasksPriority;
	status?: TasksStatus;
	due_date?: string;
	tags?: string[];
}

export interface Task {
	id: string;
	title: string;
	description: string;
	status: TasksStatus;
	priority: TasksPriority;
	due_date?: string;
	tags: string[];
	user_id: string;
	created_at: string;
	updated_at: string;
}

export interface User {
	id: string;
	email: string;
	username: string;
	role: UserRole;
	is_active: boolean;
}

export interface ApiResponse<T> {
	data: T | null;
	error: unknown | null;
}

export interface MessageResponse {
	message: string;
}
