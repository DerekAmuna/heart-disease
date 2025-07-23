import * as React from 'react'

/**
 * HealthcareTab
 *
 * Placeholder component for the Healthcare Features tab.
 * Will display comparative charts relating healthcare metrics
 * (e.g., hospital beds, physicians per capita) to heart disease rates.
 */
export const HealthcareTab: React.FC = () => {
  return (
    <section className="space-y-6">
      <h2 className="text-2xl font-semibold">Healthcare Features</h2>
      <p className="text-muted-foreground">
        This section will host comparative charts of healthcare infrastructure
        metrics against heart disease prevalence.
      </p>
      {/* TODO: Insert healthcare-related Chart components once implemented */}
    </section>
  )
}

export default HealthcareTab
