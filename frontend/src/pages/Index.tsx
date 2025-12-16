import React, { useState } from 'react';
import { ManufacturingLogo } from '@/components/ManufacturingLogo';
import { LeftPanel } from '@/components/LeftPanel';
import { CenterPanel } from '@/components/CenterPanel';
import { RightPanel } from '@/components/RightPanel';
import { AccountData } from '@/components/AccountCard';
import { Bell, Settings, User } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Toaster } from '@/components/ui/sonner';

const sampleAccounts: AccountData[] = [
  {
    id: '1',
    company: 'Jimenez, Lewis and Burns',
    score: 0.55,
    severity: 'MEDIUM',
    tags: ['Order Drop', 'Ticket Spike'],
    detectedAgo: '3 mins ago',
  },
  {
    id: '2',
    company: 'Anderson Manufacturing Co.',
    score: 0.82,
    severity: 'HIGH',
    tags: ['Churn Risk', 'Payment Delayed'],
    detectedAgo: '12 mins ago',
  },
  {
    id: '3',
    company: 'Pacific Steel Industries',
    score: 0.38,
    severity: 'LOW',
    tags: ['Volume Decline'],
    detectedAgo: '28 mins ago',
  },
  {
    id: '4',
    company: 'Midwest Parts Distributors',
    score: 0.71,
    severity: 'HIGH',
    tags: ['Quality Issues', 'Returns Spike'],
    detectedAgo: '45 mins ago',
  },
  {
    id: '5',
    company: 'Summit Industrial Supply',
    score: 0.44,
    severity: 'MEDIUM',
    tags: ['Engagement Drop'],
    detectedAgo: '1 hour ago',
  },
  {
    id: '6',
    company: 'Eastern Component Works',
    score: 0.29,
    severity: 'LOW',
    tags: ['Minor Delay'],
    detectedAgo: '2 hours ago',
  },
];

const Index = () => {
  const [activeAccountId, setActiveAccountId] = useState<string | null>('1');

  return (
    <div className="flex flex-col h-screen bg-background">
      {/* Top Navigation */}
      <header className="h-14 border-b border-border bg-card flex items-center justify-between px-4 flex-shrink-0">
        <div className="flex items-center gap-3">
          <ManufacturingLogo size={28} className="text-primary" />
          <div>
            <h1 className="text-sm font-semibold text-foreground leading-none">
              Manufacturing Account Agent
            </h1>
            <p className="text-[11px] text-muted-foreground">
              Data-Driven Account Management
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0 relative">
            <Bell className="h-4 w-4" />
            <span className="absolute -top-0.5 -right-0.5 h-3.5 w-3.5 bg-destructive text-[9px] text-destructive-foreground rounded-full flex items-center justify-center font-medium">
              3
            </span>
          </Button>
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
            <Settings className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
            <User className="h-4 w-4" />
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        <LeftPanel 
          accounts={sampleAccounts}
          activeAccountId={activeAccountId}
          onAccountSelect={setActiveAccountId}
        />
        <CenterPanel accountId={activeAccountId} />
        <RightPanel accountId={activeAccountId} />
      </div>

      <Toaster position="bottom-right" />
    </div>
  );
};

export default Index;
