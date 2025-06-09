import React, { useEffect, useState } from "react";
import { fetchLaunches } from "../api";
import type { Launch } from "../api";

const LaunchList: React.FC = () => {
  const [launches, setLaunches] = useState<Launch[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
  const load = async () => {
    try {
      const data = await fetchLaunches();
      setLaunches(data ?? []);
    } catch (error) {
      console.error("Failed to load launches:", error);
    } finally {
      setLoading(false);
    }
  };
  load();
}, []);



  if (loading) return <p>Loading launches...</p>;

  return (
    <div className="bg-white p-4 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Launch Results</h2>
      <div className="overflow-auto max-h-[400px]">
        <table className="w-full text-sm text-left">
          <thead className="bg-gray-200">
            <tr>
              <th className="p-2">Name</th>
              <th className="p-2">Date</th>
              <th className="p-2">Rocket</th>
              <th className="p-2">Launchpad</th>
              <th className="p-2">Success</th>
            </tr>
          </thead>
          <tbody>
            {launches.map((launch) => (
              <tr key={launch.id} className="border-b hover:bg-gray-50">
                <td className="p-2">{launch.name}</td>
                <td className="p-2">{new Date(launch.date_utc).toLocaleDateString()}</td>
                {/* Uncomment and update these if you have rocket and launchpad info */}
                {/* <td className="p-2">{launch.rocket}</td> */}
                {/* <td className="p-2">{launch.launchpad}</td> */}
                <td className="p-2">{launch.success ? "✅" : "❌"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default LaunchList;
