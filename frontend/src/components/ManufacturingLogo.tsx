import React from 'react';

interface ManufacturingLogoProps {
  className?: string;
  size?: number;
}

export const ManufacturingLogo: React.FC<ManufacturingLogoProps> = ({ 
  className = '', 
  size = 32 
}) => {
  return (
    <svg 
      width={size} 
      height={size} 
      viewBox="0 0 48 48" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* Factory building */}
      <rect x="4" y="28" width="12" height="16" rx="1" fill="currentColor" opacity="0.9"/>
      <rect x="18" y="20" width="12" height="24" rx="1" fill="currentColor" opacity="0.8"/>
      <rect x="32" y="24" width="12" height="20" rx="1" fill="currentColor" opacity="0.7"/>
      
      {/* Chimneys */}
      <rect x="6" y="22" width="3" height="8" rx="0.5" fill="currentColor"/>
      <rect x="11" y="24" width="3" height="6" rx="0.5" fill="currentColor"/>
      <rect x="22" y="12" width="4" height="10" rx="0.5" fill="currentColor"/>
      
      {/* Chart line overlay */}
      <path 
        d="M4 36 L12 32 L20 38 L28 28 L36 30 L44 22" 
        stroke="hsl(var(--primary))" 
        strokeWidth="2.5" 
        strokeLinecap="round" 
        strokeLinejoin="round"
        fill="none"
      />
      
      {/* Data points */}
      <circle cx="12" cy="32" r="2" fill="hsl(var(--primary))"/>
      <circle cx="28" cy="28" r="2" fill="hsl(var(--primary))"/>
      <circle cx="44" cy="22" r="2" fill="hsl(var(--primary))"/>
      
      {/* Gear accent */}
      <circle cx="40" cy="8" r="5" stroke="currentColor" strokeWidth="1.5" fill="none" opacity="0.5"/>
      <circle cx="40" cy="8" r="2" fill="currentColor" opacity="0.5"/>
    </svg>
  );
};

export default ManufacturingLogo;
