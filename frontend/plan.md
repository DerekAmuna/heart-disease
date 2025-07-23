# Heart Disease Data Visualization - Frontend Implementation Plan

## 📋 Project Overview

Recreate the existing Dash Plotly heart disease visualization dashboard using modern web technologies:
- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite
- **UI Library**: shadcn/ui (not shadcn-ui)
- **Styling**: Tailwind CSS
- **Visualizations**: Plotly.js
- **State Management**: Zustand
- **Data Fetching**: TanStack Query

## 🎯 Current Application Analysis

### Features to Recreate:
- **Navigation**: 5 main tabs (Introduction, Choropleth Visualization, GEO-ECO Features, Healthcare Features, Trends)
- **Sidebar**: Dynamic filters with cascading dropdowns
- **Data**: 194 countries, 1980-2021 timeframe, 50K+ data points
- **Visualizations**: Interactive choropleth maps, scatter plots, trend analysis
- **UI**: Clean, modern design with responsive layout

### Key Components:
1. **Header**: Navigation tabs with icons and active states
2. **Sidebar**: Collapsible filter panel with multiple dropdowns and sliders
3. **Introduction Tab**: Hero section with 4 feature cards and dataset metrics
4. **World Map Tab**: Interactive choropleth map with year slider
5. **Analysis Tabs**: GeoEco, Healthcare, and Trends visualizations

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/                     # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dropdown.tsx
│   │   │   ├── slider.tsx
│   │   │   └── ...
│   │   ├── layout/
│   │   │   ├── Header.tsx          # Navigation tabs
│   │   │   ├── Sidebar.tsx         # Filter sidebar
│   │   │   └── Layout.tsx          # Main layout wrapper
│   │   ├── tabs/
│   │   │   ├── IntroductionTab.tsx # Landing page with cards
│   │   │   ├── WorldMapTab.tsx     # Choropleth visualization
│   │   │   ├── GeoEcoTab.tsx       # Economic analysis
│   │   │   ├── HealthcareTab.tsx   # Healthcare insights
│   │   │   └── TrendsTab.tsx       # Trend analysis
│   │   ├── visualizations/
│   │   │   ├── ChoroplethMap.tsx   # Plotly choropleth
│   │   │   ├── ScatterPlot.tsx     # Scatter visualizations
│   │   │   ├── LineChart.tsx       # Trend charts
│   │   │   └── Chart.tsx           # Base chart component
│   │   ├── filters/
│   │   │   ├── YearSlider.tsx      # Year range selector
│   │   │   ├── MetricDropdown.tsx  # Metric selection
│   │   │   ├── RegionFilter.tsx    # Region/Country cascade
│   │   │   └── FilterPanel.tsx     # Combined filters
│   │   └── common/
│   │       ├── FeatureCard.tsx     # Reusable card component
│   │       ├── LoadingSpinner.tsx  # Loading states
│   │       └── ErrorBoundary.tsx   # Error handling
│   ├── hooks/
│   │   ├── useData.ts              # Data fetching hook
│   │   ├── useFilters.ts           # Filter state hook
│   │   └── useVisualization.ts     # Chart logic hook
│   ├── lib/
│   │   ├── utils.ts                # Utility functions
│   │   ├── data.ts                 # Data processing
│   │   └── constants.ts            # App constants
│   ├── stores/
│   │   ├── filterStore.ts          # Zustand filter state
│   │   └── dataStore.ts            # Zustand data cache
│   ├── types/
│   │   ├── data.ts                 # Data type definitions
│   │   ├── filters.ts              # Filter type definitions
│   │   └── index.ts                # Exported types
│   ├── styles/
│   │   └── globals.css             # Global styles
│   ├── App.tsx                     # Main app component
│   └── main.tsx                    # Entry point
├── public/
│   ├── data/
│   │   ├── heart_processed.csv     # Main dataset
│   │   └── trends.csv              # Trends data
│   └── favicon.ico
├── package.json
├── vite.config.ts
├── tailwind.config.js
├── tsconfig.json
└── README.md
```

## 🔧 Technical Architecture

### State Management
```typescript
// Filter State Structure
interface FilterState {
  year: number;
  metric: string;
  gender: 'Both' | 'Male' | 'Female';
  region: string[];
  country: string[];
  income: string[];
  age: string;
  topN: number;
  activeTab: string;
}
```

### Data Types
```typescript
interface HeartDiseaseData {
  Entity: string;
  Code: string;
  Year: number;
  Region: string;
  WB_Income: string;
  // Dynamic metric columns
  [key: string]: string | number;
}
```

### Key Dependencies
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.0.0",
    "@radix-ui/react-select": "^1.2.0",
    "@radix-ui/react-slider": "^1.1.0",
    "@radix-ui/react-tabs": "^1.0.0",
    "tailwindcss": "^3.3.0",
    "plotly.js": "^2.26.0",
    "react-plotly.js": "^2.6.0",
    "papaparse": "^5.4.1",
    "@tanstack/react-query": "^4.29.0",
    "zustand": "^4.3.0",
    "lucide-react": "^0.263.0",
    "clsx": "^1.2.1",
    "tailwind-merge": "^1.13.0"
  }
}
```

