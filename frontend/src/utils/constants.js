export const APP_CONFIG = {
  name: import.meta.env.VITE_APP_NAME || "NotesApp",
  version: import.meta.env.VITE_APP_VERSION || "1.0.0",
};

export const TOAST_TYPES = {
  SUCCESS: "success",
  ERROR: "error",
  INFO: "info",
  WARNING: "warning",
};

export const STORAGE_KEYS = {
  SUPABASE_TOKEN: "supabase_token",
};

export const ROUTES = {
  HOME: "/",
  DASHBOARD: "/dashboard",
  AUTH: "/auth",
};
