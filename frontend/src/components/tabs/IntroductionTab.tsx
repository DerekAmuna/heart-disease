import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import FeatureCard from '@/components/common/FeatureCard';
import { Globe, Heart, TrendingUp, Users, MapPin, BarChart3, Activity, Clock } from 'lucide-react';
import type { FeatureCardProps, DatasetMetrics } from '@/types/components';

// Mock data - will be replaced when Phase 2 state management is integrated
const FEATURE_CARDS_DATA: FeatureCardProps[] = [
  {
    title: 'Global Coverage',
    description: 'Comprehensive data from 194 countries worldwide, providing a truly global perspective on heart disease patterns and mortality rates.',
    icon: <Globe className="w-5 h-5" />,
    value: '194 Countries',
    color: 'blue'
  },
  {
    title: 'Health Impact',
    description: 'Tracking cardiovascular disease mortality rates and their relationship with socioeconomic and demographic factors.',
    icon: <Heart className="w-5 h-5" />,
    value: 'CVD Analysis',
    color: 'green'
  },
  {
    title: 'Long-term Trends',
    description: 'Four decades of data (1980-2021) revealing long-term patterns, health transitions, and epidemiological changes globally.',
    icon: <TrendingUp className="w-5 h-5" />,
    value: '42 Years',
    color: 'yellow'
  },
  {
    title: 'Demographic Insights',
    description: 'Age-standardized mortality rates with gender-specific insights across different income levels and geographic regions.',
    icon: <Users className="w-5 h-5" />,
    value: 'Multi-dimensional',
    color: 'purple'
  }
];

const DATASET_METRICS: DatasetMetrics = {
  total_countries: 194,
  total_years: 42,
  data_points: 50284,
  latest_year: 2021
};

const NAVIGATION_FEATURES = [
  { icon: <MapPin className="w-4 h-4" />, label: 'World Map Visualization', color: 'bg-blue-100 text-blue-800' },
  { icon: <BarChart3 className="w-4 h-4" />, label: 'Economic Analysis', color: 'bg-green-100 text-green-800' },
  { icon: <Activity className="w-4 h-4" />, label: 'Healthcare Insights', color: 'bg-yellow-100 text-yellow-800' },
  { icon: <Clock className="w-4 h-4" />, label: 'Trend Analysis', color: 'bg-purple-100 text-purple-800' }
];

/**
 * IntroductionTab - Enhanced landing page component
 * 
 * Features:
 * - Hero section with compelling copy
 * - Interactive feature cards highlighting key capabilities
 * - Dataset metrics with visual hierarchy
 * - Navigation hints with icons
 * - Responsive design across all breakpoints
 * - Accessible and keyboard navigable
 */
const IntroductionTab: React.FC = () => {
  return (
    <section className="space-y-12 p-6 max-w-7xl mx-auto">
      {/* Hero Section */}
      <div className="text-center space-y-6">
        <div className="space-y-4">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 leading-tight">
            Global Heart Disease Data Explorer
          </h1>
          <p className="text-xl text-gray-600 max-w-4xl mx-auto leading-relaxed">
            Explore comprehensive cardiovascular disease mortality data spanning four decades 
            across 194 countries. Discover patterns, trends, and relationships between heart 
            disease and socioeconomic factors worldwide.
          </p>
        </div>
        
        <div className="flex flex-wrap justify-center gap-2 text-sm text-gray-500">
          <span className="flex items-center gap-1">
            <Globe className="w-4 h-4" />
            Global Dataset
          </span>
          <Separator orientation="vertical" className="h-4" />
          <span className="flex items-center gap-1">
            <Clock className="w-4 h-4" />
            1980-2021
          </span>
          <Separator orientation="vertical" className="h-4" />
          <span className="flex items-center gap-1">
            <BarChart3 className="w-4 h-4" />
            Interactive Visualizations
          </span>
        </div>
      </div>

      {/* Feature Cards Grid */}
      <div className="space-y-6">
        <h2 className="text-2xl font-semibold text-center text-gray-800">
          Explore Key Features
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {FEATURE_CARDS_DATA.map((feature, index) => (
            <FeatureCard
              key={index}
              title={feature.title}
              description={feature.description}
              icon={feature.icon}
              value={feature.value}
              color={feature.color}
            />
          ))}
        </div>
      </div>

      {/* Dataset Metrics */}
      <Card className="bg-gradient-to-r from-blue-50 via-indigo-50 to-purple-50 border-blue-200">
        <CardHeader className="text-center">
          <CardTitle className="text-3xl text-blue-900 mb-2">
            Dataset Overview
          </CardTitle>
          <CardDescription className="text-lg text-blue-700">
            Comprehensive statistics about our global heart disease dataset
          </CardDescription>
        </CardHeader>
        <CardContent className="pt-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="text-center space-y-2">
              <div className="text-4xl font-bold text-blue-800">
                {DATASET_METRICS.total_countries.toLocaleString()}
              </div>
              <div className="text-sm text-blue-600 font-medium uppercase tracking-wide">
                Countries
              </div>
            </div>
            <div className="text-center space-y-2">
              <div className="text-4xl font-bold text-green-800">
                {DATASET_METRICS.total_years}
              </div>
              <div className="text-sm text-green-600 font-medium uppercase tracking-wide">
                Years of Data
              </div>
            </div>
            <div className="text-center space-y-2">
              <div className="text-4xl font-bold text-yellow-800">
                {DATASET_METRICS.data_points.toLocaleString()}+
              </div>
              <div className="text-sm text-yellow-600 font-medium uppercase tracking-wide">
                Data Points
              </div>
            </div>
            <div className="text-center space-y-2">
              <div className="text-4xl font-bold text-purple-800">
                {DATASET_METRICS.latest_year}
              </div>
              <div className="text-sm text-purple-600 font-medium uppercase tracking-wide">
                Latest Year
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Navigation Hints */}
      <div className="text-center space-y-6">
        <div className="space-y-3">
          <h3 className="text-2xl font-semibold text-gray-800">
            Explore Different Perspectives
          </h3>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Navigate through the tabs above to explore different aspects of the global heart disease data
          </p>
        </div>
        
        <div className="flex flex-wrap justify-center gap-4">
          {NAVIGATION_FEATURES.map((feature, index) => (
            <div
              key={index}
              className={`flex items-center gap-2 px-4 py-2 rounded-full font-medium transition-all hover:shadow-md cursor-pointer ${feature.color}`}
            >
              {feature.icon}
              {feature.label}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default IntroductionTab;
