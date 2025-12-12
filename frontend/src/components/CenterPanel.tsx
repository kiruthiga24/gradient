import React from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { BarChart3, Table2, FileText, Activity } from 'lucide-react';
import { DataTable, TableRowData } from './DataTable';
import { LineChartPanel } from './LineChartPanel';
import { AnalysisSummary } from './AnalysisSummary';

interface CenterPanelProps {
  accountId: string | null;
}

const sampleTableData: TableRowData[] = [
  { metric: 'Order Volume', current: '1,245', previous: '1,489', change: -16.4, status: 'down' },
  { metric: 'Avg Order Value', current: '$2,340', previous: '$2,180', change: 7.3, status: 'up' },
  { metric: 'Support Tickets', current: '47', previous: '23', change: 104.3, status: 'down' },
  { metric: 'Response Time', current: '4.2h', previous: '2.1h', change: 100, status: 'down' },
  { metric: 'Customer NPS', current: '42', previous: '67', change: -37.3, status: 'down' },
  { metric: 'Delivery On-Time', current: '78%', previous: '94%', change: -17, status: 'down' },
];

const chartData = [
  { name: 'Week 1', orders: 420, tickets: 12, revenue: 98 },
  { name: 'Week 2', orders: 380, tickets: 18, revenue: 89 },
  { name: 'Week 3', orders: 340, tickets: 24, revenue: 76 },
  { name: 'Week 4', orders: 290, tickets: 35, revenue: 65 },
  { name: 'Week 5', orders: 245, tickets: 47, revenue: 54 },
];

const analysisSummary = `Based on comprehensive analysis of account data over the past 30 days, 
significant deterioration in key performance indicators has been detected. Order volume has declined 
by 16.4% while support tickets have increased by 104%. This pattern typically indicates supply chain 
or quality control issues requiring immediate attention. The correlation between delivery delays 
and ticket spikes suggests fulfillment bottlenecks.`;

const patterns = [
  'Order volume declining at 4.1% per week for 5 consecutive weeks',
  'Support ticket spike correlates with delivery delay reports',
  'Customer NPS dropped 25 points following product quality complaints',
  'Repeat order rate decreased from 45% to 28%',
];

const recommendations = [
  'Schedule immediate review call with account stakeholders',
  'Investigate supply chain and fulfillment process bottlenecks',
  'Implement proactive communication about delivery expectations',
  'Consider offering service credits to retain customer relationship',
];

export const CenterPanel: React.FC<CenterPanelProps> = ({ accountId }) => {
  if (!accountId) {
    return (
      <div className="flex-1 flex items-center justify-center bg-secondary/20">
        <div className="text-center text-muted-foreground">
          <Activity className="h-12 w-12 mx-auto mb-3 opacity-40" />
          <p className="text-sm">Select an account to view analysis</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto scrollbar-thin bg-background/50 p-6">
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList className="bg-secondary/50">
          <TabsTrigger value="overview" className="text-xs gap-1.5">
            <Activity className="h-3.5 w-3.5" />
            Overview
          </TabsTrigger>
          <TabsTrigger value="metrics" className="text-xs gap-1.5">
            <Table2 className="h-3.5 w-3.5" />
            Metrics
          </TabsTrigger>
          <TabsTrigger value="trends" className="text-xs gap-1.5">
            <BarChart3 className="h-3.5 w-3.5" />
            Trends
          </TabsTrigger>
          <TabsTrigger value="analysis" className="text-xs gap-1.5">
            <FileText className="h-3.5 w-3.5" />
            Analysis
          </TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4 animate-fade-in">
          <AnalysisSummary 
            summary={analysisSummary}
            patterns={patterns}
            recommendations={recommendations}
          />
          <LineChartPanel data={chartData} title="Performance Trend (5 Weeks)" />
        </TabsContent>

        <TabsContent value="metrics" className="space-y-4 animate-fade-in">
          <DataTable data={sampleTableData} title="Key Performance Indicators" />
          <DataTable 
            data={[
              { metric: 'Production Output', current: '8,450 units', previous: '9,200 units', change: -8.2, status: 'down' },
              { metric: 'Defect Rate', current: '3.2%', previous: '1.8%', change: 77.8, status: 'down' },
              { metric: 'Equipment Uptime', current: '87%', previous: '96%', change: -9.4, status: 'down' },
              { metric: 'Raw Material Cost', current: '$45.2K', previous: '$42.1K', change: 7.4, status: 'down' },
            ]}
            title="Manufacturing Metrics"
          />
        </TabsContent>

        <TabsContent value="trends" className="space-y-4 animate-fade-in">
          <LineChartPanel data={chartData} title="Order & Ticket Trends" />
          <LineChartPanel 
            data={[
              { name: 'Jan', orders: 520, tickets: 8, revenue: 112 },
              { name: 'Feb', orders: 480, tickets: 12, revenue: 98 },
              { name: 'Mar', orders: 440, tickets: 15, revenue: 89 },
              { name: 'Apr', orders: 380, tickets: 22, revenue: 76 },
              { name: 'May', orders: 320, tickets: 35, revenue: 62 },
            ]}
            title="Monthly Performance Comparison"
          />
        </TabsContent>

        <TabsContent value="analysis" className="space-y-4 animate-fade-in">
          <AnalysisSummary 
            summary={analysisSummary}
            patterns={patterns}
            recommendations={recommendations}
          />
          <div className="bg-card rounded-lg border border-border p-4">
            <h3 className="text-sm font-semibold text-foreground mb-3">Detailed Analysis Report</h3>
            <div className="prose prose-sm text-muted-foreground space-y-3">
              <p>
                <strong className="text-foreground">Executive Summary:</strong> Account shows signs of significant 
                operational stress with declining order volumes and increasing support burden. Root cause analysis 
                points to manufacturing quality issues and supply chain disruptions.
              </p>
              <p>
                <strong className="text-foreground">Risk Assessment:</strong> Current trajectory suggests 30% 
                probability of account churn within 60 days without intervention. Recommended urgency level: HIGH.
              </p>
              <p>
                <strong className="text-foreground">Historical Context:</strong> This account has been a consistent 
                performer since 2019, making current decline anomalous. Previous issues in 2021 were resolved 
                through enhanced support engagement.
              </p>
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default CenterPanel;
