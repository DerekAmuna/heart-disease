import * as React from 'react'

/**
 * TrendsTab
 *
 * Placeholder component for the Trends tab.
 * Will display time series charts showing trends in heart disease metrics over time.
 */
export const TrendsTab: React.FC = () => {
  return (
    <section className="space-y-6">
      <h2 className="text-2xl font-semibold">Trend Analysis</h2>
      <p className="text-muted-foreground">
        This section will host time series visualizations of heart disease metrics
        across different countries and metrics over time.
      </p>
      {/* TODO: Insert LineChart or other trend chart components once implemented */}
    </section>
  )
}

export default TrendsTab
