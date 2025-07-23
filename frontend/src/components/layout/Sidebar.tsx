import * as React from "react";
import { Button } from "@/components/ui/button";
import { X } from "lucide-react";

export type SidebarProps = {
  /** Whether the sidebar is currently open */
  isOpen: boolean;
  /** Toggle handler to open/close the sidebar */
  onToggle: () => void;
  /** Content to render inside the sidebar (e.g., filter panels) */
  children?: React.ReactNode;
};

/**
 * Sidebar component skeleton.
 * Renders a collapsible side panel with a toggle button.
 * TODO: Populate with filter controls and dynamic content.
 */
export const Sidebar: React.FC<SidebarProps> = ({
  isOpen,
  onToggle,
  children,
}) => {
  return (
    <>
      {/* Overlay behind sidebar when open */}
      {isOpen && (
        <div className="fixed inset-0 z-10 bg-black/50" onClick={onToggle} />
      )}

      <aside
        className={`fixed inset-y-0 left-0 z-20 flex w-64 flex-col bg-card p-4 shadow-lg transition-transform duration-200 ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        {/* Header with close button */}
        <div className="mb-4 flex justify-between items-center">
          <h2 className="text-lg font-semibold">Filters</h2>
          <Button
            variant="ghost"
            size="icon"
            onClick={onToggle}
            aria-label="Close sidebar"
          >
            <X className="h-5 w-5" />
          </Button>
        </div>

        {/* Filter content placeholder */}
        <div className="flex-1 overflow-y-auto space-y-4">
          {children ?? (
            <p className="text-sm text-muted-foreground">
              {/* TODO: Add filter controls here */}
              Sidebar filters will appear here.
            </p>
          )}
        </div>
      </aside>
    </>
  );
};

Sidebar.displayName = "Sidebar";
export default Sidebar;
