export type UserRole = "USER" | "ADMIN" | "ANALYST";

export type AuthUser = {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
};

export type AuthResponse = {
  access_token: string;
  token_type: "bearer";
  expires_in: number;
  user: AuthUser;
};

export type RegisterPayload = {
  name: string;
  email: string;
  password: string;
};

export type LoginPayload = {
  email: string;
  password: string;
};