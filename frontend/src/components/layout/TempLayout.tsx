import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import IntroductionTab from '@/components/tabs/IntroductionTab';

// Temporary layout for testing Phase 3 components
const TempLayout: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-2xl font-bold text-gray-900 py-4">
            Heart Disease Data Explorer
          </h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Tabs defaultValue="introduction" className="w-full">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="introduction">Introduction</TabsTrigger>
            <TabsTrigger value="worldmap" disabled>World Map</TabsTrigger>
            <TabsTrigger value="geoeco" disabled>GEO-ECO</TabsTrigger>
            <TabsTrigger value="healthcare" disabled>Healthcare</TabsTrigger>
            <TabsTrigger value="trends" disabled>Trends</TabsTrigger>
          </TabsList>
          
          <TabsContent value="introduction" className="mt-6">
            <IntroductionTab />
          </TabsContent>
          
          <TabsContent value="worldmap" className="mt-6">
            <div className="text-center py-12 text-gray-500">
              World Map tab coming soon...
            </div>
          </TabsContent>
          
          {/* Other tabs will be implemented in later phases */}
        </Tabs>
      </main>
    </div>
  );
};

export default TempLayout;
