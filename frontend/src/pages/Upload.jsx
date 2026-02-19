/**
 * Upload Page
 * X-ray image upload and analysis interface
 */
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Upload, AlertCircle, FileImage, X } from "lucide-react";
import { inferenceAPI } from "../services/api";
import Disclaimer from "../components/Disclaimer";

const UploadPage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handleFileSelect = (e) => {
    const file = e.target.files[0];

    if (file) {
      // Validate file type
      const validTypes = ["image/jpeg", "image/jpg", "image/png"];
      if (!validTypes.includes(file.type)) {
        setError("Please upload a valid image file (JPEG, JPG, or PNG)");
        return;
      }

      // Validate file size (10MB max)
      if (file.size > 10 * 1024 * 1024) {
        setError("File size must be less than 10MB");
        return;
      }

      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setError("");
    }
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedFile) {
      setError("Please select a file to upload");
      return;
    }

    setLoading(true);
    setError("");
    setUploadProgress(0);

    try {
      const response = await inferenceAPI.predictPneumonia(
        selectedFile,
        (progressEvent) => {
          const progress = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total,
          );
          setUploadProgress(progress);
        },
      );

      // Navigate to results page with prediction data and original file
      navigate("/results", { 
        state: { 
          result: response.data,
          uploadedFile: selectedFile 
        } 
      });
    } catch (err) {
      console.error("Upload error:", err);
      setError(
        err.response?.data?.detail ||
          "Failed to analyze image. Please try again.",
      );
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="medical-container max-w-4xl">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Upload Chest X-Ray
          </h1>
          <p className="text-gray-600">
            Upload a chest X-ray image for pneumonia detection and
            classification
          </p>
        </div>

        <Disclaimer />

        <form onSubmit={handleSubmit} className="card">
          {error && (
            <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded flex items-center">
              <AlertCircle className="h-5 w-5 mr-2 flex-shrink-0" />
              <span className="text-sm">{error}</span>
            </div>
          )}

          {/* File Upload Area */}
          <div className="mb-6">
            {!selectedFile ? (
              <label
                htmlFor="file-upload"
                className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100 transition-colors"
              >
                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                  <Upload className="w-12 h-12 mb-4 text-gray-400" />
                  <p className="mb-2 text-sm text-gray-700">
                    <span className="font-semibold">Click to upload</span> or
                    drag and drop
                  </p>
                  <p className="text-xs text-gray-500">
                    JPEG, JPG or PNG (MAX. 10MB)
                  </p>
                </div>
                <input
                  id="file-upload"
                  name="file-upload"
                  type="file"
                  className="hidden"
                  accept="image/jpeg,image/jpg,image/png"
                  onChange={handleFileSelect}
                  disabled={loading}
                />
              </label>
            ) : (
              <div className="relative">
                <img
                  src={previewUrl}
                  alt="Preview"
                  className="w-full h-auto max-h-96 object-contain rounded-lg border border-gray-300"
                />
                {!loading && (
                  <button
                    type="button"
                    onClick={handleRemoveFile}
                    className="absolute top-2 right-2 p-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors"
                  >
                    <X className="h-5 w-5" />
                  </button>
                )}
                <div className="mt-3 flex items-center text-sm text-gray-600">
                  <FileImage className="h-5 w-5 mr-2" />
                  <span>{selectedFile.name}</span>
                  <span className="ml-2 text-gray-400">
                    ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
                  </span>
                </div>
              </div>
            )}
          </div>

          {/* Upload Progress */}
          {loading && (
            <div className="mb-6">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">
                  {uploadProgress < 100 ? "Uploading..." : "Analyzing..."}
                </span>
                <span className="text-sm font-medium text-medical-primary">
                  {uploadProgress}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-medical-primary h-2 rounded-full transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                ></div>
              </div>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={!selectedFile || loading}
            className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? "Analyzing..." : "Analyze X-Ray"}
          </button>
        </form>

        {/* Instructions */}
        <div className="card mt-6">
          <h3 className="font-semibold text-lg text-gray-900 mb-3">
            Upload Guidelines
          </h3>
          <ul className="space-y-2 text-sm text-gray-600">
            <li className="flex items-start">
              <span className="mr-2">•</span>
              <span>Ensure the X-ray image is clear and properly oriented</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">•</span>
              <span>Supported formats: JPEG, JPG, PNG</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">•</span>
              <span>Maximum file size: 10MB</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">•</span>
              <span>Analysis typically takes 5-10 seconds</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default UploadPage;
