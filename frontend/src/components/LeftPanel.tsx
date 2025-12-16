import React from 'react';
import { Input } from '@/components/ui/input';
import { Search, Filter } from 'lucide-react';
import { AccountCard, AccountData } from './AccountCard';
import { Button } from '@/components/ui/button';

interface LeftPanelProps {
  accounts: AccountData[];
  activeAccountId: string | null;
  onAccountSelect: (id: string) => void;
}

export const LeftPanel: React.FC<LeftPanelProps> = ({ 
  accounts, 
  activeAccountId, 
  onAccountSelect 
}) => {
  return (
    <div className="w-80 flex-shrink-0 bg-card border-r border-border flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-border">
        <h2 className="text-sm font-semibold text-foreground mb-3">Account Alerts</h2>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input 
            placeholder="Search accounts..." 
            className="pl-9 h-9 text-sm bg-secondary/50 border-border/60"
          />
        </div>
        <div className="flex gap-2 mt-3">
          <Button variant="outline" size="sm" className="text-xs h-7">
            <Filter className="h-3 w-3 mr-1" />
            All Severity
          </Button>
          <Button variant="outline" size="sm" className="text-xs h-7">
            Latest First
          </Button>
        </div>
      </div>

      {/* Accounts List */}
      <div className="flex-1 overflow-y-auto scrollbar-thin p-3 space-y-2">
        {accounts.map((account) => (
          <AccountCard
            key={account.id}
            account={account}
            isActive={activeAccountId === account.id}
            onClick={() => onAccountSelect(account.id)}
          />
        ))}
      </div>

      {/* Footer Stats */}
      <div className="p-4 border-t border-border bg-secondary/30">
        <div className="flex justify-between text-xs text-muted-foreground">
          <span>{accounts.length} accounts monitored</span>
          <span className="text-destructive font-medium">
            {accounts.filter(a => a.severity === 'HIGH').length} critical
          </span>
        </div>
      </div>
    </div>
  );
};

export default LeftPanel;
