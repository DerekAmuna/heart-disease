import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';

interface FeatureCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  value?: string | number;
  color?: 'blue' | 'green' | 'yellow' | 'purple';
  className?: string;
}

const colorVariants = {
  blue: {
    card: 'border-blue-200 bg-blue-50 hover:bg-blue-100',
    icon: 'text-blue-600 bg-blue-100',
    title: 'text-blue-900',
    description: 'text-blue-700',
    value: 'text-blue-800'
  },
  green: {
    card: 'border-green-200 bg-green-50 hover:bg-green-100',
    icon: 'text-green-600 bg-green-100',
    title: 'text-green-900',
    description: 'text-green-700',
    value: 'text-green-800'
  },
  yellow: {
    card: 'border-yellow-200 bg-yellow-50 hover:bg-yellow-100',
    icon: 'text-yellow-600 bg-yellow-100',
    title: 'text-yellow-900',
    description: 'text-yellow-700',
    value: 'text-yellow-800'
  },
  purple: {
    card: 'border-purple-200 bg-purple-50 hover:bg-purple-100',
    icon: 'text-purple-600 bg-purple-100',
    title: 'text-purple-900',
    description: 'text-purple-700',
    value: 'text-purple-800'
  }
};

const FeatureCard: React.FC<FeatureCardProps> = ({
  title,
  description,
  icon,
  value,
  color = 'blue',
  className
}) => {
  const variant = colorVariants[color];

  return (
    <Card 
      className={cn(
        'transition-all duration-200 hover:shadow-md cursor-pointer',
        variant.card,
        className
      )}
    >
      <CardHeader className="pb-3">
        <div className="flex items-center gap-3">
          <div className={cn(
            'p-2 rounded-lg',
            variant.icon
          )}>
            {icon}
          </div>
          <CardTitle className={cn(
            'text-lg font-semibold',
            variant.title
          )}>
            {title}
          </CardTitle>
        </div>
      </CardHeader>
      <CardContent className="pt-0">
        <p className={cn(
          'text-sm mb-3',
          variant.description
        )}>
          {description}
        </p>
        {value && (
          <div className={cn(
            'text-2xl font-bold',
            variant.value
          )}>
            {typeof value === 'number' ? value.toLocaleString() : value}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default FeatureCard;
