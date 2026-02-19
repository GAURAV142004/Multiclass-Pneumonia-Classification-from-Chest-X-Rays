/**
 * Authentication Context
 * Manages user authentication state across the application
 */
import { createContext, useContext, useState, useEffect } from "react";
import { authAPI } from "../services/api";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Load user from localStorage on mount
  useEffect(() => {
    const token = localStorage.getItem("token");
    const savedUser = localStorage.getItem("user");

    if (token && savedUser) {
      try {
        setUser(JSON.parse(savedUser));
        setIsAuthenticated(true);
      } catch (error) {
        console.error("Error parsing saved user:", error);
        localStorage.removeItem("token");
        localStorage.removeItem("user");
      }
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      const response = await authAPI.login(email, password);

      if (response && response.access_token) {
        const { access_token, user } = response;

        localStorage.setItem("token", access_token);
        localStorage.setItem("user", JSON.stringify(user));

        setUser(user);
        setIsAuthenticated(true);

        return { success: true };
      } else {
        throw new Error("Invalid response from server");
      }
    } catch (error) {
      console.error("Login error:", error);
      return {
        success: false,
        message:
          error.response?.data?.detail || "Login failed. Please try again.",
      };
    }
  };

  const signup = async (email, password, fullName) => {
    try {
      const response = await authAPI.signup(email, password, fullName);

      if (response && response.access_token) {
        const { access_token, user } = response;

        localStorage.setItem("token", access_token);
        localStorage.setItem("user", JSON.stringify(user));

        setUser(user);
        setIsAuthenticated(true);

        return { success: true };
      } else {
        throw new Error("Invalid response from server");
      }
    } catch (error) {
      console.error("Signup error:", error);
      return {
        success: false,
        message:
          error.response?.data?.detail || "Signup failed. Please try again.",
      };
    }
  };

  const logout = () => {
    authAPI.logout();
    setUser(null);
    setIsAuthenticated(false);
  };

  const value = {
    user,
    loading,
    isAuthenticated,
    login,
    signup,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
};