## 📅 Implementation Phases

### Phase 1: Project Setup & Foundation (Day 1)
- [x] Create Vite + React + TypeScript project
- [x] Install and configure shadcn/ui
- [x] Set up Tailwind CSS configuration
- [x] Create basic project structure
- [x] Configure development environment

### Phase 2: Core Architecture (Day 1-2)
- [ ] Set up Zustand stores for state management
- [ ] Create data loading utilities with Papa Parse
- [ ] Build Layout component with Header and Sidebar
- [ ] Implement basic tab navigation
- [ ] Set up TanStack Query for data fetching

### Phase 3: UI Components (Day 2-3)
- [ ] Create shadcn/ui base components
- [ ] Build reusable FeatureCard component
- [ ] Implement Introduction tab with hero section
- [ ] Create dataset metrics display
- [ ] Add responsive design breakpoints

### Phase 4: Filter System (Day 3-4)
- [ ] Build Sidebar component with collapsible functionality
- [ ] Implement cascading Region → Country dropdowns
- [ ] Create YearSlider with range selection
- [ ] Add MetricDropdown with dynamic options
- [ ] Connect filters to global state

### Phase 5: Visualizations (Day 4-6)
- [ ] Integrate Plotly.js for choropleth maps
- [ ] Build ChoroplethMap component with interactions
- [ ] Implement WorldMapTab with filtering
- [ ] Add hover tooltips and click interactions
- [ ] Create base Chart component for reusability

### Phase 6: Advanced Features (Day 6-8)
- [ ] Build GeoEcoTab with scatter plots
- [ ] Implement HealthcareTab with comparative charts
- [ ] Create TrendsTab with time series visualizations
- [ ] Add advanced filtering capabilities
- [ ] Optimize performance with memoization

### Phase 7: Polish & Enhancement (Day 8-10)
- [ ] Add loading states and skeleton loaders
- [ ] Implement error boundaries and handling
- [ ] Responsive design refinements
- [ ] Performance optimization
- [ ] Testing and documentation

## 🎨 Design System

### Color Scheme
- **Primary**: Blue (#3B82F6) for main navigation and primary actions
- **Success**: Green (#10B981) for positive metrics
- **Info**: Light Blue (#06B6D4) for informational content
- **Warning**: Yellow (#F59E0B) for trends and analytics
- **Secondary**: Gray shades for text and backgrounds

### Typography
- **Headers**: Inter font family, bold weights
- **Body**: Inter font family, regular weights
- **Code**: JetBrains Mono for data displays

### Layout
- **Grid**: 12-column responsive grid system
- **Spacing**: Tailwind's spacing scale (4px base unit)
- **Breakpoints**: sm (640px), md (768px), lg (1024px), xl (1280px)

## 🚀 Performance Considerations

1. **Code Splitting**: Lazy load tab components
2. **Data Optimization**: Client-side caching with TanStack Query
3. **Rendering**: Memoize expensive calculations
4. **Bundle Size**: Tree-shake unused Plotly.js modules
5. **Loading**: Progressive data loading for large datasets

## 🔍 Development Guidelines

### Code Style
- **TypeScript**: Strict mode enabled
- **ESLint**: Airbnb configuration
- **Prettier**: Code formatting
- **Imports**: Absolute imports with path mapping

### Component Patterns
- **Composition**: Prefer composition over inheritance
- **Hooks**: Custom hooks for business logic
- **Props**: Strict TypeScript interfaces
- **State**: Local state for UI, global for data

### Testing Strategy
- **Unit Tests**: Vitest for utilities and hooks
- **Component Tests**: React Testing Library
- **E2E Tests**: Playwright for critical user flows
- **Visual Tests**: Storybook for component documentation

## 📊 Data Strategy

### Data Processing
1. **Loading**: Parse CSV files with Papa Parse
2. **Filtering**: Client-side filtering for responsiveness
3. **Caching**: Memory cache with TTL for processed data
4. **Optimization**: Debounced filter updates

### API Design (Future)
```typescript
// Potential API endpoints for server-side processing
GET /api/data/countries          // Country list
GET /api/data/metrics           // Available metrics
GET /api/data/heart-disease     // Filtered dataset
GET /api/data/trends            // Trend analysis
```

## ✅ Success Criteria

- [ ] **Functionality**: All original features recreated
- [ ] **Performance**: < 3s initial load time
- [ ] **Responsive**: Works on mobile, tablet, desktop
- [ ] **Accessibility**: WCAG 2.1 AA compliance
- [ ] **Type Safety**: 100% TypeScript coverage
- [ ] **Testing**: > 80% code coverage
- [ ] **Bundle Size**: < 2MB initial bundle

## 🎯 Next Steps

1. **Start Implementation**: Begin with Phase 1 setup
2. **Regular Reviews**: Daily progress check-ins
3. **User Testing**: Gather feedback on UI/UX
4. **Performance Monitoring**: Track metrics throughout development
5. **Documentation**: Maintain comprehensive README

---

**Last Updated**: 2024-01-19
**Version**: 1.0
**Status**: Ready for Implementation
