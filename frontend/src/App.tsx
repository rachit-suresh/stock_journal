import { useState } from "react";
import { Dashboard } from "./pages/Dashboard";
import { History } from "./pages/History";
import { LayoutDashboard, History as HistoryIcon } from "lucide-react";

function App() {
  const [activeTab, setActiveTab] = useState<"dashboard" | "history">(
    "dashboard"
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Tab Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            <button
              onClick={() => setActiveTab("dashboard")}
              className={`py-4 px-1 inline-flex items-center border-b-2 font-medium text-sm transition-colors ${
                activeTab === "dashboard"
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              }`}
            >
              <LayoutDashboard className="w-5 h-5 mr-2" />
              Active Trades
            </button>
            <button
              onClick={() => setActiveTab("history")}
              className={`py-4 px-1 inline-flex items-center border-b-2 font-medium text-sm transition-colors ${
                activeTab === "history"
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              }`}
            >
              <HistoryIcon className="w-5 h-5 mr-2" />
              History
            </button>
          </div>
        </div>
      </nav>

      {/* Content */}
      {activeTab === "dashboard" ? <Dashboard /> : <History />}
    </div>
  );
}

export default App;
