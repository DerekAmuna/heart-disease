import React, { useState } from "react";
import Header from "./Header";
import Sidebar from "./Sidebar";
import { Menu } from "lucide-react";
import IntroductionTab from "../tabs/IntroductionTab";
import WorldMapTab from "../tabs/WorldMapTab";
import GeoEcoTab from "../tabs/GeoEcoTab";
import HealthcareTab from "../tabs/HealthcareTab";
import TrendsTab from "../tabs/TrendsTab";

type LayoutProps = {};

/**
 * Layout component:
 * - Renders a top bar with a mobile menu button and navigation tabs.
 * - Shows a collapsible sidebar for filters.
 * - Wraps the main content area.
 */
export const Layout: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>("introduction");
  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(false);

  const handleTabChange = (tabId: string) => {
    setActiveTab(tabId);
    // Close sidebar on mobile when switching tabs
    setIsSidebarOpen(false);
  };

  const toggleSidebar = () => {
    setIsSidebarOpen((prev) => !prev);
  };

  return (
    <div className="flex h-screen flex-col">
      {/* Top bar: mobile menu toggle + header navigation */}
      <div className="flex items-center justify-between bg-card px-4 py-2 shadow-md">
        <button
          onClick={toggleSidebar}
          className="md:hidden"
          aria-label="Toggle sidebar"
        >
          <Menu className="h-6 w-6" />
        </button>
        <Header activeTab={activeTab} onTabChange={handleTabChange} />
      </div>

      <div className="flex flex-1">
        {/* Sidebar for filters */}
        <Sidebar isOpen={isSidebarOpen} onToggle={toggleSidebar}>
          {/* TODO: add filter panels here */}
        </Sidebar>

        {/* Main content */}
        <main className="flex-1 overflow-auto bg-background p-6">
          {activeTab === "introduction" && <IntroductionTab />}
          {activeTab === "worldmap" && <WorldMapTab />}
          {activeTab === "geoeco" && <GeoEcoTab />}
          {activeTab === "healthcare" && <HealthcareTab />}
          {activeTab === "trends" && <TrendsTab />}
        </main>
      </div>
    </div>
  );
};

export default Layout;
