import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/axios";
import { tryCatch } from "@/lib/trycatch";

// ─────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────

export type UserProfile = {
  id: string;
  email: string;
  username: string;
  role: string;
};

export type AdminUser = {
  id: string;
  email: string;
  username: string;
  role: string;
  is_active: boolean;
};

export type UserUpdate = {
  username: string;
};

export type ApiResponse<T> = {
  data: T | null;
  error: string | null;
  message?: string;
};

// ─────────────────────────────────────────────
// Query Keys
// ─────────────────────────────────────────────

export const userQueryKeys = {
  me: ["users", "me"] as const,
  adminAll: ["admin", "users"] as const,
  adminOne: (id: string) => ["admin", "users", id] as const,
};

// ─────────────────────────────────────────────
// User Hooks
// ─────────────────────────────────────────────

/** GET /users/me */
export function useGetMe() {
  return useQuery({
    queryKey: userQueryKeys.me,
    queryFn: async () => {
      const { data, error } = await tryCatch(
        api.get<ApiResponse<UserProfile>>("/users/me")
      );
      if (error) throw error;
      return data?.data.data;
    },
  });
}

/** PATCH /users/me */
export function useUpdateMe() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (body: UserUpdate) => {
      const { data, error } = await tryCatch(
        api.patch<ApiResponse<{ message: string }>>("/users/me", body)
      );
      if (error) throw error;
      return data?.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userQueryKeys.me });
    },
  });
}

/** DELETE /users/me */
export function useDeleteMe() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async () => {
      const { data, error } = await tryCatch(
        api.delete<ApiResponse<{ message: string }>>("/users/me")
      );
      if (error) throw error;
      return data?.data;
    },
    onSuccess: () => {
      queryClient.clear();
    },
  });
}

// ─────────────────────────────────────────────
// Admin — User Hooks
// ─────────────────────────────────────────────

/** GET /users/admin/all */
export function useAdminGetAllUsers() {
  return useQuery({
    queryKey: userQueryKeys.adminAll,
    queryFn: async () => {
      const { data, error } = await tryCatch(
        api.get<ApiResponse<AdminUser[]>>("/users/admin/all")
      );
      if (error) throw error;
      return data?.data.data;
    },
  });
}

/** GET /users/admin/:id */
export function useAdminGetUser(userId: string) {
  return useQuery({
    queryKey: userQueryKeys.adminOne(userId),
    queryFn: async () => {
      const { data, error } = await tryCatch(
        api.get<ApiResponse<UserProfile>>(`/users/admin/${userId}`)
      );
      if (error) throw error;
      return data?.data.data;
    },
    enabled: !!userId,
  });
}

/** DELETE /users/admin/:id */
export function useAdminDeleteUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (userId: string) => {
      const { data, error } = await tryCatch(
        api.delete<ApiResponse<{ message: string }>>(`/users/admin/${userId}`)
      );
      if (error) throw error;
      return data?.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userQueryKeys.adminAll });
    },
  });
}

/** PATCH /users/admin/:id/role */
export function useAdminUpdateUserRole() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({
      userId,
      role,
    }: {
      userId: string;
      role: "user" | "admin";
    }) => {
      const { data, error } = await tryCatch(
        api.patch<ApiResponse<UserProfile>>(
          `/users/admin/${userId}/role?role=${role}`
        )
      );
      if (error) throw error;
      return data?.data;
    },
    onSuccess: (_, { userId }) => {
      queryClient.invalidateQueries({ queryKey: userQueryKeys.adminAll });
      queryClient.invalidateQueries({ queryKey: userQueryKeys.adminOne(userId) });
    },
  });
}