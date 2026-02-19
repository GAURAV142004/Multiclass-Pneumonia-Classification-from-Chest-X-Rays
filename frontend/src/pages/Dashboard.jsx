/**
 * Dashboard Page
 * Main landing page after login
 */
import { useAuth } from "../context/AuthContext";
import { Upload, FileText, Activity, TrendingUp } from "lucide-react";
import { Link } from "react-router-dom";
import Disclaimer from "../components/Disclaimer";

const Dashboard = () => {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="medical-container">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome, {user?.full_name}
          </h1>
          <p className="text-gray-600">
            Two-Stage Explainable Pneumonia Detection and Classification System
          </p>
        </div>

        <Disclaimer />

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <Link
            to="/upload"
            className="card hover:shadow-lg transition-shadow cursor-pointer group"
          >
            <div className="flex items-center space-x-4">
              <div className="p-3 bg-medical-light rounded-lg group-hover:bg-medical-primary transition-colors">
                <Upload className="h-8 w-8 text-medical-primary group-hover:text-white" />
              </div>
              <div>
                <h3 className="font-semibold text-lg text-gray-900">
                  Upload X-Ray
                </h3>
                <p className="text-sm text-gray-600">
                  Analyze chest X-ray image
                </p>
              </div>
            </div>
          </Link>

          <Link
            to="/profile"
            className="card hover:shadow-lg transition-shadow cursor-pointer group"
          >
            <div className="flex items-center space-x-4">
              <div className="p-3 bg-green-100 rounded-lg group-hover:bg-green-500 transition-colors">
                <FileText className="h-8 w-8 text-green-600 group-hover:text-white" />
              </div>
              <div>
                <h3 className="font-semibold text-lg text-gray-900">
                  Scan History
                </h3>
                <p className="text-sm text-gray-600">View past analyses</p>
              </div>
            </div>
          </Link>

          <div className="card">
            <div className="flex items-center space-x-4">
              <div className="p-3 bg-purple-100 rounded-lg">
                <Activity className="h-8 w-8 text-purple-600" />
              </div>
              <div>
                <h3 className="font-semibold text-lg text-gray-900">
                  System Status
                </h3>
                <p className="text-sm text-green-600 font-medium">
                  All models online
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* How It Works */}
        <div className="card mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            How It Works
          </h2>

          <div className="space-y-6">
            {/* Stage 1 */}
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-10 h-10 bg-medical-primary text-white rounded-full flex items-center justify-center font-bold">
                1
              </div>
              <div>
                <h3 className="font-semibold text-lg text-gray-900 mb-1">
                  Lung Segmentation
                </h3>
                <p className="text-gray-600">
                  U-Net model identifies and isolates lung regions from the
                  chest X-ray image
                </p>
              </div>
            </div>

            {/* Stage 2 */}
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-10 h-10 bg-medical-primary text-white rounded-full flex items-center justify-center font-bold">
                2
              </div>
              <div>
                <h3 className="font-semibold text-lg text-gray-900 mb-1">
                  Binary Classification (Normal vs Pneumonia)
                </h3>
                <p className="text-gray-600">
                  ConvNeXt classifier determines if pneumonia is present in the
                  X-ray
                </p>
              </div>
            </div>

            {/* Stage 3 */}
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-10 h-10 bg-medical-primary text-white rounded-full flex items-center justify-center font-bold">
                3
              </div>
              <div>
                <h3 className="font-semibold text-lg text-gray-900 mb-1">
                  Pneumonia Classification (Viral vs Bacterial)
                </h3>
                <p className="text-gray-600">
                  If pneumonia detected, dual-input classifier identifies the
                  type using both original and segmented images
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="card">
            <h3 className="font-semibold text-lg text-gray-900 mb-3 flex items-center">
              <TrendingUp className="h-5 w-5 mr-2 text-medical-primary" />
              High Accuracy
            </h3>
            <p className="text-gray-600">
              Stage-1 accuracy exceeds 90%, with Stage-2 achieving 80-88%
              classification accuracy
            </p>
          </div>

          <div className="card">
            <h3 className="font-semibold text-lg text-gray-900 mb-3 flex items-center">
              <Activity className="h-5 w-5 mr-2 text-medical-primary" />
              Explainable AI
            </h3>
            <p className="text-gray-600">
              Visual segmentation masks and confidence scores provide
              transparency in predictions
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
