import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  FileText, 
  Presentation, 
  Download, 
  Edit, 
  ChevronLeft, 
  ChevronRight,
  ZoomIn,
  ZoomOut,
  Maximize2
} from 'lucide-react';

interface DocumentViewerProps {
  onEdit?: () => void;
  onDownload?: (format: string) => void;
}

export const DocumentViewer: React.FC<DocumentViewerProps> = ({ onEdit, onDownload }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [zoom, setZoom] = useState(100);
  const totalPages = 5;

  const pptSlides = [
    { 
      title: 'Account Health Overview', 
      content: 'Q4 Performance Analysis',
      bullets: ['Order trends declining', 'Support tickets increasing', 'Action plan required']
    },
    { 
      title: 'Key Metrics Summary', 
      content: 'Manufacturing KPIs',
      bullets: ['Production output: -8.2%', 'Defect rate: +77.8%', 'Equipment uptime: 87%']
    },
    { 
      title: 'Root Cause Analysis', 
      content: 'Primary Factors Identified',
      bullets: ['Supply chain disruption', 'Quality control gaps', 'Staffing challenges']
    },
    { 
      title: 'Recommended Actions', 
      content: 'Immediate Steps',
      bullets: ['Stakeholder meeting', 'Process audit', 'Recovery plan implementation']
    },
    { 
      title: 'Timeline & Resources', 
      content: 'Implementation Schedule',
      bullets: ['Week 1-2: Assessment', 'Week 3-4: Implementation', 'Week 5+: Monitoring']
    },
  ];

  const currentSlide = pptSlides[currentPage - 1];

  return (
    <div className="bg-card rounded-lg border border-border overflow-hidden">
      <Tabs defaultValue="ppt" className="h-full">
        <div className="flex items-center justify-between px-4 py-2 border-b border-border bg-secondary/30">
          <TabsList className="h-8 bg-secondary/50">
            <TabsTrigger value="ppt" className="text-xs gap-1 h-6 px-2">
              <Presentation className="h-3 w-3" />
              PPT
            </TabsTrigger>
            <TabsTrigger value="pdf" className="text-xs gap-1 h-6 px-2">
              <FileText className="h-3 w-3" />
              PDF
            </TabsTrigger>
          </TabsList>
          <div className="flex gap-1">
            <Button 
              variant="ghost" 
              size="sm" 
              className="h-7 px-2 text-xs"
              onClick={onEdit}
            >
              <Edit className="h-3 w-3 mr-1" />
              Edit
            </Button>
            <Button 
              variant="ghost" 
              size="sm" 
              className="h-7 px-2 text-xs"
              onClick={() => onDownload?.('pptx')}
            >
              <Download className="h-3 w-3 mr-1" />
              Download
            </Button>
          </div>
        </div>

        <TabsContent value="ppt" className="m-0">
          {/* Slide Preview */}
          <div 
            className="bg-gradient-to-br from-primary/5 to-accent/5 p-6 min-h-[280px] relative"
            style={{ transform: `scale(${zoom / 100})`, transformOrigin: 'top left' }}
          >
            <div className="bg-card border border-border rounded-lg p-6 shadow-lg max-w-md mx-auto">
              <div className="border-l-4 border-primary pl-4 mb-4">
                <h2 className="text-lg font-bold text-foreground">{currentSlide.title}</h2>
                <p className="text-sm text-muted-foreground">{currentSlide.content}</p>
              </div>
              <ul className="space-y-2">
                {currentSlide.bullets.map((bullet, idx) => (
                  <li key={idx} className="flex items-center gap-2 text-sm text-muted-foreground">
                    <span className="h-1.5 w-1.5 rounded-full bg-primary flex-shrink-0" />
                    {bullet}
                  </li>
                ))}
              </ul>
              <div className="absolute bottom-4 right-4 text-xs text-muted-foreground">
                Slide {currentPage} of {totalPages}
              </div>
            </div>
          </div>

          {/* Controls */}
          <div className="flex items-center justify-between px-4 py-3 border-t border-border bg-secondary/20">
            <div className="flex items-center gap-2">
              <Button 
                variant="outline" 
                size="sm" 
                className="h-7 w-7 p-0"
                onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                disabled={currentPage === 1}
              >
                <ChevronLeft className="h-4 w-4" />
              </Button>
              <span className="text-xs text-muted-foreground min-w-[60px] text-center">
                {currentPage} / {totalPages}
              </span>
              <Button 
                variant="outline" 
                size="sm" 
                className="h-7 w-7 p-0"
                onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                disabled={currentPage === totalPages}
              >
                <ChevronRight className="h-4 w-4" />
              </Button>
            </div>
            <div className="flex items-center gap-1">
              <Button 
                variant="ghost" 
                size="sm" 
                className="h-7 w-7 p-0"
                onClick={() => setZoom(Math.max(50, zoom - 10))}
              >
                <ZoomOut className="h-3.5 w-3.5" />
              </Button>
              <span className="text-xs text-muted-foreground w-10 text-center">{zoom}%</span>
              <Button 
                variant="ghost" 
                size="sm" 
                className="h-7 w-7 p-0"
                onClick={() => setZoom(Math.min(150, zoom + 10))}
              >
                <ZoomIn className="h-3.5 w-3.5" />
              </Button>
              <Button variant="ghost" size="sm" className="h-7 w-7 p-0 ml-2">
                <Maximize2 className="h-3.5 w-3.5" />
              </Button>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="pdf" className="m-0">
          <div className="bg-secondary/20 p-6 min-h-[280px]">
            <div className="bg-card border border-border rounded-lg p-6 shadow-sm max-w-md mx-auto">
              <h2 className="text-lg font-bold text-foreground mb-4 pb-2 border-b border-border">
                Account Analysis Report
              </h2>
              <div className="space-y-4 text-sm text-muted-foreground">
                <section>
                  <h3 className="font-semibold text-foreground text-xs uppercase tracking-wide mb-1">
                    Executive Summary
                  </h3>
                  <p className="text-xs leading-relaxed">
                    This report provides a comprehensive analysis of account performance 
                    metrics and identifies key areas requiring immediate attention.
                  </p>
                </section>
                <section>
                  <h3 className="font-semibold text-foreground text-xs uppercase tracking-wide mb-1">
                    Key Findings
                  </h3>
                  <ul className="text-xs space-y-1">
                    <li>• Order volume decline: 16.4%</li>
                    <li>• Support ticket increase: 104%</li>
                    <li>• Customer NPS drop: 25 points</li>
                  </ul>
                </section>
              </div>
              <div className="mt-4 pt-3 border-t border-border text-[10px] text-muted-foreground">
                Generated by Manufacturing Agent • Page {currentPage}
              </div>
            </div>
          </div>
          
          {/* PDF Controls */}
          <div className="flex items-center justify-between px-4 py-3 border-t border-border bg-secondary/20">
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" className="h-7 w-7 p-0">
                <ChevronLeft className="h-4 w-4" />
              </Button>
              <span className="text-xs text-muted-foreground">1 / 12</span>
              <Button variant="outline" size="sm" className="h-7 w-7 p-0">
                <ChevronRight className="h-4 w-4" />
              </Button>
            </div>
            <Button 
              variant="outline" 
              size="sm" 
              className="h-7 text-xs"
              onClick={() => onDownload?.('pdf')}
            >
              <Download className="h-3 w-3 mr-1" />
              Download PDF
            </Button>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default DocumentViewer;
