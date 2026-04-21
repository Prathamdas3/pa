import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { tasksApi } from "@/api/client";
import type { TaskCreate, TaskUpdate } from "@/api/types";

export function useTasks() {
	return useQuery({
		queryKey: ["tasks"],
		queryFn: async () => {
			const { data, error } = await tasksApi.getAll();
			if (error) throw error;
			return data?.data || [];
		},
	});
}

export function useTask(taskId: string) {
	return useQuery({
		queryKey: ["tasks", taskId],
		queryFn: async () => {
			const { data, error } = await tasksApi.getOne(taskId);
			if (error) throw error;
			return data?.data;
		},
		enabled: !!taskId,
	});
}

export function useCreateTask() {
	const queryClient = useQueryClient();
	return useMutation({
		mutationFn: async (task: TaskCreate) => {
			const { data, error } = await tasksApi.create(task);
			if (error) throw error;
			return data?.data;
		},
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ["tasks"] });
		},
	});
}

export function useUpdateTask() {
	const queryClient = useQueryClient();
	return useMutation({
		mutationFn: async ({
			taskId,
			data: taskData,
		}: {
			taskId: string;
			data: TaskUpdate;
		}) => {
			const { data, error } = await tasksApi.update(taskId, taskData);
			if (error) throw error;
			return data?.data;
		},
		onSuccess: (_, variables) => {
			queryClient.invalidateQueries({ queryKey: ["tasks"] });
			queryClient.invalidateQueries({ queryKey: ["tasks", variables.taskId] });
		},
	});
}

export function useDeleteTask() {
	const queryClient = useQueryClient();
	return useMutation({
		mutationFn: async (taskId: string) => {
			const { data, error } = await tasksApi.delete(taskId);
			if (error) throw error;
			return data?.data;
		},
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ["tasks"] });
		},
	});
}
