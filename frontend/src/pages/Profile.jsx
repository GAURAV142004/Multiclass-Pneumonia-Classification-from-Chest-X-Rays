/**
 * Profile Page
 * User profile and scan history
 */
import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { userAPI } from "../services/api";
import { User, Mail, Calendar, FileText } from "lucide-react";

const Profile = () => {
  const { user } = useAuth();
  const [scanHistory, setScanHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadScanHistory();
  }, []);

  const loadScanHistory = async () => {
    try {
      const response = await userAPI.getScanHistory(10);
      setScanHistory(response.history || []);
    } catch (error) {
      console.error("Error loading scan history:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="medical-container max-w-4xl">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Profile</h1>

        {/* User Info Card */}
        <div className="card mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            User Information
          </h2>

          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <User className="h-5 w-5 text-gray-400" />
              <div>
                <div className="text-sm text-gray-500">Full Name</div>
                <div className="font-medium text-gray-900">
                  {user?.full_name}
                </div>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <Mail className="h-5 w-5 text-gray-400" />
              <div>
                <div className="text-sm text-gray-500">Email</div>
                <div className="font-medium text-gray-900">{user?.email}</div>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <Calendar className="h-5 w-5 text-gray-400" />
              <div>
                <div className="text-sm text-gray-500">Member Since</div>
                <div className="font-medium text-gray-900">
                  {new Date(user?.created_at).toLocaleDateString()}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Scan History */}
        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
            <FileText className="h-6 w-6 mr-2" />
            Recent Scan History
          </h2>

          {loading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-medical-primary mx-auto"></div>
            </div>
          ) : scanHistory.length > 0 ? (
            <div className="space-y-3">
              {scanHistory.map((scan) => (
                <div
                  key={scan.id}
                  className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                >
                  <div>
                    <div className="font-semibold text-gray-900">
                      {scan.prediction_label}
                    </div>
                    <div className="text-sm text-gray-600">
                      {new Date(scan.created_at).toLocaleString()}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-semibold text-medical-primary">
                      {(scan.confidence * 100).toFixed(1)}%
                    </div>
                    <div className="text-sm text-gray-500">Confidence</div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              No scan history yet. Upload your first X-ray to get started.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Profile;
