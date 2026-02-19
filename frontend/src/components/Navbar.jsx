/**
 * Navigation Bar Component
 * Medical-grade header with authentication controls
 */
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Activity, LogOut, User } from "lucide-react";

const Navbar = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="bg-white shadow-md border-b border-gray-200">
      <div className="medical-container">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <Activity className="h-8 w-8 text-medical-primary" />
            <span className="text-xl font-bold text-gray-900">
              Pneumonia Detection System
            </span>
          </Link>

          {/* Navigation */}
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <Link
                  to="/dashboard"
                  className="text-gray-700 hover:text-medical-primary font-medium transition-colors"
                >
                  Dashboard
                </Link>
                <Link
                  to="/upload"
                  className="text-gray-700 hover:text-medical-primary font-medium transition-colors"
                >
                  Upload X-Ray
                </Link>
                <Link
                  to="/profile"
                  className="flex items-center space-x-1 text-gray-700 hover:text-medical-primary transition-colors"
                >
                  <User className="h-5 w-5" />
                  <span className="font-medium">
                    {user?.full_name || "Profile"}
                  </span>
                </Link>
                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-1 text-red-600 hover:text-red-700 font-medium transition-colors"
                >
                  <LogOut className="h-5 w-5" />
                  <span>Logout</span>
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="text-gray-700 hover:text-medical-primary font-medium transition-colors"
                >
                  Login
                </Link>
                <Link to="/signup" className="btn-primary">
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
