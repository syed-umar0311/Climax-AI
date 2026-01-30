import { useEffect, useState } from "react";
import EmissionPrediction from "../components/EmissionPrediction";
import ForecastsConfiguration from "../components/ForecastsConfiguration";
import MonthlyTrends from "../components/MonthlyTrends";
import PredictionSkeleton from "../components/PredictionSkeleton";
import LLMResponse from "../components/LLMResponse";

export default function Prediction() {
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);

  useEffect(() => {
    fetchPrediction({
      country: "PAK",
      sector: "transportation",
      gas: "co2",
      year: 2025,
      month: 1,
    });
  }, []);

  const fetchPrediction = async (forecastConfiguration) => {
    setLoading(true);
    const endpoint = "http://127.0.0.1:5000/api/predict";
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(forecastConfiguration),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      setPrediction(data);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching historical data:", error);
    }
  };

  return (
    <div className="space-y-10 p-6 min-h-screen">
      <ForecastsConfiguration fetchPrediction={fetchPrediction} />

      {loading ? (
        <PredictionSkeleton />
      ) : (
        <>
          {prediction != null && <EmissionPrediction prediction={prediction} />}
          {prediction != null && <MonthlyTrends prediction={prediction} />}
          {prediction != null && <LLMResponse response={prediction.llm_insights} />}
        </>
      )}
    </div>
  );
}
