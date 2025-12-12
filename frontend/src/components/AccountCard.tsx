"use client"

import type React from "react"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"

export interface AccountData {
  id: string
  company: string
  score: number
  severity: "HIGH" | "MEDIUM" | "LOW"
  tags: string[]
  detectedAgo: string
}

interface AccountCardProps {
  account: AccountData
  isActive: boolean
  onClick: () => void
}

export const AccountCard: React.FC<AccountCardProps> = ({ account, isActive, onClick }) => {
  const severityClasses = {
    HIGH: "severity-high",
    MEDIUM: "severity-medium",
    LOW: "severity-low",
  }

  const severityBadgeClasses = {
    HIGH: "bg-destructive/15 text-destructive border-destructive/30 hover:bg-destructive/20",
    MEDIUM: "bg-warning/15 text-warning border-warning/30 hover:bg-warning/20",
    LOW: "bg-success/15 text-success border-success/30 hover:bg-success/20",
  }

  return (
    <div
      onClick={onClick}
      className={cn(
        "p-4 rounded-lg border cursor-pointer transition-all duration-200",
        "hover:shadow-md hover:border-primary/30",
        isActive ? "bg-primary/5 border-primary/40 shadow-sm" : "bg-card border-border/60 hover:bg-card/80",
      )}
    >
      {/* Company Name */}
      <h3 className="font-semibold text-base text-card-foreground mb-2 leading-tight">{account.company}</h3>

      {/* Score and Severity */}
      <div className="flex items-center gap-3 mb-3">
        <div className="flex items-center gap-1.5">
          <span className="text-xs text-muted-foreground">Score:</span>
          <span className="font-mono text-sm font-semibold text-foreground">{account.score.toFixed(2)}</span>
        </div>
        <Badge
          variant="outline"
          className={cn("text-xs px-2 py-0.5 font-medium", severityBadgeClasses[account.severity])}
        >
          {account.severity}
        </Badge>
      </div>

      {/* Tags */}
      <div className="flex flex-wrap gap-2 mb-3">
        {account.tags.map((tag, idx) => (
          <span
            key={idx}
            className="text-xs font-medium text-foreground border border-border/60 px-2 py-0.5 rounded bg-muted/30"
          >
            [ {tag} ]
          </span>
        ))}
      </div>

      {/* Detected Time */}
      <p className="text-[11px] text-muted-foreground">Detected {account.detectedAgo}</p>
    </div>
  )
}

export default AccountCard
