import { useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/axios";
import { tryCatch } from "@/lib/trycatch";

// ─────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────

export type UserCreate = {
  email: string;
  username: string;
  password: string;
};

export type LoginUser = {
  email: string;
  password: string;
};

export type AuthUser = {
  id: string;
  email: string;
  username: string;
};

export type ApiResponse<T> = {
  data: T | null;
  error: string | null;
  message?: string;
};

// ─────────────────────────────────────────────
// Hooks
// ─────────────────────────────────────────────

/** POST /auth/sign-up/user */
export function useSignUpUser() {
  return useMutation({
    mutationFn: async (body: UserCreate) => {
      const { data, error } = await tryCatch(
        api.post<ApiResponse<AuthUser>>("/auth/sign-up/user", body)
      );
      if (error) throw error;
      return data?.data;
    },
  });
}

/** POST /auth/sign-up/admin */
export function useSignUpAdmin() {
  return useMutation({
    mutationFn: async (body: UserCreate) => {
      const { data, error } = await tryCatch(
        api.post<ApiResponse<AuthUser>>("/auth/sign-up/admin", body)
      );
      if (error) throw error;
      return data?.data;
    },
  });
}

/** POST /auth/login */
export function useLogin() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (body: LoginUser) => {
      const { data, error } = await tryCatch(
        api.post<ApiResponse<AuthUser>>("/auth/login", body)
      );
      if (error) throw error;
      return data?.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users", "me"] });
    },
  });
}

/** POST /auth/logout */
export function useLogout() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async () => {
      const { data, error } = await tryCatch(
        api.post<ApiResponse<{ message: string }>>("/auth/logout")
      );
      if (error) throw error;
      return data?.data;
    },
    onSuccess: () => {
      queryClient.clear();
    },
  });
}

/** GET /auth/refresh */
export function useRefreshToken() {
  return useMutation({
    mutationFn: async () => {
      const { data, error } = await tryCatch(
        api.get<ApiResponse<{ message: string }>>("/auth/refresh")
      );
      if (error) throw error;
      return data?.data;
    },
  });
}