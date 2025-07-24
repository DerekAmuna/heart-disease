// Component type definitions for Phase 3

export interface FeatureCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  value?: string | number;
  color?: 'blue' | 'green' | 'yellow' | 'purple';
  className?: string;
}

export interface DatasetMetrics {
  total_countries: number;
  total_years: number;
  data_points: number;
  latest_year: number;
}

export interface IntroductionData {
  hero: {
    title: string;
    subtitle: string;
    description: string;
  };
  features: FeatureCardProps[];
  metrics: DatasetMetrics;
}

// Color variant type for consistent theming
export type ColorVariant = 'blue' | 'green' | 'yellow' | 'purple';
