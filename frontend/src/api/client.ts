import { tryCatch } from "#/lib/trycatch";
import type {
	ApiResponse,
	LoginUser,
	MessageResponse,
	Task,
	TaskCreate,
	TaskUpdate,
	User,
	UserCreate,
	UserRole,
	UserUpdate,
} from "./types";

const BASE_URL = "/api/v1";

const request = async <T>(
	path: string,
	options: RequestInit = {},
): Promise<T> => {
	const response = await fetch(`${BASE_URL}${path}`, {
		...options,
		headers: {
			"Content-Type": "application/json",
			...options.headers,
		},
	});

	if (!response.ok) {
		const errorData = await response.json().catch(() => ({}));
		throw new Error(errorData.error || response.statusText);
	}

	return response.json();
};

export const authApi = {
	signUpUser: (data: UserCreate) =>
		tryCatch(
			request<ApiResponse<{ id: string; email: string; username: string }>>(
				"/auth/sign-up/user",
				{
					method: "POST",
					body: JSON.stringify(data),
				},
			),
		),

	signUpAdmin: (data: UserCreate) =>
		tryCatch(
			request<ApiResponse<{ id: string; email: string; username: string }>>(
				"/auth/sign-up/admin",
				{
					method: "POST",
					body: JSON.stringify(data),
				},
			),
		),

	login: (data: LoginUser) =>
		tryCatch(
			request<ApiResponse<{ id: string; email: string; username: string }>>(
				"/auth/login",
				{
					method: "POST",
					body: JSON.stringify(data),
				},
			),
		),

	logout: () =>
		tryCatch(
			request<ApiResponse<MessageResponse>>("/auth/logout", { method: "POST" }),
		),

	refresh: () =>
		tryCatch(
			request<ApiResponse<MessageResponse>>("/auth/refresh", { method: "GET" }),
		),
};

export const tasksApi = {
	getAll: () => tryCatch(request<ApiResponse<Task[]>>("/tasks")),

	create: (data: TaskCreate) =>
		tryCatch(
			request<ApiResponse<Task>>("/tasks", {
				method: "POST",
				body: JSON.stringify(data),
			}),
		),

	getOne: (taskId: string) =>
		tryCatch(request<ApiResponse<Task>>(`/tasks/${taskId}`)),

	update: (taskId: string, data: TaskUpdate) =>
		tryCatch(
			request<ApiResponse<Task>>(`/tasks/${taskId}`, {
				method: "PATCH",
				body: JSON.stringify(data),
			}),
		),

	delete: (taskId: string) =>
		tryCatch(
			request<ApiResponse<MessageResponse>>(`/tasks/${taskId}`, {
				method: "DELETE",
			}),
		),

	// Admin endpoints
	adminGetAll: () => tryCatch(request<ApiResponse<Task[]>>("/tasks/admin/all")),

	adminGetOne: (taskId: string) =>
		tryCatch(request<ApiResponse<Task>>(`/tasks/admin/${taskId}`)),

	adminDelete: (taskId: string) =>
		tryCatch(
			request<ApiResponse<MessageResponse>>(`/tasks/admin/${taskId}`, {
				method: "DELETE",
			}),
		),
};

export const usersApi = {
	getMe: () =>
		tryCatch(
			request<
				ApiResponse<{
					id: string;
					email: string;
					username: string;
					role: string;
				}>
			>("/users/me"),
		),

	updateMe: (data: UserUpdate) =>
		tryCatch(
			request<ApiResponse<MessageResponse>>("/users/me", {
				method: "PATCH",
				body: JSON.stringify(data),
			}),
		),

	deleteMe: () =>
		tryCatch(
			request<ApiResponse<MessageResponse>>("/users/me", { method: "DELETE" }),
		),

	// Admin endpoints
	adminGetAll: () => tryCatch(request<ApiResponse<User[]>>("/users/admin/all")),

	adminGetOne: (userId: string) =>
		tryCatch(
			request<
				ApiResponse<{
					id: string;
					email: string;
					username: string;
					role: string;
				}>
			>(`/users/admin/${userId}`),
		),

	adminDelete: (userId: string) =>
		tryCatch(
			request<ApiResponse<MessageResponse>>(`/users/admin/${userId}`, {
				method: "DELETE",
			}),
		),

	adminUpdateRole: (userId: string, role: UserRole) =>
		tryCatch(
			request<
				ApiResponse<{
					id: string;
					email: string;
					username: string;
					role: string;
				}>
			>(`/users/admin/${userId}/role?role=${role}`, {
				method: "PATCH",
			}),
		),
};
