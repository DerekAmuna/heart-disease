import * as React from 'react'

/**
 * WorldMapTab
 *
 * Placeholder component for the Choropleth Visualization tab.
 * Renders a heading and descriptive text until the actual map is implemented.
 */
export const WorldMapTab: React.FC = () => {
  return (
    <section className="space-y-6">
      <h2 className="text-2xl font-semibold">Choropleth Visualization</h2>
      <p className="text-muted-foreground">
        This section will host an interactive world map (choropleth) showing
        heart disease metrics by country and year.
      </p>
      {/* TODO: Insert ChoroplethMap component with year slider once implemented */}
    </section>
  )
}

export default WorldMapTab
