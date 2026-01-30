import Emission from "../components/Emission";
import Filters from "../components/Filters";
import DashboardVisualizations from "../components/DashboardVisualizations";
import EmissionsBySector from "../components/EmissionsBySector";
import { useEffect, useState } from "react";
import DashboardSkeleton from "../components/DashboardSkeleton";
import LLMResponse from "../components/LLMResponse";

export default function Dashboard() {
  const [historicalData, setHistoricalData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistoricalData({
      country: "PAK",
      sector_name: "transportation",
      gas_name: "co2",  
      start_year: 2020,
      end_year: 2024,
    });
  }, []);

  const fetchHistoricalData = async (filtersObject) => {
    setLoading(true);
    const endpoint = "http://127.0.0.1:5000/api/historical";
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(filtersObject),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      setHistoricalData(data);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching historical data:", error);
    }
  };

  return (
    <div className="space-y-10 p-6 min-h-screen">
      <Filters fetchHistoricalData={fetchHistoricalData} />
      {loading ? (
        <DashboardSkeleton />
      ) : (
        <>
          {historicalData != null && (
            <Emission historicalData={historicalData} />
          )}
          {historicalData != null && (
            <DashboardVisualizations historicalData={historicalData} />
          )}
          {historicalData != null && (
            <EmissionsBySector historicalData={historicalData} />
          )}
          {historicalData != null && (
            <LLMResponse response={historicalData.llm_insights} />
          )}
        </>
      )}
    </div>
  );
}
