/**
 * Results Page
 * Displays prediction results with images and confidence scores
 */
import { useState } from "react";
import { useLocation, useNavigate, Link } from "react-router-dom";
import { CheckCircle, AlertCircle, ArrowLeft, Download, ArrowRight } from "lucide-react";
import { inferenceAPI } from "../services/api";
import Disclaimer from "../components/Disclaimer";

const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const result = location.state?.result;
  const uploadedFile = location.state?.uploadedFile;

  const [currentResult, setCurrentResult] = useState(result);
  const [loadingStage2, setLoadingStage2] = useState(false);
  const [stage2Error, setStage2Error] = useState("");

  const handleProceedToStage2 = async () => {
    if (!uploadedFile) {
      setStage2Error("Original file not available. Please upload again.");
      return;
    }

    setLoadingStage2(true);
    setStage2Error("");

    try {
      const response = await inferenceAPI.predictPneumonia(uploadedFile, true);
      setCurrentResult(response.data);
    } catch (err) {
      console.error("Stage-2 error:", err);
      setStage2Error(
        err.response?.data?.detail || "Failed to run Stage-2 classification."
      );
    } finally {
      setLoadingStage2(false);
    }
  };

  if (!currentResult) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="medical-container max-w-4xl">
          <div className="card text-center">
            <AlertCircle className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              No Results Available
            </h2>
            <p className="text-gray-600 mb-6">
              Please upload an X-ray image to get started.
            </p>
            <Link to="/upload" className="btn-primary inline-block">
              Upload X-Ray
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const { prediction, images, disclaimer } = currentResult;
  const isNormal = prediction.label === "Normal";
  const isPneumonia = prediction.label.includes("Pneumonia");
  const pendingStage2 = prediction.pending_stage2 === true;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="medical-container max-w-6xl">
        {/* Back Button */}
        <button
          onClick={() => navigate("/upload")}
          className="mb-6 flex items-center text-medical-primary hover:text-medical-dark font-medium"
        >
          <ArrowLeft className="h-5 w-5 mr-1" />
          Back to Upload
        </button>

        {/* Results Header */}
        <div className="card mb-6">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-3xl font-bold text-gray-900">
              Analysis Results
            </h1>
            {isNormal ? (
              <CheckCircle className="h-12 w-12 text-green-500" />
            ) : (
              <AlertCircle className="h-12 w-12 text-yellow-500" />
            )}
          </div>

          {/* Prediction */}
          <div className="mb-4">
            <div className="flex items-baseline justify-between mb-2">
              <h2 className="text-2xl font-bold">
                <span
                  className={isNormal ? "text-green-600" : "text-yellow-600"}
                >
                  {prediction.label}
                </span>
              </h2>
              <span className="text-lg font-semibold text-gray-700">
                Confidence: {prediction.confidence}%
              </span>
            </div>

            {/* Stage Information */}
            <div className="text-sm text-gray-600">
              Classification Stage: {prediction.stage} of 2
            </div>
          </div>

          {/* Additional Probabilities */}
          {prediction.stage === 1 && (
            <div className="grid grid-cols-2 gap-4 mt-4">
              <div className="bg-green-50 p-4 rounded-lg">
                <div className="text-sm font-medium text-green-900 mb-1">
                  Normal Probability
                </div>
                <div className="text-2xl font-bold text-green-600">
                  {(prediction.normal_probability * 100).toFixed(1)}%
                </div>
              </div>
              <div className="bg-yellow-50 p-4 rounded-lg">
                <div className="text-sm font-medium text-yellow-900 mb-1">
                  Pneumonia Probability
                </div>
                <div className="text-2xl font-bold text-yellow-600">
                  {(prediction.pneumonia_probability * 100).toFixed(1)}%
                </div>
              </div>
            </div>
          )}

          {prediction.stage === 2 && (
            <div className="grid grid-cols-2 gap-4 mt-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="text-sm font-medium text-blue-900 mb-1">
                  Viral Probability
                </div>
                <div className="text-2xl font-bold text-blue-600">
                  {(prediction.viral_probability * 100).toFixed(1)}%
                </div>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <div className="text-sm font-medium text-purple-900 mb-1">
                  Bacterial Probability
                </div>
                <div className="text-2xl font-bold text-purple-600">
                  {(prediction.bacterial_probability * 100).toFixed(1)}%
                </div>
              </div>
            </div>
          )}

          {/* Stage-2 Confirmation Button */}
          {pendingStage2 && (
            <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-blue-900 mb-2">
                    Pneumonia Detected - Proceed to Classification?
                  </h3>
                  <p className="text-sm text-blue-800 mb-4">
                    Stage-1 has detected pneumonia in the X-ray. Would you like to proceed with Stage-2 classification to determine if it's Viral or Bacterial pneumonia?
                  </p>
                  {stage2Error && (
                    <div className="mb-4 text-sm text-red-600 flex items-center">
                      <AlertCircle className="h-4 w-4 mr-2" />
                      {stage2Error}
                    </div>
                  )}
                  <button
                    onClick={handleProceedToStage2}
                    disabled={loadingStage2}
                    className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                  >
                    {loadingStage2 ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                        Running Stage-2 Classification...
                      </>
                    ) : (
                      <>
                        Proceed to Stage-2
                        <ArrowRight className="ml-2 h-5 w-5" />
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Images Comparison */}
        <div className="card mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Image Analysis
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Original Image */}
            <div>
              <h3 className="font-semibold text-lg text-gray-900 mb-2">
                Original X-Ray
              </h3>
              <div className="bg-gray-100 rounded-lg p-4">
                <img
                  src={images.original}
                  alt="Original X-Ray"
                  className="w-full h-auto rounded"
                />
              </div>
            </div>

            {/* Segmented Image */}
            <div>
              <h3 className="font-semibold text-lg text-gray-900 mb-2">
                Lung Segmentation
              </h3>
              <div className="bg-gray-100 rounded-lg p-4">
                <img
                  src={images.segmented}
                  alt="Segmented Lungs"
                  className="w-full h-auto rounded"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Interpretation */}
        <div className="card mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Interpretation
          </h2>

          <div className="space-y-3 text-gray-700">
            {isNormal && (
              <p>
                The analysis indicates <strong>no pneumonia</strong> detected in
                the chest X-ray. The lung segmentation shows clear lung fields
                without significant abnormalities.
              </p>
            )}

            {isPneumonia && (
              <>
                <p>
                  The analysis has detected signs of{" "}
                  <strong>{prediction.label}</strong> in the chest X-ray with a
                  confidence level of {prediction.confidence}%.
                </p>

                {prediction.label === "Viral Pneumonia" && (
                  <p>
                    Viral pneumonia typically presents with more diffuse,
                    bilateral interstitial patterns. Treatment generally focuses
                    on supportive care and antiviral medications if appropriate.
                  </p>
                )}

                {prediction.label === "Bacterial Pneumonia" && (
                  <p>
                    Bacterial pneumonia often shows more localized consolidation
                    patterns. Treatment typically involves antibiotic therapy as
                    prescribed by a healthcare provider.
                  </p>
                )}
              </>
            )}
          </div>
        </div>

        {/* Disclaimer */}
        <Disclaimer />

        {/* Actions */}
        <div className="flex justify-center space-x-4 mt-6">
          <Link to="/upload" className="btn-primary">
            Analyze Another Image
          </Link>
          <Link to="/dashboard" className="btn-secondary">
            Back to Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Results;
