import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/axios";
import { tryCatch } from "@/lib/trycatch";

// ─────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────

export type Task = {
  id: string;
  title: string;
  description: string | null;
  status: "pending" | "in_progress" | "completed";
  priority: "low" | "medium" | "high";
  due_date: string | null;
  tags: string[] | null;
  user_id: string;
  created_at: string;
  updated_at: string;
};

export type TaskCreate = {
  title: string;
  description?: string;
  status?: "pending" | "in_progress" | "completed";
  priority?: "low" | "medium" | "high";
  due_date?: string;
  tags?: string[];
};

export type TaskUpdate = Partial<TaskCreate>;

export type ApiResponse<T> = {
  data: T | null;
  error: string | null;
  message?: string;
};

// ─────────────────────────────────────────────
// Query Keys
// ─────────────────────────────────────────────

export const taskQueryKeys = {
  all: ["tasks"] as const,
  one: (id: string) => ["tasks", id] as const,
  adminAll: ["admin", "tasks"] as const,
  adminOne: (id: string) => ["admin", "tasks", id] as const,
};

// ─────────────────────────────────────────────
// User Task Hooks
// ─────────────────────────────────────────────

/** GET /tasks */
export function useGetTasks() {
  return useQuery({
    queryKey: taskQueryKeys.all,
    queryFn: async () => {
      const { data, error } = await tryCatch(
        api.get<ApiResponse<Task[]>>("/tasks")
      );
      if (error) throw error;
      return data?.data.data;
    },
  });
}

/** GET /tasks/:id */
export function useGetTask(taskId: string) {
  return useQuery({
    queryKey: taskQueryKeys.one(taskId),
    queryFn: async () => {
      const { data, error } = await tryCatch(
        api.get<ApiResponse<Task>>(`/tasks/${taskId}`)
      );
      if (error) throw error;
      return data?.data.data;
    },
    enabled: !!taskId,
  });
}

/** POST /tasks */
export function useCreateTask() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (body: TaskCreate) => {
      const { data, error } = await tryCatch(
        api.post<ApiResponse<Task>>("/tasks", body)
      );
      if (error) throw error;
      return data?.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: taskQueryKeys.all });
    },
  });
}

/** PATCH /tasks/:id */
export function useUpdateTask(taskId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (body: TaskUpdate) => {
      const { data, error } = await tryCatch(
        api.patch<ApiResponse<Task>>(`/tasks/${taskId}`, body)
      );
      if (error) throw error;
      return data?.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: taskQueryKeys.all });
      queryClient.invalidateQueries({ queryKey: taskQueryKeys.one(taskId) });
    },
  });
}

/** DELETE /tasks/:id */
export function useDeleteTask() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (taskId: string) => {
      const { data, error } = await tryCatch(
        api.delete<ApiResponse<{ message: string }>>(`/tasks/${taskId}`)
      );
      if (error) throw error;
      return data?.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: taskQueryKeys.all });
    },
  });
}

// ─────────────────────────────────────────────
// Admin Task Hooks
// ─────────────────────────────────────────────

/** GET /tasks/admin/all */
export function useAdminGetAllTasks() {
  return useQuery({
    queryKey: taskQueryKeys.adminAll,
    queryFn: async () => {
      const { data, error } = await tryCatch(
        api.get<ApiResponse<Task[]>>("/tasks/admin/all")
      );
      if (error) throw error;
      return data?.data.data;
    },
  });
}

/** GET /tasks/admin/:id */
export function useAdminGetTask(taskId: string) {
  return useQuery({
    queryKey: taskQueryKeys.adminOne(taskId),
    queryFn: async () => {
      const { data, error } = await tryCatch(
        api.get<ApiResponse<Task>>(`/tasks/admin/${taskId}`)
      );
      if (error) throw error;
      return data?.data.data;
    },
    enabled: !!taskId,
  });
}

/** DELETE /tasks/admin/:id */
export function useAdminDeleteTask() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (taskId: string) => {
      const { data, error } = await tryCatch(
        api.delete<ApiResponse<{ message: string }>>(
          `/tasks/admin/${taskId}`
        )
      );
      if (error) throw error;
      return data?.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: taskQueryKeys.adminAll });
      queryClient.invalidateQueries({ queryKey: taskQueryKeys.all });
    },
  });
}