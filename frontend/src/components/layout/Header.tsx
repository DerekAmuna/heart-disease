import * as React from 'react'
import { Button } from '@/components/ui/button'

export type HeaderProps = {
  /** The id of the currently active tab */
  activeTab: string
  /** Callback when a tab is clicked */
  onTabChange: (tabId: string) => void
}

/** Define the five main navigation tabs */
const NAV_TABS: { id: string; label: string }[] = [
  { id: 'introduction', label: 'Introduction' },
  { id: 'worldmap', label: 'Choropleth' },
  { id: 'geoeco', label: 'GEO-ECO' },
  { id: 'healthcare', label: 'Healthcare' },
  { id: 'trends', label: 'Trends' },
]

/**
 * Header component:
 * Renders a horizontal nav of buttons for each main tab.
 */
export const Header: React.FC<HeaderProps> = ({ activeTab, onTabChange }) => {
  return (
    <header className="flex items-center justify-center bg-card px-6 py-4 shadow-md">
      {NAV_TABS.map(tab => (
        <Button
          key={tab.id}
          variant={activeTab === tab.id ? 'default' : 'ghost'}
          size="sm"
          onClick={() => onTabChange(tab.id)}
          className="capitalize"
        >
          {tab.label}
        </Button>
      ))}
    </header>
  )
}

Header.displayName = 'Header'
export default Header
