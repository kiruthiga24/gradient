import React, { useState, useEffect } from 'react';
import { AlertTriangle, TrendingDown, Lightbulb, CheckCircle2 } from 'lucide-react';

interface AnalysisSummaryProps {
  summary: string;
  patterns: string[];
  recommendations: string[];
}

export const AnalysisSummary: React.FC<AnalysisSummaryProps> = ({ 
  summary, 
  patterns, 
  recommendations 
}) => {
  const [displayedText, setDisplayedText] = useState('');
  const [isTyping, setIsTyping] = useState(true);

  useEffect(() => {
    setDisplayedText('');
    setIsTyping(true);
    let index = 0;
    
    const interval = setInterval(() => {
      if (index < summary.length) {
        setDisplayedText(summary.slice(0, index + 1));
        index++;
      } else {
        setIsTyping(false);
        clearInterval(interval);
      }
    }, 15);

    return () => clearInterval(interval);
  }, [summary]);

  return (
    <div className="space-y-4">
      {/* AI Summary */}
      <div className="bg-card rounded-lg border border-border p-4">
        <div className="flex items-center gap-2 mb-3">
          <AlertTriangle className="h-4 w-4 text-warning" />
          <h3 className="text-sm font-semibold text-foreground">AI Analysis Summary</h3>
        </div>
        <p className={`text-sm text-muted-foreground leading-relaxed ${isTyping ? 'typing-cursor' : ''}`}>
          {displayedText}
        </p>
      </div>

      {/* Detected Patterns */}
      <div className="bg-card rounded-lg border border-border p-4">
        <div className="flex items-center gap-2 mb-3">
          <TrendingDown className="h-4 w-4 text-destructive" />
          <h3 className="text-sm font-semibold text-foreground">Detected Patterns</h3>
        </div>
        <ul className="space-y-2">
          {patterns.map((pattern, idx) => (
            <li key={idx} className="flex items-start gap-2 text-sm text-muted-foreground">
              <span className="text-destructive mt-1">•</span>
              <span>{pattern}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Recommendations */}
      <div className="bg-card rounded-lg border border-border p-4">
        <div className="flex items-center gap-2 mb-3">
          <Lightbulb className="h-4 w-4 text-warning" />
          <h3 className="text-sm font-semibold text-foreground">Recommendations</h3>
        </div>
        <ul className="space-y-2">
          {recommendations.map((rec, idx) => (
            <li key={idx} className="flex items-start gap-2 text-sm text-muted-foreground">
              <CheckCircle2 className="h-3.5 w-3.5 text-success mt-0.5 flex-shrink-0" />
              <span>{rec}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default AnalysisSummary;
