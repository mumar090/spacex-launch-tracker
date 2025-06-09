import React, { useEffect, useState } from "react";
import { Bar, Pie, Line } from "react-chartjs-2";
import { Chart, registerables } from "chart.js";
import { fetchStatistics } from "../api";
import type { StatisticsResponse } from "../api";

Chart.register(...registerables);

const StatisticsDashboard: React.FC = () => {
  const [stats, setStats] = useState<StatisticsResponse | null>(null);

  useEffect(() => {
    const loadData = async () => {
      const data = await fetchStatistics();
      setStats(data);
    };
    loadData();
  }, []);

  if (!stats) return <p>Loading statistics...</p>;

  const rocketSuccessData = {
    labels: Object.keys(stats.success_rate_by_rocket),
    datasets: [
      {
        label: "Success Rate (%)",
        data: Object.values(stats.success_rate_by_rocket),
        backgroundColor: "rgba(54, 162, 235, 0.6)",
      },
    ],
  };

  const launchpadData = {
    labels: Object.keys(stats.launch_count_by_launchpad),
    datasets: [
      {
        label: "Launch Count",
        data: Object.values(stats.launch_count_by_launchpad),
        backgroundColor: [
          "rgba(255, 99, 132, 0.6)",
          "rgba(255, 206, 86, 0.6)",
          "rgba(75, 192, 192, 0.6)",
          "rgba(153, 102, 255, 0.6)",
        ],
      },
    ],
  };

  const frequencyData = {
    labels: Object.keys(stats.launch_frequency.monthly ?? {}),
    datasets: [
      {
        label: "Launches Per Month",
        data: Object.values(stats.launch_frequency.monthly ?? {}),
        borderColor: "rgba(255, 99, 132, 1)",
        fill: false,
      },
    ],
  };

  return (
    <div className="p-4 space-y-10">
      <h2 className="text-2xl font-bold mb-4">Launch Statistics</h2>

      <div className="shadow-lg p-4 rounded-lg bg-white">
        <h3 className="text-xl font-semibold mb-2">Success Rate by Rocket</h3>
        <Bar data={rocketSuccessData} />
      </div>

      <div className="shadow-lg p-4 rounded-lg bg-white">
        <h3 className="text-xl font-semibold mb-2">Launch Count by Launchpad</h3>
        <Pie data={launchpadData} />
      </div>

      <div className="shadow-lg p-4 rounded-lg bg-white">
        <h3 className="text-xl font-semibold mb-2">Launch Frequency (Monthly)</h3>
        <Line data={frequencyData} />
      </div>
    </div>
  );
};

export default StatisticsDashboard;