import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { authApi, usersApi } from "@/api/client";
import type { LoginUser, UserCreate } from "@/api/types";

export function useUser() {
	return useQuery({
		queryKey: ["user"],
		queryFn: async () => {
			const { data, error } = await usersApi.getMe();
			if (error) throw error;
			return data?.data;
		},
		retry: false,
	});
}

export function useLogin() {
	const queryClient = useQueryClient();
	return useMutation({
		mutationFn: async (credentials: LoginUser) => {
			const { data, error } = await authApi.login(credentials);
			if (error) throw error;
			return data?.data;
		},
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ["user"] });
		},
	});
}

export function useSignUp() {
	const queryClient = useQueryClient();
	return useMutation({
		mutationFn: async (user: UserCreate) => {
			const { data, error } = await authApi.signUpUser(user);
			if (error) throw error;
			return data?.data;
		},
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ["user"] });
		},
	});
}

export function useLogout() {
	const queryClient = useQueryClient();
	return useMutation({
		mutationFn: async () => {
			const { data, error } = await authApi.logout();
			if (error) throw error;
			return data?.data;
		},
		onSuccess: () => {
			queryClient.setQueryData(["user"], null);
			queryClient.clear();
		},
	});
}
