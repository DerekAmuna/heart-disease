import * as React from 'react'

/**
 * IntroductionTab
 *
 * This component renders the landing page hero section,
 * feature cards, and dataset metrics placeholders.
 */
export const IntroductionTab: React.FC = () => {
  return (
    <section className="space-y-12">
      {/* Hero Section */}
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold">Heart Disease Data Dashboard</h1>
        <p className="text-lg text-muted-foreground">
          Explore global heart disease metrics through interactive visualizations,
          filters, and trend analysis.
        </p>
      </div>

      {/* Feature Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Placeholder cards */}
        <div className="p-6 bg-card rounded-lg shadow">
          <h3 className="text-xl font-semibold mb-2">Choropleth Map</h3>
          <p className="text-sm text-muted-foreground">
            Visualize heart disease prevalence across countries.
          </p>
        </div>
        <div className="p-6 bg-card rounded-lg shadow">
          <h3 className="text-xl font-semibold mb-2">Geo-Eco Analysis</h3>
          <p className="text-sm text-muted-foreground">
            Compare geographic and economic factors.
          </p>
        </div>
        <div className="p-6 bg-card rounded-lg shadow">
          <h3 className="text-xl font-semibold mb-2">Healthcare Insights</h3>
          <p className="text-sm text-muted-foreground">
            Correlate metrics with healthcare infrastructure.
          </p>
        </div>
        <div className="p-6 bg-card rounded-lg shadow">
          <h3 className="text-xl font-semibold mb-2">Trend Analysis</h3>
          <p className="text-sm text-muted-foreground">
            Track heart disease trends over time.
          </p>
        </div>
      </div>

      {/* Dataset Metrics */}
      <div className="space-y-4">
        <h2 className="text-2xl font-semibold">Dataset Metrics</h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <div className="p-4 bg-card rounded-lg text-center">
            <span className="text-3xl font-bold">194</span>
            <p className="text-sm text-muted-foreground">Countries</p>
          </div>
          <div className="p-4 bg-card rounded-lg text-center">
            <span className="text-3xl font-bold">1980–2021</span>
            <p className="text-sm text-muted-foreground">Years Covered</p>
          </div>
          <div className="p-4 bg-card rounded-lg text-center">
            <span className="text-3xl font-bold">50K+</span>
            <p className="text-sm text-muted-foreground">Data Points</p>
          </div>
        </div>
      </div>
    </section>
  )
}

export default IntroductionTab
