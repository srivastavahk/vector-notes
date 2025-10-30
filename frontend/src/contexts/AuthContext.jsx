import React, { createContext, useContext, useState, useEffect } from "react";
import { supabase } from "@/services/supabase";
import { useToast } from "@/contexts/ToastContext";
import { STORAGE_KEYS } from "@/utils/constants";

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const { addToast } = useToast();

  useEffect(() => {
    checkSession();

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((event, session) => {
      if (session) {
        setUser(session.user);
        sessionStorage.setItem(
          STORAGE_KEYS.SUPABASE_TOKEN,
          session.access_token,
        );
      } else {
        setUser(null);
        sessionStorage.removeItem(STORAGE_KEYS.SUPABASE_TOKEN);
      }
    });

    return () => subscription.unsubscribe();
  }, []);

  const checkSession = async () => {
    try {
      const {
        data: { session },
      } = await supabase.auth.getSession();
      if (session) {
        setUser(session.user);
        sessionStorage.setItem(
          STORAGE_KEYS.SUPABASE_TOKEN,
          session.access_token,
        );
      }
    } catch (error) {
      console.error("Session check failed:", error);
    } finally {
      setLoading(false);
    }
  };

  const signUp = async (email, password) => {
    try {
      const { data, error } = await supabase.auth.signUp({ email, password });
      if (error) throw error;

      addToast(
        "Account created successfully! Please check your email for verification.",
        "success",
      );
      return true;
    } catch (error) {
      addToast(error.message, "error");
      return false;
    }
  };

  const signIn = async (email, password) => {
    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });
      if (error) throw error;

      addToast("Welcome back!", "success");
      return true;
    } catch (error) {
      addToast(error.message, "error");
      return false;
    }
  };

  const signOut = async () => {
    try {
      await supabase.auth.signOut();
      addToast("Signed out successfully", "success");
    } catch (error) {
      addToast("Error signing out", "error");
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, signUp, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
};
