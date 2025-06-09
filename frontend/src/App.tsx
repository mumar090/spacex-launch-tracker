import React from "react";
import LaunchList from "./components/LaunchList";
import StatisticsDashboard from "./components/StatisticsDashboard";

const App: React.FC = () => {
  return (
    <div className="p-6 space-y-12 bg-gray-100 min-h-screen" style={{ padding: 20 }}>
      <h1>SpaceX Launch Tracker</h1>
      <LaunchList />
      <StatisticsDashboard />
    </div>
  );
};

export default App;