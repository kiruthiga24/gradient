import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

export interface TableRowData {
  metric: string;
  current: string;
  previous: string;
  change: number;
  status: 'up' | 'down' | 'stable';
}

interface DataTableProps {
  data: TableRowData[];
  title: string;
}

export const DataTable: React.FC<DataTableProps> = ({ data, title }) => {
  const getTrendIcon = (status: string) => {
    switch (status) {
      case 'up':
        return <TrendingUp className="h-3.5 w-3.5 text-success" />;
      case 'down':
        return <TrendingDown className="h-3.5 w-3.5 text-destructive" />;
      default:
        return <Minus className="h-3.5 w-3.5 text-muted-foreground" />;
    }
  };

  const getChangeColor = (status: string) => {
    switch (status) {
      case 'up':
        return 'text-success';
      case 'down':
        return 'text-destructive';
      default:
        return 'text-muted-foreground';
    }
  };

  return (
    <div className="bg-card rounded-lg border border-border overflow-hidden">
      <div className="px-4 py-3 border-b border-border bg-secondary/30">
        <h3 className="text-sm font-semibold text-foreground">{title}</h3>
      </div>
      <Table>
        <TableHeader>
          <TableRow className="hover:bg-transparent">
            <TableHead className="text-xs font-medium">Metric</TableHead>
            <TableHead className="text-xs font-medium text-right">Current</TableHead>
            <TableHead className="text-xs font-medium text-right">Previous</TableHead>
            <TableHead className="text-xs font-medium text-right">Change</TableHead>
            <TableHead className="text-xs font-medium text-center">Trend</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((row, idx) => (
            <TableRow key={idx} className="hover:bg-secondary/30">
              <TableCell className="text-sm font-medium">{row.metric}</TableCell>
              <TableCell className="text-sm text-right font-mono">{row.current}</TableCell>
              <TableCell className="text-sm text-right font-mono text-muted-foreground">{row.previous}</TableCell>
              <TableCell className={`text-sm text-right font-mono ${getChangeColor(row.status)}`}>
                {row.change > 0 ? '+' : ''}{row.change}%
              </TableCell>
              <TableCell className="text-center">
                {getTrendIcon(row.status)}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default DataTable;
