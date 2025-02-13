# Heart Disease Data Visualization Dashboard

An interactive dashboard built with Dash and Plotly for visualizing global heart disease data trends and patterns.

## Features

### 1. Interactive Navigation
- **Collapsible Sidebar**: Filter data by:
  - Country
  - Region
  - Gender
  - World Income Level
- **Responsive Layout**: Automatically adjusts to screen size
- **Tab-based Navigation**: Easy access to different visualizations

### 2. Visualization Tabs

#### Choropleth Map 🌐
- Global choropleth visualization of heart disease data
- Year slider with animation feature
- Play/Pause functionality for time-series animation
- Interactive map with zoom and pan capabilities

#### GEO-ECO Features 💰
- Economic indicators and their correlation with heart disease
- Regional analysis and comparisons
- Trend analysis across income groups

#### Healthcare Features 🏥
- Healthcare system indicators
- Medical facility distribution
- Treatment accessibility metrics

#### Trends Analysis 📈
- Four-panel visualization layout
- Temporal trend analysis
- Comparative statistics
- Auto-scaling plots

## Project Structure

```
heart-disease/
├── application.py          # Main application entry point
├── components/
│   ├── common/            # Shared components
│   │   ├── filter_slider.py
│   │   ├── plots.py
│   │   └── year_slider.py
│   ├── tabs/              # Tab-specific components
│   │   ├── world_map.py
│   │   ├── geo_eco.py
│   │   ├── healthcare.py
│   │   └── trends.py
│   └── sidebar.py         # Sidebar component
└── .ebextensions/         # AWS Elastic Beanstalk configuration
```

## Technical Implementation

### Core Components
1. **Sidebar**
   - Collapsible design with smooth transitions
   - Toggle button for space efficiency
   - Responsive width adjustment (250px expanded, 60px collapsed)

2. **Year Slider**
   - Range: 1950-2023
   - Animation capabilities
   - 1-second interval for time series
   - Play/Pause controls

3. **Choropleth Map**
   - Clean interface without legends/menus
   - Interactive zoom and pan
   - Dynamic year-based updates
   - Optimized for performance

4. **Plot Layout**
   - Viewport-based sizing (37vh per plot)
   - Minimal padding for maximum space utilization
   - Two-row, two-column grid layout
   - Responsive design

### Key Features
- **Dynamic Content Loading**: Uses callbacks for efficient content updates
- **Responsive Design**: Adapts to different screen sizes
- **Performance Optimization**: Minimal redraws and efficient state management
- **User Experience**: Smooth transitions and intuitive controls

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python application.py
   ```

## Development Notes

### Callback Structure
- **Tab Navigation**: Dynamic content loading with loading states
- **Year Slider**: Interval-based updates for animation
- **Sidebar**: Toggle state management with transitions
- **Data Updates**: Real-time visualization updates

### Styling Approach
- Bootstrap-based responsive grid
- Custom CSS for transitions
- Viewport-based sizing
- Minimal padding for optimal space usage

## Deployment

The application is configured for AWS Elastic Beanstalk deployment with:
- Flask server configuration
- NGINX proxy settings
- Environment configurations
- Static file handling




App URL : [Heart Disease Visualisation](http://Heartdiseasedev-env-1.eba-kzx3p4pv.us-east-1.elasticbeanstalk.com)
