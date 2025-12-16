import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Phone, 
  Mail, 
  Calendar, 
  FileText,
  Edit,
  Check,
  X,
  Plus
} from 'lucide-react';
import { DocumentViewer } from './DocumentViewer';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { toast } from 'sonner';

interface ActionItem {
  id: string;
  title: string;
  description: string;
  status: 'pending' | 'in-progress' | 'completed';
  priority: 'high' | 'medium' | 'low';
}

interface RightPanelProps {
  accountId: string | null;
}

export const RightPanel: React.FC<RightPanelProps> = ({ accountId }) => {
  const [actions, setActions] = useState<ActionItem[]>([
    { id: '1', title: 'Schedule Review Call', description: 'Set up call with account stakeholders', status: 'pending', priority: 'high' },
    { id: '2', title: 'Prepare Analysis Report', description: 'Compile data for presentation', status: 'in-progress', priority: 'high' },
    { id: '3', title: 'Draft Recovery Plan', description: 'Create action plan document', status: 'pending', priority: 'medium' },
  ]);

  const [editingAction, setEditingAction] = useState<ActionItem | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const handleEdit = (action: ActionItem) => {
    setEditingAction({ ...action });
    setIsDialogOpen(true);
  };

  const handleSaveAction = () => {
    if (editingAction) {
      setActions(actions.map(a => a.id === editingAction.id ? editingAction : a));
      toast.success('Action updated successfully');
      setIsDialogOpen(false);
      setEditingAction(null);
    }
  };

  const handleDownload = (format: string) => {
    toast.success(`Downloading ${format.toUpperCase()} file...`);
  };

  const handleDocumentEdit = () => {
    toast.info('Opening document editor...');
  };

  const statusColors = {
    pending: 'bg-warning/15 text-warning border-warning/30',
    'in-progress': 'bg-primary/15 text-primary border-primary/30',
    completed: 'bg-success/15 text-success border-success/30',
  };

  const priorityColors = {
    high: 'text-destructive',
    medium: 'text-warning',
    low: 'text-muted-foreground',
  };

  if (!accountId) {
    return (
      <div className="w-80 flex-shrink-0 bg-card border-l border-border flex items-center justify-center">
        <p className="text-sm text-muted-foreground">Select an account</p>
      </div>
    );
  }

  return (
    <div className="w-96 flex-shrink-0 bg-card border-l border-border flex flex-col h-full overflow-hidden">
      {/* Header */}
      <div className="p-4 border-b border-border">
        <h2 className="text-sm font-semibold text-foreground">Quick Actions</h2>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto scrollbar-thin p-4 space-y-4">
        {/* Action Buttons */}
        <div className="grid grid-cols-2 gap-2">
          <Button variant="outline" size="sm" className="justify-start text-xs h-9">
            <Phone className="h-3.5 w-3.5 mr-2" />
            Call
          </Button>
          <Button variant="outline" size="sm" className="justify-start text-xs h-9">
            <Mail className="h-3.5 w-3.5 mr-2" />
            Email
          </Button>
          <Button variant="outline" size="sm" className="justify-start text-xs h-9">
            <Calendar className="h-3.5 w-3.5 mr-2" />
            Schedule
          </Button>
          <Button variant="outline" size="sm" className="justify-start text-xs h-9">
            <FileText className="h-3.5 w-3.5 mr-2" />
            Notes
          </Button>
        </div>

        {/* Action Items */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-semibold text-foreground">Action Items</h3>
            <Button variant="ghost" size="sm" className="h-6 px-2 text-xs">
              <Plus className="h-3 w-3 mr-1" />
              Add
            </Button>
          </div>
          {actions.map((action) => (
            <div 
              key={action.id} 
              className="bg-secondary/30 rounded-lg p-3 border border-border/50"
            >
              <div className="flex items-start justify-between mb-1">
                <h4 className={`text-xs font-medium ${priorityColors[action.priority]}`}>
                  {action.title}
                </h4>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  className="h-5 w-5 p-0"
                  onClick={() => handleEdit(action)}
                >
                  <Edit className="h-3 w-3" />
                </Button>
              </div>
              <p className="text-[11px] text-muted-foreground mb-2">{action.description}</p>
              <Badge variant="outline" className={`text-[10px] ${statusColors[action.status]}`}>
                {action.status}
              </Badge>
            </div>
          ))}
        </div>

        {/* Document Viewer */}
        <div className="space-y-2">
          <h3 className="text-xs font-semibold text-foreground">Documents</h3>
          <DocumentViewer 
            onEdit={handleDocumentEdit}
            onDownload={handleDownload}
          />
        </div>
      </div>

      {/* Edit Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle className="text-sm">Edit Action Item</DialogTitle>
          </DialogHeader>
          {editingAction && (
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <label className="text-xs font-medium text-foreground">Title</label>
                <Input 
                  value={editingAction.title}
                  onChange={(e) => setEditingAction({ ...editingAction, title: e.target.value })}
                  className="h-9 text-sm"
                />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-medium text-foreground">Description</label>
                <Textarea 
                  value={editingAction.description}
                  onChange={(e) => setEditingAction({ ...editingAction, description: e.target.value })}
                  className="text-sm resize-none"
                  rows={3}
                />
              </div>
              <div className="flex gap-2 pt-2">
                <Button size="sm" className="flex-1" onClick={handleSaveAction}>
                  <Check className="h-3.5 w-3.5 mr-1" />
                  Save
                </Button>
                <Button size="sm" variant="outline" onClick={() => setIsDialogOpen(false)}>
                  <X className="h-3.5 w-3.5 mr-1" />
                  Cancel
                </Button>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default RightPanel;
