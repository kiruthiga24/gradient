// ========================================
// AI Agent Dashboard - Application Logic
// ========================================

// ========================================
// Sample Data
// ========================================

const alertsData = {
  churn: [
    {
      id: "churn-1",
      company: "Acme Corp",
      type: "Usage Decline Alert",
      severity: "critical",
      score: 92,
      metrics: { engagement: "-45%", logins: "2/week" },
      timestamp: "2 min ago",
      analysis: {
        summary:
          "Acme Corp shows critical signs of potential churn. User engagement has dropped 45% over the past 30 days, with key stakeholders reducing their platform usage significantly. The primary admin hasn't logged in for 12 days, and support ticket volume has increased by 60%.",
        patterns: [
          { icon: "📉", label: "Engagement Drop", value: "45% decrease in 30 days" },
          { icon: "👤", label: "Admin Inactive", value: "No login for 12 days" },
          { icon: "🎫", label: "Support Tickets", value: "+60% volume increase" },
          { icon: "💳", label: "Payment Risk", value: "Renewal in 18 days" },
        ],
        scenarios: [
          { title: "Executive Outreach Campaign", impact: "+35% retention probability" },
          { title: "Emergency Success Review", impact: "+28% satisfaction score" },
          { title: "Feature Adoption Workshop", impact: "+42% engagement lift" },
        ],
      },
      actions: [
        {
          type: "crm",
          title: "Create CRM Task",
          description: "Schedule executive check-in call with VP of Operations",
          due: "Tomorrow",
          owner: "Sarah Chen",
          impact: "High",
        },
        {
          type: "email",
          title: "Send Personalized Email",
          description: "Re-engagement email highlighting unused premium features",
          due: "Today",
          owner: "Auto-send",
          impact: "Medium",
        },
        {
          type: "recovery",
          title: "Initiate Recovery Flow",
          description: "Trigger 5-step recovery sequence with exclusive offer",
          due: "Immediate",
          owner: "System",
          impact: "High",
        },
        {
          type: "crm",
          title: "Log Health Score",
          description: "Update account health metrics in CRM dashboard",
          due: "Today",
          owner: "System",
          impact: "Low",
        },
      ],
    },
    {
      id: "churn-2",
      company: "TechStart Inc",
      type: "Feature Abandonment",
      severity: "high",
      score: 78,
      metrics: { features: "-3 active", sessions: "↓32%" },
      timestamp: "15 min ago",
      analysis: {
        summary:
          "TechStart Inc has stopped using 3 core features that were previously part of their daily workflow. This indicates a potential mismatch between product capabilities and evolving needs.",
        patterns: [
          { icon: "🔧", label: "Features Dropped", value: "3 core features unused" },
          { icon: "⏱️", label: "Session Time", value: "32% shorter sessions" },
          { icon: "📊", label: "Dashboard Views", value: "Down 55% weekly" },
          { icon: "🔄", label: "API Calls", value: "Minimal activity" },
        ],
        scenarios: [
          { title: "Feature Re-training Session", impact: "+40% feature adoption" },
          { title: "Workflow Optimization Call", impact: "+25% productivity gain" },
          { title: "Custom Integration Setup", impact: "+50% stickiness" },
        ],
      },
      actions: [
        {
          type: "email",
          title: "Feature Highlight Email",
          description: "Send curated feature guide based on their use case",
          due: "Today",
          owner: "Auto-send",
          impact: "Medium",
        },
        {
          type: "crm",
          title: "Schedule Demo Call",
          description: "Book feature walkthrough with product specialist",
          due: "This week",
          owner: "Mike R.",
          impact: "High",
        },
      ],
    },
    {
      id: "churn-3",
      company: "GlobalRetail",
      type: "Contract Risk",
      severity: "high",
      score: 85,
      metrics: { renewal: "12 days", nps: "6/10" },
      timestamp: "32 min ago",
      analysis: {
        summary:
          "GlobalRetail's contract expires in 12 days with no renewal discussion initiated. Recent NPS score of 6 indicates lukewarm satisfaction.",
        patterns: [
          { icon: "📅", label: "Renewal Date", value: "12 days remaining" },
          { icon: "⭐", label: "NPS Score", value: "6/10 (down from 8)" },
          { icon: "💬", label: "Feedback", value: "2 unresolved complaints" },
          { icon: "🏢", label: "Stakeholders", value: "New decision maker" },
        ],
        scenarios: [
          { title: "Renewal Negotiation Meeting", impact: "+45% close rate" },
          { title: "Value Assessment Report", impact: "+30% perceived ROI" },
          { title: "Loyalty Discount Offer", impact: "+60% renewal probability" },
        ],
      },
      actions: [
        {
          type: "crm",
          title: "Flag Priority Account",
          description: "Mark as high-priority renewal in CRM",
          due: "Immediate",
          owner: "System",
          impact: "High",
        },
        {
          type: "email",
          title: "Send ROI Report",
          description: "Automated value summary email to stakeholders",
          due: "Today",
          owner: "Auto-send",
          impact: "High",
        },
        {
          type: "recovery",
          title: "Prepare Renewal Package",
          description: "Generate custom renewal proposal with incentives",
          due: "Tomorrow",
          owner: "Sales Team",
          impact: "Critical",
        },
      ],
    },
    {
      id: "churn-4",
      company: "FinServe Ltd",
      type: "Payment Issue",
      severity: "medium",
      score: 65,
      metrics: { attempts: "2 failed", balance: "$12,400" },
      timestamp: "1 hour ago",
      analysis: {
        summary:
          "FinServe Ltd has experienced 2 consecutive failed payment attempts. While they have a positive history, immediate action is needed to prevent service disruption.",
        patterns: [
          { icon: "💳", label: "Payment Failures", value: "2 consecutive attempts" },
          { icon: "💰", label: "Outstanding", value: "$12,400 balance" },
          { icon: "📈", label: "History", value: "18 months customer" },
          { icon: "✅", label: "Past Payments", value: "100% on-time prior" },
        ],
        scenarios: [
          { title: "Payment Method Update", impact: "+90% collection rate" },
          { title: "Flexible Payment Plan", impact: "+75% retention" },
          { title: "Account Manager Outreach", impact: "+85% resolution" },
        ],
      },
      actions: [
        {
          type: "email",
          title: "Payment Update Request",
          description: "Friendly reminder to update payment method",
          due: "Immediate",
          owner: "Auto-send",
          impact: "High",
        },
        {
          type: "crm",
          title: "Log Payment Issue",
          description: "Create billing support ticket",
          due: "Today",
          owner: "Billing",
          impact: "Medium",
        },
      ],
    },
    {
      id: "churn-5",
      company: "MediaPro Agency",
      type: "Support Escalation",
      severity: "medium",
      score: 58,
      metrics: { tickets: "5 open", wait: "48+ hrs" },
      timestamp: "2 hours ago",
      analysis: {
        summary:
          "MediaPro Agency has 5 unresolved support tickets with an average wait time exceeding 48 hours. Customer frustration is building.",
        patterns: [
          { icon: "🎫", label: "Open Tickets", value: "5 unresolved" },
          { icon: "⏰", label: "Wait Time", value: "48+ hours average" },
          { icon: "😤", label: "Sentiment", value: "Frustration detected" },
          { icon: "📞", label: "Escalations", value: "2 manager requests" },
        ],
        scenarios: [
          { title: "Priority Support Queue", impact: "+80% satisfaction" },
          { title: "Dedicated Rep Assignment", impact: "+65% loyalty" },
          { title: "Service Credit Offer", impact: "+40% goodwill" },
        ],
      },
      actions: [
        {
          type: "crm",
          title: "Escalate Tickets",
          description: "Move all tickets to priority queue",
          due: "Immediate",
          owner: "Support Lead",
          impact: "Critical",
        },
        {
          type: "email",
          title: "Apology Email",
          description: "Send personalized apology with timeline",
          due: "Today",
          owner: "Auto-send",
          impact: "Medium",
        },
      ],
    },
    {
      id: "churn-6",
      company: "EduLearn Pro",
      type: "Low Adoption",
      severity: "low",
      score: 42,
      metrics: { users: "12/50", completion: "23%" },
      timestamp: "3 hours ago",
      analysis: {
        summary:
          "EduLearn Pro has only onboarded 12 of 50 purchased seats with 23% training completion. Early intervention can improve adoption.",
        patterns: [
          { icon: "👥", label: "Seat Usage", value: "12 of 50 active" },
          { icon: "📚", label: "Training", value: "23% completion" },
          { icon: "🚀", label: "Onboarding", value: "Stalled at step 3" },
          { icon: "📆", label: "Account Age", value: "45 days old" },
        ],
        scenarios: [
          { title: "Onboarding Bootcamp", impact: "+60% seat activation" },
          { title: "Admin Training Session", impact: "+45% adoption rate" },
          { title: "Success Plan Creation", impact: "+50% engagement" },
        ],
      },
      actions: [
        {
          type: "email",
          title: "Onboarding Guide",
          description: "Send step-by-step activation guide",
          due: "Today",
          owner: "Auto-send",
          impact: "Medium",
        },
        {
          type: "crm",
          title: "Schedule Check-in",
          description: "Book 30-min adoption review call",
          due: "This week",
          owner: "CSM Team",
          impact: "High",
        },
      ],
    },
  ],
  expansion: [
    {
      id: "exp-1",
      company: "ScaleUp Solutions",
      type: "Upsell Opportunity",
      severity: "low",
      score: 95,
      metrics: { usage: "142%", growth: "+28 users" },
      timestamp: "5 min ago",
      analysis: {
        summary:
          "ScaleUp Solutions is consistently exceeding their current plan limits. They've added 28 new users this month and are hitting API limits daily.",
        patterns: [
          { icon: "📈", label: "Plan Usage", value: "142% of limit" },
          { icon: "👥", label: "User Growth", value: "+28 this month" },
          { icon: "🔌", label: "API Calls", value: "Daily limit reached" },
          { icon: "💼", label: "Department", value: "3 teams using" },
        ],
        scenarios: [
          { title: "Enterprise Plan Upgrade", impact: "+$24K ARR" },
          { title: "API Tier Expansion", impact: "+$8K ARR" },
          { title: "Multi-team License", impact: "+$15K ARR" },
        ],
      },
      actions: [
        {
          type: "crm",
          title: "Create Expansion Opportunity",
          description: "Log upsell opportunity in pipeline",
          due: "Today",
          owner: "Sales",
          impact: "High",
        },
        {
          type: "email",
          title: "Premium Features Preview",
          description: "Send exclusive enterprise feature overview",
          due: "Today",
          owner: "Auto-send",
          impact: "Medium",
        },
      ],
    },
    {
      id: "exp-2",
      company: "DataDriven Co",
      type: "Cross-sell Signal",
      severity: "low",
      score: 88,
      metrics: { interest: "Analytics+", requests: "3 demos" },
      timestamp: "20 min ago",
      analysis: {
        summary:
          "DataDriven Co has requested 3 demos for our Analytics+ module and their usage patterns indicate strong alignment with advanced reporting needs.",
        patterns: [
          { icon: "📊", label: "Demo Requests", value: "3 for Analytics+" },
          { icon: "📋", label: "Report Usage", value: "Heavy export activity" },
          { icon: "🔗", label: "Integrations", value: "BI tools connected" },
          { icon: "⭐", label: "Satisfaction", value: "NPS 9/10" },
        ],
        scenarios: [
          { title: "Analytics+ Bundle Sale", impact: "+$12K ARR" },
          { title: "Custom Dashboard Package", impact: "+$6K ARR" },
          { title: "Training Certification", impact: "+$3K one-time" },
        ],
      },
      actions: [
        {
          type: "crm",
          title: "Schedule Product Demo",
          description: "Book Analytics+ deep-dive session",
          due: "This week",
          owner: "Product Sales",
          impact: "High",
        },
        {
          type: "email",
          title: "Case Study Share",
          description: "Send relevant success stories",
          due: "Today",
          owner: "Auto-send",
          impact: "Medium",
        },
      ],
    },
    {
      id: "exp-3",
      company: "InnovateTech",
      type: "Referral Potential",
      severity: "low",
      score: 91,
      metrics: { nps: "10/10", mentions: "5 social" },
      timestamp: "45 min ago",
      analysis: {
        summary:
          "InnovateTech is a highly satisfied customer with NPS of 10 and has mentioned us positively 5 times on social media. Prime referral candidate.",
        patterns: [
          { icon: "⭐", label: "NPS Score", value: "10/10 promoter" },
          { icon: "📱", label: "Social Mentions", value: "5 positive posts" },
          { icon: "💬", label: "Testimonial", value: "Offered to provide" },
          { icon: "🤝", label: "Network", value: "Industry influencer" },
        ],
        scenarios: [
          { title: "Referral Program Invite", impact: "+2 qualified leads" },
          { title: "Case Study Feature", impact: "+15% conversion lift" },
          { title: "Partner Program Offer", impact: "+$20K partner revenue" },
        ],
      },
      actions: [
        {
          type: "email",
          title: "Referral Invite",
          description: "Send exclusive referral program invitation",
          due: "Today",
          owner: "Auto-send",
          impact: "High",
        },
        {
          type: "crm",
          title: "Log Advocate",
          description: "Add to customer advocacy program",
          due: "Today",
          owner: "Marketing",
          impact: "Medium",
        },
      ],
    },
    {
      id: "exp-4",
      company: "Enterprise Global",
      type: "Contract Expansion",
      severity: "low",
      score: 82,
      metrics: { seats: "+150 needed", divisions: "3 new" },
      timestamp: "1 hour ago",
      analysis: {
        summary:
          "Enterprise Global is expanding to 3 new divisions and needs approximately 150 additional seats. Multi-year deal potential.",
        patterns: [
          { icon: "🏢", label: "New Divisions", value: "3 coming online" },
          { icon: "👥", label: "Seat Request", value: "~150 additional" },
          { icon: "📅", label: "Timeline", value: "Q1 rollout planned" },
          { icon: "💰", label: "Budget", value: "Approved for expansion" },
        ],
        scenarios: [
          { title: "Enterprise Agreement", impact: "+$180K ARR" },
          { title: "Multi-year Commitment", impact: "+$400K TCV" },
          { title: "Strategic Partnership", impact: "Flagship account" },
        ],
      },
      actions: [
        {
          type: "crm",
          title: "Create Enterprise Opp",
          description: "Log major expansion opportunity",
          due: "Today",
          owner: "Enterprise Sales",
          impact: "Critical",
        },
        {
          type: "email",
          title: "Executive Proposal",
          description: "Send tailored enterprise proposal",
          due: "Tomorrow",
          owner: "Account Exec",
          impact: "High",
        },
      ],
    },
    {
      id: "exp-5",
      company: "StartupBoost",
      type: "Plan Upgrade Ready",
      severity: "low",
      score: 76,
      metrics: { growth: "+85%", features: "All used" },
      timestamp: "2 hours ago",
      analysis: {
        summary:
          "StartupBoost has grown 85% in the past quarter and is using all features in their current plan. Natural upgrade candidate.",
        patterns: [
          { icon: "🚀", label: "Growth Rate", value: "+85% quarterly" },
          { icon: "✅", label: "Feature Usage", value: "100% adoption" },
          { icon: "⏱️", label: "Usage Time", value: "+40% increase" },
          { icon: "👍", label: "Satisfaction", value: "Very positive feedback" },
        ],
        scenarios: [
          { title: "Pro Plan Upgrade", impact: "+$5K ARR" },
          { title: "Startup Growth Bundle", impact: "+$8K ARR" },
          { title: "Annual Commitment", impact: "+20% discount locked" },
        ],
      },
      actions: [
        {
          type: "email",
          title: "Upgrade Incentive",
          description: "Send limited-time upgrade offer",
          due: "Today",
          owner: "Auto-send",
          impact: "Medium",
        },
        {
          type: "crm",
          title: "Flag for Outreach",
          description: "Add to upgrade campaign list",
          due: "Today",
          owner: "Growth Team",
          impact: "Medium",
        },
      ],
    },
    {
      id: "exp-6",
      company: "RetailMax",
      type: "Add-on Interest",
      severity: "low",
      score: 68,
      metrics: { trials: "2 active", interest: "Integrations" },
      timestamp: "3 hours ago",
      analysis: {
        summary: "RetailMax is actively trialing 2 add-on modules and has expressed interest in custom integrations.",
        patterns: [
          { icon: "🧪", label: "Active Trials", value: "2 modules testing" },
          { icon: "🔌", label: "Integration Ask", value: "POS system sync" },
          { icon: "📞", label: "Engagement", value: "3 support calls" },
          { icon: "📈", label: "Trial Usage", value: "Heavy testing" },
        ],
        scenarios: [
          { title: "Add-on Bundle Sale", impact: "+$7K ARR" },
          { title: "Custom Integration", impact: "+$15K services" },
          { title: "Retail Vertical Package", impact: "+$12K ARR" },
        ],
      },
      actions: [
        {
          type: "crm",
          title: "Follow Up on Trial",
          description: "Check in on add-on experience",
          due: "This week",
          owner: "Sales Rep",
          impact: "Medium",
        },
        {
          type: "email",
          title: "Integration Guide",
          description: "Send integration documentation",
          due: "Today",
          owner: "Auto-send",
          impact: "Low",
        },
      ],
    },
  ],
  operations: [
    {
      id: "ops-1",
      company: "System Monitor",
      type: "Performance Alert",
      severity: "critical",
      score: 95,
      metrics: { latency: "+340ms", errors: "2.3%" },
      timestamp: "1 min ago",
      analysis: {
        summary:
          "System latency has increased by 340ms with error rate spiking to 2.3%. Database query optimization needed urgently.",
        patterns: [
          { icon: "⚡", label: "Latency Spike", value: "+340ms avg response" },
          { icon: "❌", label: "Error Rate", value: "2.3% (up from 0.1%)" },
          { icon: "🗄️", label: "DB Load", value: "89% CPU usage" },
          { icon: "👥", label: "Affected Users", value: "~2,400 impacted" },
        ],
        scenarios: [
          { title: "Query Optimization", impact: "-280ms latency" },
          { title: "Cache Implementation", impact: "-60% DB load" },
          { title: "Load Balancer Adjust", impact: "+99.9% uptime" },
        ],
      },
      actions: [
        {
          type: "crm",
          title: "Create Incident Ticket",
          description: "Log P1 incident in monitoring system",
          due: "Immediate",
          owner: "DevOps",
          impact: "Critical",
        },
        {
          type: "email",
          title: "Alert Engineering",
          description: "Notify on-call engineering team",
          due: "Immediate",
          owner: "System",
          impact: "Critical",
        },
      ],
    },
    {
      id: "ops-2",
      company: "API Gateway",
      type: "Rate Limit Warning",
      severity: "high",
      score: 82,
      metrics: { usage: "92%", throttled: "156 reqs" },
      timestamp: "8 min ago",
      analysis: {
        summary:
          "API rate limits approaching capacity with 156 requests throttled in the last hour. Scaling recommended.",
        patterns: [
          { icon: "🔌", label: "Rate Usage", value: "92% of limit" },
          { icon: "⛔", label: "Throttled", value: "156 requests/hour" },
          { icon: "📈", label: "Trend", value: "+15% daily growth" },
          { icon: "🏢", label: "Top Consumer", value: "Enterprise Global" },
        ],
        scenarios: [
          { title: "Tier Upgrade", impact: "+50% capacity" },
          { title: "Rate Limit Optimization", impact: "-30% throttling" },
          { title: "Caching Strategy", impact: "-40% API calls" },
        ],
      },
      actions: [
        {
          type: "crm",
          title: "Review Usage Patterns",
          description: "Analyze top API consumers",
          due: "Today",
          owner: "Platform Team",
          impact: "High",
        },
        {
          type: "email",
          title: "Usage Advisory",
          description: "Send optimization recommendations",
          due: "Today",
          owner: "Auto-send",
          impact: "Medium",
        },
      ],
    },
    {
      id: "ops-3",
      company: "Auth Service",
      type: "Security Event",
      severity: "high",
      score: 88,
      metrics: { attempts: "847 failed", unique: "23 IPs" },
      timestamp: "12 min ago",
      analysis: {
        summary: "Unusual login pattern detected: 847 failed attempts from 23 unique IPs. Possible brute force attack.",
        patterns: [
          { icon: "🔐", label: "Failed Logins", value: "847 in 1 hour" },
          { icon: "🌐", label: "Unique IPs", value: "23 sources" },
          { icon: "🎯", label: "Target Accounts", value: "12 targeted" },
          { icon: "📍", label: "Origin", value: "Multiple countries" },
        ],
        scenarios: [
          { title: "IP Blocking", impact: "Immediate protection" },
          { title: "MFA Enforcement", impact: "+95% security" },
          { title: "Rate Limiting", impact: "-80% attack surface" },
        ],
      },
      actions: [
        {
          type: "recovery",
          title: "Block Suspicious IPs",
          description: "Add IPs to firewall blocklist",
          due: "Immediate",
          owner: "Security",
          impact: "Critical",
        },
        {
          type: "email",
          title: "Security Advisory",
          description: "Notify affected account holders",
          due: "Today",
          owner: "Auto-send",
          impact: "High",
        },
      ],
    },
    {
      id: "ops-4",
      company: "Data Pipeline",
      type: "Sync Delay",
      severity: "medium",
      score: 65,
      metrics: { delay: "45 min", records: "12.4K pending" },
      timestamp: "25 min ago",
      analysis: {
        summary: "Data synchronization running 45 minutes behind schedule with 12,400 records pending processing.",
        patterns: [
          { icon: "⏱️", label: "Current Delay", value: "45 minutes" },
          { icon: "📊", label: "Pending Records", value: "12,400 items" },
          { icon: "🔄", label: "Sync Rate", value: "60% normal speed" },
          { icon: "💾", label: "Queue Size", value: "Growing steadily" },
        ],
        scenarios: [
          { title: "Scale Workers", impact: "-30min delay" },
          { title: "Priority Queue", impact: "Critical data first" },
          { title: "Batch Optimization", impact: "+40% throughput" },
        ],
      },
      actions: [
        {
          type: "crm",
          title: "Monitor Queue",
          description: "Set up enhanced monitoring",
          due: "Today",
          owner: "Data Ops",
          impact: "Medium",
        },
        {
          type: "recovery",
          title: "Scale Processing",
          description: "Increase worker instances",
          due: "Immediate",
          owner: "DevOps",
          impact: "High",
        },
      ],
    },
    {
      id: "ops-5",
      company: "Storage Cluster",
      type: "Capacity Warning",
      severity: "medium",
      score: 72,
      metrics: { used: "78%", growth: "+2.1TB/week" },
      timestamp: "1 hour ago",
      analysis: {
        summary: "Storage cluster at 78% capacity with weekly growth of 2.1TB. Will reach critical levels in ~3 weeks.",
        patterns: [
          { icon: "💾", label: "Current Usage", value: "78% capacity" },
          { icon: "📈", label: "Weekly Growth", value: "+2.1TB/week" },
          { icon: "⏰", label: "Time to Critical", value: "~3 weeks" },
          { icon: "📁", label: "Largest Tenant", value: "Enterprise Global" },
        ],
        scenarios: [
          { title: "Storage Expansion", impact: "+50% capacity" },
          { title: "Data Archival", impact: "-15% usage" },
          { title: "Compression Upgrade", impact: "-20% footprint" },
        ],
      },
      actions: [
        {
          type: "crm",
          title: "Plan Expansion",
          description: "Create storage expansion proposal",
          due: "This week",
          owner: "Infrastructure",
          impact: "High",
        },
        {
          type: "email",
          title: "Usage Report",
          description: "Send storage analysis to stakeholders",
          due: "Today",
          owner: "Auto-send",
          impact: "Low",
        },
      ],
    },
    {
      id: "ops-6",
      company: "CDN Network",
      type: "Cache Miss Rate",
      severity: "low",
      score: 48,
      metrics: { hitRate: "82%", miss: "+8%" },
      timestamp: "2 hours ago",
      analysis: {
        summary: "CDN cache hit rate dropped to 82%, 8% below optimal. Some regions experiencing slower load times.",
        patterns: [
          { icon: "🌐", label: "Hit Rate", value: "82% (target 90%)" },
          { icon: "📍", label: "Affected Regions", value: "APAC, South America" },
          { icon: "⚡", label: "Load Time", value: "+180ms affected areas" },
          { icon: "🔄", label: "Cache Invalidations", value: "Higher than normal" },
        ],
        scenarios: [
          { title: "Cache Rule Optimization", impact: "+8% hit rate" },
          { title: "Regional PoP Addition", impact: "-100ms latency" },
          { title: "TTL Adjustment", impact: "+5% efficiency" },
        ],
      },
      actions: [
        {
          type: "crm",
          title: "Analyze Cache Rules",
          description: "Review and optimize caching strategy",
          due: "This week",
          owner: "Platform",
          impact: "Medium",
        },
        {
          type: "email",
          title: "Performance Update",
          description: "Notify stakeholders of optimization plan",
          due: "Tomorrow",
          owner: "Auto-send",
          impact: "Low",
        },
      ],
    },
  ],
  supply: [
    {
      id: "sup-1",
      company: "Warehouse Alpha",
      type: "Stock Critical",
      severity: "critical",
      score: 94,
      metrics: { sku: "SKU-2847", stock: "12 units" },
      timestamp: "3 min ago",
      analysis: {
        summary:
          "Critical SKU-2847 down to 12 units with average daily demand of 45 units. Stockout imminent within 6 hours.",
        patterns: [
          { icon: "📦", label: "Current Stock", value: "12 units remaining" },
          { icon: "📈", label: "Daily Demand", value: "45 units average" },
          { icon: "⏰", label: "Time to Stockout", value: "~6 hours" },
          { icon: "🚚", label: "Reorder Status", value: "Not initiated" },
        ],
        scenarios: [
          { title: "Emergency Reorder", impact: "Prevent stockout" },
          { title: "Cross-warehouse Transfer", impact: "24hr solution" },
          { title: "Supplier Expedite", impact: "48hr delivery" },
        ],
      },
      actions: [
        {
          type: "recovery",
          title: "Emergency Purchase Order",
          description: "Create priority PO for SKU-2847",
          due: "Immediate",
          owner: "Procurement",
          impact: "Critical",
        },
        {
          type: "email",
          title: "Supplier Alert",
          description: "Notify primary supplier of urgent need",
          due: "Immediate",
          owner: "Auto-send",
          impact: "Critical",
        },
      ],
    },
    {
      id: "sup-2",
      company: "Supplier Network",
      type: "Delivery Delay",
      severity: "high",
      score: 78,
      metrics: { orders: "8 delayed", avg: "+3.2 days" },
      timestamp: "18 min ago",
      analysis: {
        summary: "8 orders from primary supplier experiencing delays averaging 3.2 days. Impact on fulfillment SLAs.",
        patterns: [
          { icon: "📋", label: "Delayed Orders", value: "8 shipments" },
          { icon: "⏱️", label: "Average Delay", value: "+3.2 days" },
          { icon: "🏭", label: "Supplier", value: "GlobalParts Inc" },
          { icon: "📍", label: "Origin", value: "Shipping congestion" },
        ],
        scenarios: [
          { title: "Alternative Supplier", impact: "Immediate availability" },
          { title: "Air Freight Upgrade", impact: "-2 days transit" },
          { title: "Customer Communication", impact: "Manage expectations" },
        ],
      },
      actions: [
        {
          type: "crm",
          title: "Update Delivery ETAs",
          description: "Revise all affected order timelines",
          due: "Today",
          owner: "Logistics",
          impact: "High",
        },
        {
          type: "email",
          title: "Customer Notification",
          description: "Proactive delay communication",
          due: "Today",
          owner: "Auto-send",
          impact: "Medium",
        },
      ],
    },
    {
      id: "sup-3",
      company: "Quality Control",
      type: "Defect Spike",
      severity: "high",
      score: 85,
      metrics: { rate: "4.2%", batch: "B-2024-1847" },
      timestamp: "35 min ago",
      analysis: {
        summary: "Defect rate to 4.2% in batch B-2024-1847, well above 1% threshold. Quality hold recommended.",
        patterns: [
          { icon: "⚠️", label: "Defect Rate", value: "4.2% (threshold 1%)" },
          { icon: "📦", label: "Affected Batch", value: "B-2024-1847" },
          { icon: "🔍", label: "Defect Type", value: "Component failure" },
          { icon: "📊", label: "Units Affected", value: "~840 potential" },
        ],
        scenarios: [
          { title: "Quality Hold", impact: "Prevent distribution" },
          { title: "Supplier Audit", impact: "Root cause analysis" },
          { title: "Batch Recall", impact: "Customer protection" },
        ],
      },
      actions: [
        {
          type: "recovery",
          title: "Initiate Quality Hold",
          description: "Stop batch distribution pending review",
          due: "Immediate",
          owner: "QA Team",
          impact: "Critical",
        },
        {
          type: "crm",
          title: "Supplier Notification",
          description: "Alert supplier of quality issue",
          due: "Today",
          owner: "Procurement",
          impact: "High",
        },
      ],
    },
    {
      id: "sup-4",
      company: "Distribution Hub",
      type: "Capacity Strain",
      severity: "medium",
      score: 67,
      metrics: { utilization: "94%", backlog: "2,400 units" },
      timestamp: "1 hour ago",
      analysis: {
        summary: "Distribution hub at 94% capacity with 2,400 unit backlog. Peak season approaching requires action.",
        patterns: [
          { icon: "🏭", label: "Capacity Used", value: "94% utilized" },
          { icon: "📦", label: "Backlog", value: "2,400 units" },
          { icon: "📅", label: "Peak Season", value: "Starts in 2 weeks" },
          { icon: "👥", label: "Staffing", value: "85% coverage" },
        ],
        scenarios: [
          { title: "Temporary Staff", impact: "+30% throughput" },
          { title: "Overflow Facility", impact: "+50% capacity" },
          { title: "Shift Extension", impact: "+20% daily output" },
        ],
      },
      actions: [
        {
          type: "crm",
          title: "Capacity Planning",
          description: "Create peak season staffing plan",
          due: "This week",
          owner: "Operations",
          impact: "High",
        },
        {
          type: "email",
          title: "Staffing Request",
          description: "Send temporary staffing requirements",
          due: "Today",
          owner: "HR",
          impact: "Medium",
        },
      ],
    },
    {
      id: "sup-5",
      company: "Inventory System",
      type: "Forecast Variance",
      severity: "medium",
      score: 58,
      metrics: { variance: "+23%", categories: "4 affected" },
      timestamp: "2 hours ago",
      analysis: {
        summary: "Demand forecast showing +23% variance across 4 product categories. Inventory adjustment recommended.",
        patterns: [
          { icon: "📊", label: "Forecast Variance", value: "+23% above plan" },
          { icon: "📁", label: "Categories", value: "4 impacted" },
          { icon: "📈", label: "Trend", value: "Upward demand" },
          { icon: "💰", label: "Revenue Impact", value: "+$180K potential" },
        ],
        scenarios: [
          { title: "Forecast Revision", impact: "Accurate planning" },
          { title: "Safety Stock Increase", impact: "-50% stockout risk" },
          { title: "Supplier Prep", impact: "Faster response" },
        ],
      },
      actions: [
        {
          type: "crm",
          title: "Update Forecasts",
          description: "Revise demand forecasts for Q2",
          due: "This week",
          owner: "Planning",
          impact: "Medium",
        },
        {
          type: "email",
          title: "Supplier Advisory",
          description: "Notify suppliers of increased demand",
          due: "Tomorrow",
          owner: "Auto-send",
          impact: "Low",
        },
      ],
    },
    {
      id: "sup-6",
      company: "Returns Center",
      type: "RMA Backlog",
      severity: "low",
      score: 45,
      metrics: { pending: "342 RMAs", avg: "8.5 days" },
      timestamp: "3 hours ago",
      analysis: {
        summary: "Return merchandise authorization backlog at 342 items with average processing time of 8.5 days.",
        patterns: [
          { icon: "📋", label: "Pending RMAs", value: "342 items" },
          { icon: "⏱️", label: "Processing Time", value: "8.5 days average" },
          { icon: "💰", label: "Credit Value", value: "$48,200 pending" },
          { icon: "😤", label: "Customer Impact", value: "15 complaints" },
        ],
        scenarios: [
          { title: "Process Automation", impact: "-40% processing time" },
          { title: "Staff Augmentation", impact: "-3 days backlog" },
          { title: "Self-service Portal", impact: "-50% manual work" },
        ],
      },
      actions: [
        {
          type: "crm",
          title: "RMA Review",
          description: "Prioritize high-value returns",
          due: "Today",
          owner: "Returns Team",
          impact: "Medium",
        },
        {
          type: "email",
          title: "Status Updates",
          description: "Send bulk status update to customers",
          due: "Today",
          owner: "Auto-send",
          impact: "Low",
        },
      ],
    },
  ],
  quality: [
    {
      id: "quality-1",
      company: "Alpha Manufacturing",
      type: "Defect Spike",
      severity: "critical",
      score: 95,
      metrics: { batch: "B-2024-1847", rate: "4.2%" },
      timestamp: "5 min ago",
      agentRunId: "run_12345",
      useCase: "quality_incident",
      analysis: {
        summary:
          "Defect rate for batch B-2024-1847 has spiked to 4.2%, significantly exceeding the acceptable threshold of 1%. This indicates a potential issue in the production process.",
        patterns: [
          { icon: "⚠️", label: "Defect Rate", value: "4.2% (threshold 1%)" },
          { icon: "📦", label: "Affected Batch", value: "B-2024-1847" },
          { icon: "🔍", label: "Defect Type", value: "Component Failure" },
          { icon: "📊", label: "Units Affected", value: "~840 units" },
        ],
        scenarios: [
          { title: "Initiate Quality Hold", impact: "Prevent distribution of affected batch" },
          { title: "Supplier Root Cause Analysis", impact: "Identify and address supplier defect source" },
          { title: "Batch Recall", impact: "Protect customer safety and brand reputation" },
        ],
      },
      actions: [
        {
          type: "recovery",
          title: "Initiate Quality Hold",
          description: "Place batch B-2024-1847 on quality hold, preventing further distribution.",
          due: "Immediate",
          owner: "QA Team",
          impact: "Critical",
        },
        {
          type: "crm",
          title: "Notify Supplier",
          description: "Alert the supplier about the defect rate and request immediate investigation.",
          due: "Today",
          owner: "Procurement",
          impact: "High",
        },
      ],
    },
    {
      id: "quality-2",
      company: "Beta Electronics",
      type: "Performance Degradation",
      severity: "high",
      score: 82,
      metrics: { latency: "+250ms", errors: "1.5%" },
      timestamp: "15 min ago",
      agentRunId: "run_67890",
      useCase: "quality_incident",
      analysis: {
        summary:
          "System latency has increased by 250ms, and the error rate has risen to 1.5%. This could impact user experience and system reliability.",
        patterns: [
          { icon: "⚡", label: "Latency Spike", value: "+250ms average" },
          { icon: "❌", label: "Error Rate", value: "1.5% (from 0.3%)" },
          { icon: "🗄️", label: "DB Load", value: "75% CPU usage" },
        ],
        scenarios: [
          { title: "Optimize Database Queries", impact: "Reduce latency by 150ms" },
          { title: "Implement Caching Layer", impact: "Decrease DB load by 40%" },
          { title: "Scale Infrastructure", impact: "Improve system resilience" },
        ],
      },
      actions: [
        {
          type: "recovery",
          title: "Optimize Database Queries",
          description: "Analyze and optimize slow-running database queries.",
          due: "Immediate",
          owner: "DevOps",
          impact: "High",
        },
        {
          type: "email",
          title: "Notify Engineering Team",
          description: "Alert the on-call engineering team about the performance degradation.",
          due: "Immediate",
          owner: "System",
          impact: "Critical",
        },
      ],
    },
  ],
  qbr: [
    {
      id: "qbr-1",
      company: "Acme Corp",
      type: "QBR Auto-Generation",
      severity: "low",
      score: 90,
      metrics: { qtr: "Q1 2024", status: "Ready" },
      timestamp: "1 hour ago",
      agentRunId: "qbr_run_abc",
      useCase: "qbr_auto_generation",
      analysis: {
        summary: "QBR report for Acme Corp for Q1 2024 is ready. Key insights and recommendations are highlighted.",
        patterns: [
          { icon: "📅", label: "Quarter", value: "Q1 2024" },
          { icon: "📄", label: "Report Status", value: "Generated" },
          { icon: "📈", label: "Key Trends", value: "Positive growth in user engagement" },
          { icon: "⚠️", label: "Risks", value: "Potential churn indicators identified" },
        ],
        scenarios: [
          { title: "Review Growth Opportunities", impact: "+$20K ARR" },
          { title: "Address Churn Risks", impact: "+10% Retention" },
          { title: "Strategic Planning Session", impact: "Alignment on future roadmap" },
        ],
      },
      actions: [
        {
          type: "crm",
          title: "Schedule QBR Meeting",
          description: "Book a meeting with Acme Corp stakeholders to discuss the QBR.",
          due: "This Week",
          owner: "Account Manager",
          impact: "High",
        },
        {
          type: "email",
          title: "Send QBR Report Summary",
          description: "Email a summary of the QBR findings to key stakeholders.",
          due: "Today",
          owner: "Auto-send",
          impact: "Medium",
        },
        {
          type: "presentation",
          title: "Prepare Presentation Deck",
          description: "Generate a presentation deck based on the QBR analysis.",
          due: "Tomorrow",
          owner: "Sales Enablement",
          impact: "High",
        },
      ],
    },
    {
      id: "qbr-2",
      company: "Beta Electronics",
      type: "QBR Auto-Generation",
      severity: "low",
      score: 88,
      metrics: { qtr: "Q1 2024", status: "Processing" },
      timestamp: "2 hours ago",
      agentRunId: "qbr_run_def",
      useCase: "qbr_auto_generation",
      analysis: {
        summary:
          "QBR report for Beta Electronics for Q1 2024 is currently being generated. Key metrics and insights will be available shortly.",
        patterns: [
          { icon: "⏳", label: "Status", value: "Processing" },
          { icon: "📊", label: "Data Sources", value: "Pulling from CRM, Usage, and Support" },
          { icon: "🤖", label: "Agent", value: "QBR Auto-Generation Agent" },
        ],
        scenarios: [
          { title: "Monitor Generation Progress", impact: "Ensure timely report delivery" },
          { title: "Review Draft Report", impact: "Initial quality check" },
        ],
      },
      actions: [
        {
          type: "crm",
          title: "Create QBR Task",
          description: "Monitor QBR generation status.",
          due: "Today",
          owner: "System",
          impact: "Low",
        },
      ],
    },
  ],
}

const agentNames = {
  churn: "Churn Prevention Agent",
  expansion: "Revenue Expansion Agent",
  quality: "Quality Incidents Agent", // Renamed from operations
  qbr: "QBR Auto-Generation Agent", // Added QBR agent name
  supply: "Supply Chain Agent",
}

// ========================================
// API Configuration
// ========================================

const useCaseToAPIParam = {
  // Short names from navigation/state
  churn: "churn_risk",
  expansion: "expansion_opportunity",
  qbr: "qbr_auto_generation",
  supply: "supply_risk",
  quality: "quality_incident",

  // Full API names from data (handle direct mapping)
  churn_risk: "churn_risk",
  expansion_opportunity: "expansion_opportunity",
  qbr_auto_generation: "qbr_auto_generation",
  supply_risk: "supply_risk",
  quality_incident: "quality_incident",
}

const API_CONFIG = {
  baseUrl: "http://localhost:5000",
  endpoints: {
    getSignals: (useCase) => `/signals/left-pane/${useCaseToAPIParam[useCase] || "churn_risk"}`,
    getAgentData: (useCase, accountId, agentRunId) =>
      `/agent/data/${useCaseToAPIParam[useCase] || "quality_incident"}/${accountId}/${agentRunId}`,
  },
}

// ========================================
// State Management
// ========================================

const state = {
  currentUseCase: "churn",
  selectedAlert: null,
  theme: "dark",
  modalStep: 1,
  approvedActions: new Set(),
  editedActions: new Map(),
  editingActionIndex: null,
  typingAnimationId: null,
  typingTimeoutId: null,
  currentAlerts: null, // Store fetched alerts here
}

// ========================================
// DOM Elements
// ========================================

// Declare elements object at top level, initialize in init()
let elements = {}

// ========================================
// API Functions
// ========================================

async function loadAlertsFromAPI(useCase = "churn") {
  console.log("[v0] loadAlertsFromAPI called with useCase:", useCase)
  try {
    const apiParam = useCaseToAPIParam[useCase] || "churn_risk"
    console.log("[v0] Mapped API param:", apiParam)
    const url = `${API_CONFIG.baseUrl}/signals/left-pane/${apiParam}`

    console.log(`[v0] Fetching alerts from: ${url}`)

    const response = await fetch(url)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const jsonData = await response.json()
    console.log("[v0] API response received:", jsonData)

    // Handle your Flask API response structure - extract data array
    const apiData = jsonData.data || jsonData

    if (!Array.isArray(apiData)) {
      console.error("[v0] API response is not an array:", apiData)
      throw new Error("Invalid API response format")
    }

    const transformedData = transformAPIData(apiData)
    console.log("[v0] Transformed data:", transformedData)

    return transformedData
  } catch (error) {
    console.error("[v0] Error loading alerts from API:", error)

    // Check if it's a CORS error
    if (error.message.includes("Failed to fetch") || error.name === "TypeError") {
      console.error(`
╔═══════════════════════════════════════════════════════════════╗
║  CORS ERROR: Cannot connect to Flask API                     ║
╠═══════════════════════════════════════════════════════════════╣
║  Add this to your Flask app:                                  ║
║                                                               ║
║  from flask_cors import CORS                                  ║
║  app = Flask(__name__)                                        ║
║  CORS(app)                                                    ║
╚═══════════════════════════════════════════════════════════════╝
      `)
      showToast("warning", "API Connection Failed", "Using demo data. Check console for CORS setup.")
    }

    return null
  }
}

async function fetchAgentData(accountId, agentRunId, useCase) {
  // Adjusted parameter order to match API_CONFIG.endpoints.getAgentData
  try {
    const endpoint = API_CONFIG.endpoints.getAgentData(useCase, accountId, agentRunId)
    const url = `${API_CONFIG.baseUrl}${endpoint}`

    console.log(`[v0] Fetching agent data from: ${url}`)

    const response = await fetch(url)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    console.log(`[v0] Agent data received:`, data)

    if (data.error) {
      console.warn(`[v0] API returned error: ${data.error}`)
      return null
    }

    return data.data || data
  } catch (error) {
    console.error("[v0] Error fetching agent data:", error)

    if (error.message.includes("Failed to fetch") || error.message.includes("CORS")) {
      console.error("[v0] CORS Error - Make sure Flask has CORS enabled")
      showToast("Unable to fetch agent details. Check CORS configuration.", "error")
    } else {
      showToast("Failed to load agent details", "error")
    }

    return null
  }
}

// Modified loadAgentDataFromAPI to use the new fetchAgentData function
async function loadAgentDataFromAPI(alert) {
  try {
    const { useCase, id: accountId, agentRunId } = alert
    if (!agentRunId) {
      console.log(`[v0] No agentRunId for alert ${accountId}, using cached data.`)
      return {
        analysis: alert.analysis,
        actions: alert.actions,
      }
    }
    // Pass useCase to fetchAgentData
    const fetchedData = await fetchAgentData(accountId, agentRunId, useCase)

    if (fetchedData) {
      return {
        analysis: fetchedData.analysis || alert.analysis, // Fallback to cached if API misses fields
        actions: fetchedData.actions || alert.actions, // Fallback to cached if API misses fields
        // Include other relevant data from fetchedData if needed for quality incident view
        qualityIncidentData: fetchedData.qualityIncidentData || null,
        // Include other relevant data from fetchedData if needed for expansion opportunity view
        middle_panel: fetchedData.middle_panel || null,
        right_panel: fetchedData.right_panel || null,
        brief: fetchedData.brief || null, // Add brief for quality incident view
        // Add QBR specific data
        trends: fetchedData.trends || null,
        root_causes: fetchedData.root_causes || null,
        opportunities: fetchedData.opportunities || null,
        signals: fetchedData.signals || null, // Add signals for QBR
        // Add QBR right panel data
        deck: fetchedData.deck || null,
        talking_points: fetchedData.talking_points || null,
        // Add churn specific data
        commercial_brief: fetchedData.commercial_brief || null,
        detected_root_causes: fetchedData.detected_root_causes || null,
        risk_summary: fetchedData.risk_summary || null,
        email_draft: fetchedData.email_draft || null,
        // Supply specific data
        recovery: fetchedData.recovery || null,
      }
    } else {
      // If fetching failed, return cached data
      return {
        analysis: alert.analysis,
        actions: alert.actions,
      }
    }
  } catch (error) {
    console.error(`[v0] Error processing agent data for alert ${alert.id}:`, error)
    // Fallback to using the existing alert data if any error occurs
    showToast("warning", "Failed to load agent data", "Using cached data for analysis.")
    return {
      analysis: alert.analysis,
      actions: alert.actions,
    }
  }
}

function transformAPIData(apiData) {
  // Handle your Flask API response structure
  return apiData.map((item) => ({
    id: item.account_id || `alert-${Date.now()}-${Math.random()}`,
    company: item.account_name || "Unknown Company",
    type: item.use_case || "churn_risk",
    severity: item.risk_level ? item.risk_level.toLowerCase() : "medium",
    score: Number.parseFloat(item.final_score) * 100 || 50, // Convert "0.33" to 33
    metrics: Array.isArray(item.indicators) ? item.indicators : [], // Store indicators array
    timestamp: item.detected_ago || "just now",
    agentRunId: item.agent_run_id || null, // Store agent run ID for API calls
    useCase: item.use_case || "churn_risk", // Store use case for API calls
    analysis: item.analysis || {
      summary: `${item.account_name} showing ${item.risk_level} risk signals`,
      patterns: item.indicators || [],
      scenarios: [],
    },
    actions: item.actions || [],
    // Add a placeholder for detailed data that will be fetched
    detailedData: null,
  }))
}

async function refreshAlerts() {
  console.log("[v0] Refreshing alerts from API...")
  // Pass the current use case to fetchAlertsFromAPI
  const apiAlerts = await loadAlertsFromAPI(state.currentUseCase)
  state.currentAlerts = apiAlerts
  renderAlerts()
}

// ========================================
// Initialization
// ========================================

async function init() {
  console.log("[v0] Initializing application...")

  // Check if button exists
  const runAnalysisBtn = document.getElementById("runAnalysisBtn")
  console.log("[v0] runAnalysisBtn element:", runAnalysisBtn)
  console.log("[v0] runAnalysisBtn display style:", runAnalysisBtn ? runAnalysisBtn.style.display : "element not found")

  // Set initial theme
  document.documentElement.setAttribute("data-theme", state.theme)

  // Initialize all DOM element references
  elements = {
    alertsList: document.getElementById("alertsList"),
    alertCount: document.getElementById("alertCount"),
    agentName: document.getElementById("agentName"),
    analysisContent: document.getElementById("analysisContent"),
    summarySection: document.getElementById("summarySection"),
    summaryText: document.getElementById("summaryText"),
    patternsSection: document.getElementById("patternsSection"),
    patternsGrid: document.getElementById("patternsGrid"),
    scenariosSection: document.getElementById("scenariosSection"),
    scenariosList: document.getElementById("scenariosList"),
    actionsList: document.getElementById("actionsList"),
    qualityIncidentView: document.getElementById("qualityIncidentView"),
    expansionOpportunityView: document.getElementById("expansionOpportunityView"),
    defaultAnalysisView: document.getElementById("defaultAnalysisView"),
    qbrView: document.getElementById("qbrView"), // Keep this for initial check, will be created if missing
    qualityIncidentActions: document.getElementById("qualityIncidentActions"),
    expansionOpportunityActions: document.getElementById("expansionOpportunityActions"),
    // Add QBR actions container to elements
    qbrActions: document.getElementById("qbrActions"),
    modalOverlay: document.getElementById("modalOverlay"),
    toastContainer: document.getElementById("toastContainer"),
    themeToggle: document.getElementById("themeToggle"),
    createAgentBtn: document.getElementById("createAgentBtn"),
    modalClose: document.getElementById("modalClose"),
    modalBack: document.getElementById("modalBack"),
    modalNext: document.getElementById("modalNext"),
    approveActionsBtn: document.getElementById("approveActionsBtn"),
    simulateBtn: document.getElementById("simulateBtn"),
    evidenceBtn: document.getElementById("evidenceBtn"),
    approveAllBtn: document.getElementById("exportBtn"),
    exportBtn: document.getElementById("exportBtn"),
    thresholdInput: document.getElementById("thresholdInput"),
    thresholdValue: document.getElementById("thresholdValue"),
  }

  console.log("[v0] Elements initialized, qbrView:", elements.qbrView)

  console.log("[v0] About to call loadAlertsFromAPI with useCase:", state.currentUseCase)
  // Fetch alerts from Flask API
  const apiAlerts = await loadAlertsFromAPI(state.currentUseCase) // Pass currentUseCase
  console.log("[v0] loadAlertsFromAPI returned:", apiAlerts)
  state.currentAlerts = apiAlerts

  // Render initial alerts
  renderAlerts()

  // Select first alert
  const alerts = state.currentAlerts || alertsData[state.currentUseCase]
  if (alerts.length > 0) {
    selectAlert(alerts[0])
  }

  // Setup event listeners
  setupEventListeners()
}

// ========================================
// Event Listeners
// ========================================

function setupEventListeners() {
  // Use case tabs
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      const useCase = tab.dataset.usecase
      switchUseCase(useCase)
    })
  })

  // Theme toggle
  elements.themeToggle.addEventListener("click", toggleTheme)

  // Create agent button
  elements.createAgentBtn.addEventListener("click", openModal)

  // Modal controls
  elements.modalClose.addEventListener("click", closeModal)
  elements.modalOverlay.addEventListener("click", (e) => {
    if (e.target === elements.modalOverlay) closeModal()
  })
  elements.modalBack.addEventListener("click", prevModalStep)
  elements.modalNext.addEventListener("click", nextModalStep)

  // Analysis action buttons
  if (elements.approveActionsBtn) {
    elements.approveActionsBtn.addEventListener("click", () => {
      approveAllActions()
      showToast("success", "Actions Approved", "All recommended actions have been approved")
    })
  }

  if (elements.simulateBtn) {
    elements.simulateBtn.addEventListener("click", () => {
      showToast("info", "Simulation Started", "Running impact simulation...")
    })
  }

  if (elements.evidenceBtn) {
    elements.evidenceBtn.addEventListener("click", () => {
      showToast("info", "Loading Evidence", "Gathering supporting data...")
    })
  }

  // Bulk action buttons
  if (elements.approveAllBtn) {
    elements.approveAllBtn.addEventListener("click", () => {
      approveAllActions()
      showToast("success", "Bulk Approval", "All pending actions approved")
    })
  }

  if (elements.exportBtn) {
    elements.exportBtn.addEventListener("click", () => {
      showToast("info", "Exporting", "Generating action report...")
    })
  }

  // Threshold slider
  if (elements.thresholdInput) {
    elements.thresholdInput.addEventListener("input", (e) => {
      elements.thresholdValue.textContent = e.target.value
    })
  }

  // Data source toggles
  document.querySelectorAll(".data-source").forEach((source) => {
    source.addEventListener("click", () => {
      source.classList.toggle("active")
      updatePreview()
    })
  })

  // Add click listeners for alert cards
  // This part will be dynamically re-attached after rendering, so it's fine here for setup
  document.querySelectorAll(".alert-card").forEach((card) => {
    attachAlertCardListeners(card)
  })
}

// Helper function to attach listeners to a single alert card
function attachAlertCardListeners(card) {
  card.addEventListener("click", async () => {
    const alertId = card.dataset.id
    const alert = (state.currentAlerts || alertsData[state.currentUseCase]).find((a) => a.id === alertId)
    if (alert) {
      // Fetch detailed data if available and not already loaded
      if (alert.agentRunId && alert.useCase && !alert.detailedData) {
        const agentData = await fetchAgentData(alert.id, alert.agentRunId, alert.useCase)
        if (agentData) {
          alert.detailedData = agentData // Store fetched data
          console.log("[v0] Detailed agent data loaded for:", alert.company)
        }
      }
      selectAlert(alert)
    }
  })
  card.addEventListener("keydown", async (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault()
      const alertId = card.dataset.id
      const alert = (state.currentAlerts || alertsData[state.currentUseCase]).find((a) => a.id === alertId)
      if (alert) {
        if (alert.agentRunId && alert.useCase && !alert.detailedData) {
          const agentData = await fetchAgentData(alert.id, alert.agentRunId, alert.useCase)
          if (agentData) {
            alert.detailedData = agentData
            console.log("[v0] Detailed agent data loaded for:", alert.company)
          }
        }
        selectAlert(alert)
      }
    }
  })
}

// ========================================
// Use Case Switching
// ========================================

async function switchUseCase(useCase) {
  state.currentUseCase = useCase
  state.selectedAlert = null
  state.approvedActions.clear()
  state.editedActions.clear()
  state.currentAlerts = null // Clear cached alerts to refetch

  // Update tab states
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.classList.toggle("active", tab.dataset.usecase === useCase)
  })

  // Update agent name
  elements.agentName.textContent = agentNames[useCase]

  clearAnalysisPanels()

  const apiAlerts = await loadAlertsFromAPI(useCase)

  if (apiAlerts && apiAlerts.length > 0) {
    state.currentAlerts = apiAlerts
    console.log(`[v0] Loaded ${apiAlerts.length} alerts for ${useCase} from API`)
  } else {
    // Fallback to mock data
    state.currentAlerts = alertsData[useCase] || []
    console.log(`[v0] Using mock data for ${useCase}`)
  }

  renderAlerts()
}

function clearAnalysisPanels() {
  // Hide all specific views and show default
  if (elements.qualityIncidentView) {
    elements.qualityIncidentView.style.display = "none"
  }
  if (elements.expansionOpportunityView) {
    elements.expansionOpportunityView.style.display = "none"
  }
  // Hide QBR view
  if (elements.qbrView) {
    elements.qbrView.style.display = "none"
  }
  // Hide Churn view
  const churnViewContainer = document.getElementById("churnView")
  if (churnViewContainer) {
    churnViewContainer.style.display = "none"
  }
  // Hide Supply view
  const supplyViewContainer = document.getElementById("supplyView")
  if (supplyViewContainer) {
    supplyViewContainer.style.display = "none"
  }

  if (elements.defaultAnalysisView) {
    elements.defaultAnalysisView.style.display = "block"
    // Clear content of the default analysis view
    elements.defaultAnalysisView.innerHTML =
      '<div style="padding: 2rem; text-align: center; color: #94a3b8;">Select an account to view details</div>'
  }

  // Clear content of default actions list and hide specific action containers
  if (elements.actionsList) {
    elements.actionsList.innerHTML =
      '<div style="padding: 1rem; text-align: center; color: #94a3b8;">No actions available</div>'
  }
  if (elements.qualityIncidentActions) {
    elements.qualityIncidentActions.style.display = "none"
  }
  if (elements.expansionOpportunityActions) {
    elements.expansionOpportunityActions.style.display = "none"
  }
  // Hide QBR actions container if it exists
  if (elements.qbrActions) {
    elements.qbrActions.style.display = "none"
  }
  // Hide Churn actions container
  const churnActionsContainer = document.getElementById("churnActions")
  if (churnActionsContainer) {
    churnActionsContainer.style.display = "none"
  }
  // Hide Supply actions container
  const supplyActionsContainer = document.getElementById("supplyActions")
  if (supplyActionsContainer) {
    supplyActionsContainer.style.display = "none"
  }
}

// ========================================
// Alert Rendering
// ========================================

function renderAlerts() {
  const alerts = state.currentAlerts || alertsData[state.currentUseCase]
  elements.alertCount.textContent = alerts.length

  elements.alertsList.innerHTML = alerts
    .map(
      (alert) => `
    <div class="alert-card ${state.selectedAlert?.id === alert.id ? "active" : ""}"
         data-id="${alert.id}"
         tabindex="0"
         role="button"
         aria-label="View details for ${alert.company}">
      <div class="alert-header-simple">
        <h3 class="alert-company-name">${alert.company}</h3>
      </div>
      <div class="alert-score-severity">
        <span class="alert-score-label">Score: <strong>${(alert.score / 100).toFixed(2)}</strong></span>
        <span class="alert-severity-badge ${alert.severity}">${alert.severity.toUpperCase()}</span>
      </div>
      <div class="alert-tags">
        ${
          Array.isArray(alert.metrics) && alert.metrics.length > 0
            ? alert.metrics.map((indicator) => `<span class="alert-tag">${indicator}</span>`).join("")
            : alert.type
              ? `<span class="alert-tag">${alert.type}</span>`
              : ""
        }
      </div>
      <div class="alert-timestamp-simple">Detected ${alert.timestamp}</div>
    </div>
  `,
    )
    .join("")

  // Add listeners to newly rendered cards
  document.querySelectorAll(".alert-card").forEach((card) => {
    // Avoid re-attaching listeners if they already exist
    if (!card.dataset.listenerAttached) {
      attachAlertCardListeners(card)
      card.dataset.listenerAttached = "true"
    }
  })
}

// ========================================
// Alert Selection & Analysis
// ========================================

function selectAlert(alertData) {
  state.selectedAlert = alertData

  // Remove active class from all cards
  document.querySelectorAll(".alert-card").forEach((card) => {
    card.classList.remove("active")
  })

  // Add active class to the selected card
  const selectedCard = document.querySelector(`.alert-card[data-id="${alertData.id}"]`)
  if (selectedCard) {
    selectedCard.classList.add("active")
  }

  // Fetch detailed agent data if needed
  if (alertData.agentRunId && alertData.useCase) {
    fetchAgentData(alertData.id, alertData.agentRunId, alertData.useCase)
      .then((agentData) => {
        if (agentData) {
          alertData.detailedData = agentData // Store fetched data
          console.log("[v0] Detailed agent data loaded for:", alertData.company)
        } else {
          console.warn("[v0] Failed to fetch agent data, using cached or default data.")
        }
        renderSpecificView(alertData.useCase, alertData, alertData.detailedData) // Render the appropriate view after data fetch
      })
      .catch((error) => {
        console.error("[v0] Error during fetchAgentData in selectAlert:", error)
        renderSpecificView(alertData.useCase, alertData, alertData.detailedData) // Attempt to render with potentially partial data
      })
  } else {
    renderSpecificView(alertData.useCase, alertData, alertData.detailedData) // Render if no agentRunId or useCase
  }
}

// CHANGE: Hiding qbrActions when switching to other tabs
function renderSpecificView(useCase, alertData, detailedData) {
  console.log("[v0] renderSpecificView called with useCase:", useCase)
  console.log("[v0] detailedData:", detailedData)

  // Get references to view containers
  const qualityViewContainer = elements.qualityIncidentView
  const expansionViewContainer = elements.expansionOpportunityView
  const qbrViewContainer = document.getElementById("qbrView")
  const churnViewContainer = document.getElementById("churnView")
  const supplyViewContainer = document.getElementById("supplyView") // Get supply view container
  const defaultViewContainer = elements.defaultAnalysisView

  const qualityActionsContainer = elements.qualityIncidentActions
  const expansionActionsContainer = elements.expansionOpportunityActions
  const defaultActionsContainer = elements.actionsList
  const qbrActionsContainer = document.getElementById("qbrActions")
  const churnActionsContainer = document.getElementById("churnActions")
  const supplyActionsContainer = document.getElementById("supplyActions") // Get supply actions container

  // Hide all specific views and actions first
  if (qualityViewContainer) qualityViewContainer.style.display = "none"
  if (expansionViewContainer) expansionViewContainer.style.display = "none"
  if (qbrViewContainer) qbrViewContainer.style.display = "none"
  if (churnViewContainer) churnViewContainer.style.display = "none"
  if (supplyViewContainer) supplyViewContainer.style.display = "none" // Hide supply view
  if (defaultViewContainer) defaultViewContainer.style.display = "block"

  if (qualityActionsContainer) qualityActionsContainer.style.display = "none"
  if (expansionActionsContainer) expansionActionsContainer.style.display = "none"
  if (qbrActionsContainer) qbrActionsContainer.style.display = "none"
  if (churnActionsContainer) churnActionsContainer.style.display = "none"
  if (supplyActionsContainer) supplyActionsContainer.style.display = "none" // Hide supply actions
  if (defaultActionsContainer) defaultActionsContainer.style.display = "block"

  // Reset default view content
  if (defaultViewContainer) {
    defaultViewContainer.innerHTML =
      '<div style="padding: 2rem; text-align: center; color: #94a3b8;">Select an account to view details</div>'
  }
  if (defaultActionsContainer) {
    defaultActionsContainer.innerHTML =
      '<div style="padding: 1rem; text-align: center; color: #94a3b8;">No actions available</div>'
  }

  if (useCase === "quality_incident" && detailedData?.brief) {
    console.log("[v0] Rendering quality incident view")
    if (qualityViewContainer) qualityViewContainer.style.display = "block"
    if (defaultViewContainer) defaultViewContainer.style.display = "none"
    if (qualityActionsContainer) qualityActionsContainer.style.display = "block"
    if (defaultActionsContainer) defaultActionsContainer.style.display = "none"
    renderQualityIncidentView(detailedData, qualityViewContainer)
    renderQualityIncidentActions(detailedData, qualityActionsContainer)
  } else if (useCase === "expansion_opportunity" && detailedData?.middle_panel) {
    console.log("[v0] Rendering expansion opportunity view")
    if (expansionViewContainer) expansionViewContainer.style.display = "block"
    if (defaultViewContainer) defaultViewContainer.style.display = "none"
    if (expansionActionsContainer) expansionActionsContainer.style.display = "block"
    if (defaultActionsContainer) defaultActionsContainer.style.display = "none"
    renderExpansionOpportunityView(detailedData.middle_panel, expansionViewContainer)
    renderExpansionActions(detailedData.right_panel, expansionActionsContainer)
  } else if (useCase === "qbr" || useCase === "qbr_auto_generation") {
    console.log("[v0] Rendering QBR view")

    let qbrViewContainer = document.getElementById("qbrView")
    if (!qbrViewContainer) {
      const analysisContent = document.getElementById("analysisContent")
      if (analysisContent) {
        qbrViewContainer = document.createElement("div")
        qbrViewContainer.id = "qbrView"
        qbrViewContainer.style.display = "none"
        analysisContent.insertBefore(qbrViewContainer, analysisContent.firstChild)
      }
    }

    let qbrActionsContainer = document.getElementById("qbrActions")
    if (!qbrActionsContainer) {
      const panelRight = document.querySelector(".panel-right")
      if (panelRight) {
        qbrActionsContainer = document.createElement("div")
        qbrActionsContainer.id = "qbrActions"
        qbrActionsContainer.style.display = "none"
        panelRight.insertBefore(qbrActionsContainer, panelRight.firstChild)
      }
    }

    console.log("[v0] qbrViewContainer:", qbrViewContainer)
    console.log("[v0] qbrActionsContainer:", qbrActionsContainer)
    console.log("[v0] qbrActionsContainer display:", qbrActionsContainer?.style.display)

    if (qbrViewContainer) {
      qbrViewContainer.style.display = "block"
      if (defaultViewContainer) defaultViewContainer.style.display = "none"
      if (qualityViewContainer) qualityViewContainer.style.display = "none"
      if (expansionViewContainer) expansionViewContainer.style.display = "none"

      if (qbrActionsContainer) {
        console.log("[v0] Calling renderQBRActions with data")
        qbrActionsContainer.style.display = "block"
      }
      if (qualityActionsContainer) qualityActionsContainer.style.display = "none"
      if (expansionActionsContainer) expansionActionsContainer.style.display = "none"
      if (defaultActionsContainer) defaultActionsContainer.style.display = "none"

      renderQBRView(detailedData, qbrViewContainer)

      if (qbrActionsContainer) {
        console.log("[v0] Calling renderQBRActions with data")
        renderQBRActions(detailedData, qbrActionsContainer)
      } else {
        console.error("[v0] qbrActionsContainer is null after creation attempt")
      }
    }
  } else if (useCase === "churn_risk" || useCase === "churn") {
    console.log("[v0] Rendering Churn view")

    if (!detailedData || !detailedData.risk_summary) {
      console.warn("[v0] No churn data available, showing default view")
      if (defaultViewContainer) {
        defaultViewContainer.innerHTML =
          '<div style="padding: 2rem; text-align: center; color: #94a3b8;">No churn risk data available for this account</div>'
        defaultViewContainer.style.display = "block"
      }
      if (defaultActionsContainer) {
        defaultActionsContainer.innerHTML =
          '<div style="padding: 1rem; text-align: center; color: #94a3b8;">No actions available</div>'
        defaultActionsContainer.style.display = "block"
      }
      return
    }

    let churnViewContainer = document.getElementById("churnView")
    if (!churnViewContainer) {
      const analysisContent = document.getElementById("analysisContent")
      if (analysisContent) {
        churnViewContainer = document.createElement("div")
        churnViewContainer.id = "churnView"
        churnViewContainer.style.display = "none"
        analysisContent.insertBefore(churnViewContainer, analysisContent.firstChild)
      }
    }

    let churnActionsContainer = document.getElementById("churnActions")
    if (!churnActionsContainer) {
      const panelRight = document.querySelector(".panel-right")
      if (panelRight) {
        churnActionsContainer = document.createElement("div")
        churnActionsContainer.id = "churnActions"
        churnActionsContainer.style.display = "none"
        panelRight.insertBefore(churnActionsContainer, panelRight.firstChild)
      }
    }

    if (churnViewContainer) {
      churnViewContainer.style.display = "block"
      if (defaultViewContainer) defaultViewContainer.style.display = "none"
      if (qualityViewContainer) qualityViewContainer.style.display = "none"
      if (expansionViewContainer) expansionViewContainer.style.display = "none"
      if (qbrViewContainer) qbrViewContainer.style.display = "none"

      if (churnActionsContainer) {
        churnActionsContainer.style.display = "block"
      }
      if (qualityActionsContainer) qualityActionsContainer.style.display = "none"
      if (expansionActionsContainer) expansionActionsContainer.style.display = "none"
      if (qbrActionsContainer) qbrActionsContainer.style.display = "none"
      if (defaultActionsContainer) defaultActionsContainer.style.display = "none"

      renderChurnView(detailedData, churnViewContainer)
      renderChurnActions(churnActionsContainer, detailedData, alertData)
    }
  } else if (useCase === "supply_risk" || useCase === "supply") {
    console.log("[v0] Rendering Supply view")

    if (!detailedData || !detailedData.risk_summary) {
      console.warn("[v0] No supply data available, showing default view")
      if (defaultViewContainer) {
        defaultViewContainer.innerHTML =
          '<div style="padding: 2rem; text-align: center; color: #94a3b8;">No supply risk data available for this account</div>'
        defaultViewContainer.style.display = "block"
      }
      if (defaultActionsContainer) {
        defaultActionsContainer.innerHTML =
          '<div style="padding: 1rem; text-align: center; color: #94a3b8;">No actions available</div>'
        defaultActionsContainer.style.display = "block"
      }
      return
    }

    let supplyViewContainer = document.getElementById("supplyView")
    if (!supplyViewContainer) {
      const analysisContent = document.getElementById("analysisContent")
      if (analysisContent) {
        supplyViewContainer = document.createElement("div")
        supplyViewContainer.id = "supplyView"
        supplyViewContainer.style.display = "none"
        analysisContent.insertBefore(supplyViewContainer, analysisContent.firstChild)
      }
    }

    let supplyActionsContainer = document.getElementById("supplyActions")
    if (!supplyActionsContainer) {
      const panelRight = document.querySelector(".panel-right")
      if (panelRight) {
        supplyActionsContainer = document.createElement("div")
        supplyActionsContainer.id = "supplyActions"
        supplyActionsContainer.style.display = "none"
        panelRight.insertBefore(supplyActionsContainer, panelRight.firstChild)
      }
    }

    if (supplyViewContainer) {
      supplyViewContainer.style.display = "block"
      if (defaultViewContainer) defaultViewContainer.style.display = "none"
      if (qualityViewContainer) qualityViewContainer.style.display = "none"
      if (expansionViewContainer) expansionViewContainer.style.display = "none"
      if (qbrViewContainer) qbrViewContainer.style.display = "none"
      if (churnViewContainer) churnViewContainer.style.display = "none"

      if (supplyActionsContainer) {
        supplyActionsContainer.style.display = "block"
        if (defaultActionsContainer) defaultActionsContainer.style.display = "none"
        if (qualityActionsContainer) qualityActionsContainer.style.display = "none"
        if (expansionActionsContainer) expansionActionsContainer.style.display = "none"
        if (qbrActionsContainer) qbrActionsContainer.style.display = "none"
        if (churnActionsContainer) churnActionsContainer.style.display = "none"
      }

      renderSupplyView(detailedData, supplyViewContainer)
      renderSupplyActions(supplyActionsContainer, detailedData, alertData)
    }
  } else if (alertData.analysis) {
    console.log("[v0] Rendering default analysis view")
    renderAnalysis(alertData.analysis)
    renderActions(alertData.actions)
  } else {
    console.log("[v0] No detailed data available, showing default empty view.")
    clearAnalysisPanels() // Ensure panels are reset if no data at all
  }
}

function renderAnalysis(analysis) {
  // Cancel any existing animation
  if (state.typingAnimationId) {
    clearTimeout(state.typingAnimationId)
    state.typingAnimationId = null
  }
  if (state.typingTimeoutId) {
    clearTimeout(state.typingTimeoutId)
    state.typingTimeoutId = null
  }

  // Reset sections with proper transitions
  elements.summaryText.innerHTML = ""
  elements.patternsSection.style.opacity = "0"
  elements.patternsSection.style.transform = "translateY(10px)"
  elements.scenariosSection.style.opacity = "0"
  elements.scenariosSection.style.transform = "translateY(10px)"
  elements.patternsGrid.innerHTML = ""
  elements.scenariosList.innerHTML = ""

  // Add transition styles
  elements.patternsSection.style.transition = "opacity 0.4s ease, transform 0.4s ease"
  elements.scenariosSection.style.transition = "opacity 0.4s ease, transform 0.4s ease"

  // Store current alert ID to prevent stale callbacks
  const currentAlertId = state.selectedAlert?.id

  // Type summary with controlled animation
  typeText(analysis.summary, elements.summaryText, 12, () => {
    // Verify we're still on the same alert
    if (state.selectedAlert?.id !== currentAlertId) return

    // Show patterns after summary
    state.typingAnimationId = setTimeout(() => {
      if (state.selectedAlert?.id !== currentAlertId) return

      elements.patternsSection.style.opacity = "1"
      elements.patternsSection.style.transform = "translateY(0)"
      renderPatterns(analysis.patterns)

      // Show scenarios after patterns
      state.typingAnimationId = setTimeout(() => {
        if (state.selectedAlert?.id !== currentAlertId) return

        elements.scenariosSection.style.opacity = "1"
        elements.scenariosSection.style.transform = "translateY(0)"
        renderScenarios(analysis.scenarios)
      }, 400)
    }, 250)
  })
}

function renderQualityIncidentView(data, container) {
  console.log("[v0] renderQualityIncidentView called")
  container.innerHTML = `
    <div class="quality-incident-view">
      <!-- Executive Summary -->
      <div class="qi-section">
        <h3 class="qi-section-title">
          <span class="qi-icon">🔥</span>
          Executive Summary
        </h3>
        <p class="qi-summary-text">${data.brief.executive_summary}</p>
      </div>

      <!-- Key Findings -->
      <div class="qi-section">
        <h3 class="qi-section-title">
          <span class="qi-icon">📌</span>
          Key Findings
        </h3>
        <ul class="qi-findings-list">
          ${data.brief.key_findings
            .map(
              (finding) => `
            <li class="qi-finding-item">${finding}</li>
          `,
            )
            .join("")}
        </ul>
      </div>

      <!-- Root Cause Summary -->
      <div class="qi-section">
        <h3 class="qi-section-title">
          <span class="qi-icon">🧠</span>
          Root Cause Summary
        </h3>
        <div class="qi-defects-grid">
          ${data.rca.root_cause_summary
            .map(
              (defect) => `
            <div class="qi-defect-card">
              <div class="qi-defect-header">
                <span class="qi-defect-code">${defect.defect_code}</span>
                <span class="qi-defect-severity qi-severity-${defect.severity.toLowerCase()}">${defect.severity}</span>
              </div>
              <div class="qi-defect-count">${defect.count} incidents</div>
            </div>
          `,
            )
            .join("")}
        </div>
        <div class="qi-total-incidents">
          <strong>Total Incidents:</strong> ${data.rca.total_incidents}
        </div>
      </div>

      <!-- Incident Trend Chart -->
      <div class="qi-section">
        <h3 class="qi-section-title">
          <span class="qi-icon">📊</span>
          Incident Trend
        </h3>
        <div class="qi-chart-container">
          <canvas id="incidentTrendChart"></canvas>
        </div>
      </div>

      <!-- Correlated Factors -->
      <div class="qi-section">
        <h3 class="qi-section-title">
          <span class="qi-icon">🧩</span>
          Correlated Factors
        </h3>
        <div class="qi-factors-grid">
          ${Object.entries(data.rca.correlated_factors)
            .map(
              ([key, values]) => `
            <div class="qi-factor-group">
              <h4 class="qi-factor-title">${key.replace("_", " ").replace(/\b\w/g, (l) => l.toUpperCase())}</h4>
              <div class="qi-factor-items">
                ${values
                  .map(
                    (item) => `
                  <span class="qi-factor-badge">
                    ${item.value} <span class="qi-factor-count">(${item.count})</span>
                  </span>
                `,
                  )
                  .join("")}
              </div>
            </div>
          `,
            )
            .join("")}
        </div>
      </div>

      <!-- Action Plan -->
      <div class="qi-section">
        <h3 class="qi-section-title">
          <span class="qi-icon">🛠️</span>
          Action Plan
        </h3>
        <ol class="qi-action-list">
          ${data.brief.action_plan
            .map(
              (action) => `
            <li class="qi-action-item">${action}</li>
          `,
            )
            .join("")}
        </ol>
      </div>
    </div>
  `

  // Render the chart after DOM update
  setTimeout(() => renderIncidentTrendChart(data.rca.trends.daily_counts), 100)
}

function renderIncidentTrendChart(dailyCounts) {
  const canvas = document.getElementById("incidentTrendChart")
  if (!canvas) return

  const ctx = canvas.getContext("2d")

  // Destroy existing chart if any
  if (window.incidentChart) {
    window.incidentChart.destroy()
  }

  // Prepare data
  const dates = dailyCounts.map((d) => {
    const date = new Date(d.date)
    return date.toLocaleDateString("en-US", { month: "short", day: "numeric" })
  })
  const counts = dailyCounts.map((d) => d.count)

  // Create gradient
  const gradient = ctx.createLinearGradient(0, 0, 0, 300)
  gradient.addColorStop(0, "rgba(239, 68, 68, 0.3)")
  gradient.addColorStop(1, "rgba(239, 68, 68, 0.05)")

  // Get dimensions after potential resize or render delay
  const chartAreaWidth = canvas.offsetWidth - 80 // Account for padding on both sides
  const chartAreaHeight = 250 - 80 // Account for padding on top and bottom

  canvas.width = canvas.offsetWidth
  canvas.height = 250

  const padding = 40
  const chartWidth = canvas.width - padding * 2
  const chartHeight = canvas.height - padding * 2
  const maxCount = Math.max(...counts, 1) // Ensure maxCount is at least 1 to avoid division by zero

  // Clear canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  // Draw axes
  ctx.strokeStyle = "#4b5563"
  ctx.lineWidth = 1
  ctx.beginPath()
  ctx.moveTo(padding, padding)
  ctx.lineTo(padding, canvas.height - padding) // Y-axis
  ctx.lineTo(canvas.width - padding, canvas.height - padding) // X-axis
  ctx.stroke()

  // Draw line chart
  const stepX = counts.length > 1 ? chartWidth / (counts.length - 1) : chartWidth // Calculate stepX, handle single data point case

  // Draw area fill
  ctx.fillStyle = gradient
  ctx.beginPath()
  if (counts.length > 0) {
    counts.forEach((count, i) => {
      const x = padding + i * stepX
      const y = canvas.height - padding - (count / maxCount) * chartHeight
      if (i === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    })
    // Close path by drawing line back to the start of the x-axis
    ctx.lineTo(padding + (counts.length - 1) * stepX, canvas.height - padding)
  }
  ctx.closePath()
  ctx.fill()

  // Draw line
  ctx.strokeStyle = "#ef4444"
  ctx.lineWidth = 2
  ctx.beginPath()
  if (counts.length > 0) {
    counts.forEach((count, i) => {
      const x = padding + i * stepX
      const y = canvas.height - padding - (count / maxCount) * chartHeight
      if (i === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    })
  }
  ctx.stroke()

  // Draw points
  if (counts.length > 0) {
    counts.forEach((count, i) => {
      const x = padding + i * stepX
      const y = canvas.height - padding - (count / maxCount) * chartHeight

      ctx.fillStyle = "#ef4444"
      ctx.beginPath()
      ctx.arc(x, y, 4, 0, Math.PI * 2)
      ctx.fill()

      ctx.strokeStyle = "#fff"
      ctx.lineWidth = 2
      ctx.stroke()
    })
  }

  // Draw labels
  ctx.fillStyle = "#9ca3af"
  ctx.font = "11px sans-serif"
  ctx.textAlign = "center"
  if (dates.length > 0) {
    dates.forEach((date, i) => {
      const x = padding + i * stepX
      ctx.fillText(date, x, canvas.height - padding + 20)
    })
  }

  // Draw count labels on Y-axis
  ctx.textAlign = "right"
  const yLabelCount = 4 // Number of labels on Y-axis
  for (let i = 0; i < yLabelCount; i++) {
    const value = Math.round((maxCount / (yLabelCount - 1)) * i)
    const y = canvas.height - padding - (i / (yLabelCount - 1)) * chartHeight
    if (i === yLabelCount - 1) {
      // Ensure the top label is maxCount if it's a round number
      ctx.fillText(maxCount.toString(), padding - 10, padding + 4)
    } else {
      ctx.fillText(value.toString(), padding - 10, y + 4)
    }
  }
}

function startTypingAnimation(alert) {
  // Cancel any existing animation
  if (state.typingAnimationId) {
    clearTimeout(state.typingAnimationId)
    state.typingAnimationId = null
  }
  if (state.typingTimeoutId) {
    clearTimeout(state.typingTimeoutId)
    state.typingTimeoutId = null
  }

  // Reset sections with proper transitions
  elements.summaryText.innerHTML = ""
  elements.patternsSection.style.opacity = "0"
  elements.patternsSection.style.transform = "translateY(10px)"
  elements.scenariosSection.style.opacity = "0"
  elements.scenariosSection.style.transform = "translateY(10px)"
  elements.patternsGrid.innerHTML = ""
  elements.scenariosList.innerHTML = ""

  // Add transition styles
  elements.patternsSection.style.transition = "opacity 0.4s ease, transform 0.4s ease"
  elements.scenariosSection.style.transition = "opacity 0.4s ease, transform 0.4s ease"

  // Store current alert ID to prevent stale callbacks
  const currentAlertId = alert.id

  // Type summary with controlled animation
  typeText(alert.analysis.summary, elements.summaryText, 12, () => {
    // Verify we're still on the same alert
    if (state.selectedAlert?.id !== currentAlertId) return

    // Show patterns after summary
    state.typingAnimationId = setTimeout(() => {
      if (state.selectedAlert?.id !== currentAlertId) return

      elements.patternsSection.style.opacity = "1"
      elements.patternsSection.style.transform = "translateY(0)"
      renderPatterns(alert.analysis.patterns)

      // Show scenarios after patterns
      state.typingAnimationId = setTimeout(() => {
        if (state.selectedAlert?.id !== currentAlertId) return

        elements.scenariosSection.style.opacity = "1"
        elements.scenariosSection.style.transform = "translateY(0)"
        renderScenarios(alert.analysis.scenarios)
      }, 400)
    }, 250)
  })
}

let currentTypingId = 0 // Initialize currentTypingId

function typeText(text, element, speed, callback) {
  currentTypingId++
  const thisTypingId = currentTypingId
  let i = 0

  // Clear any previous content and add cursor
  element.innerHTML = '<span class="typing-cursor"></span>'

  function type() {
    // Check if this animation is still current
    if (thisTypingId !== currentTypingId) return

    if (i < text.length) {
      const displayText = text.slice(0, i + 1)
      element.innerHTML = displayText + '<span class="typing-cursor"></span>'
      i++
      state.typingTimeoutId = setTimeout(type, speed)
    } else {
      // Animation complete - remove cursor
      element.textContent = text
      if (callback) callback()
    }
  }

  // Start animation after a brief delay
  state.typingTimeoutId = setTimeout(type, 50)
}

function renderPatterns(patterns) {
  elements.patternsGrid.innerHTML = patterns
    .map(
      (pattern) => `
    <div class="pattern-item">
      <div class="pattern-icon">${pattern.icon}</div>
      <div class="pattern-text">
        <div class="pattern-label">${pattern.label}</div>
        <div class="pattern-value">${pattern.value}</div>
      </div>
    </div>
  `,
    )
    .join("")
}

function renderScenarios(scenarios) {
  elements.scenariosList.innerHTML = scenarios
    .map(
      (scenario, index) => `
    <div class="scenario-item">
      <span class="scenario-number">${index + 1}</span>
      <div class="scenario-content">
        <div class="scenario-title">${scenario.title}</div>
        <div class="scenario-impact">${scenario.impact}</div>
      </div>
    </div>
  `,
    )
    .join("")
}

// ========================================
// Actions Rendering
// ========================================

function renderActions(actions) {
  elements.actionsList.innerHTML = actions
    .map(
      (action, index) => `
    <div class="action-card ${state.approvedActions.has(index) ? "approved" : ""} ${state.editedActions.has(index) ? "edited" : ""}" data-index="${index}">
      <div class="action-header">
        <div class="action-icon ${action.type}">${getActionIcon(action.type)}</div>
        <div>
          <div class="action-title">${state.editedActions.get(index)?.title || action.title}</div>
          <div class="action-description">${state.editedActions.get(index)?.description || action.description}</div>
        </div>
      </div>
      <div class="action-meta">
        <div class="meta-item">
          <span class="meta-label">Due</span>
          <span class="meta-value">${state.editedActions.get(index)?.due || action.due}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Owner</span>
          <span class="meta-value">${state.editedActions.get(index)?.owner || action.owner}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Impact</span>
          <span class="meta-value impact">${state.editedActions.get(index)?.impact || action.impact}</span>
        </div>
      </div>
      <div class="action-buttons">
        ${
          state.approvedActions.has(index)
            ? `
          <button class="btn btn-sm btn-approved">✓ Approved</button>
          <button class="btn btn-sm btn-ghost action-send" data-index="${index}">Send Now</button>
        `
            : `
          <button class="btn btn-sm btn-success action-approve" data-index="${index}">Approve</button>
          <button class="btn btn-sm btn-secondary action-edit" data-index="${index}">Edit</button>
          <button class="btn btn-sm btn-ghost action-send" data-index="${index}">Send</button>
        `
        }
      </div>
    </div>
  `,
    )
    .join("")

  // Add event listeners
  document.querySelectorAll(".action-approve").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation()
      const index = Number.parseInt(btn.dataset.index)
      approveAction(index)
    })
  })

  document.querySelectorAll(".action-edit").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation()
      const index = Number.parseInt(btn.dataset.index)
      openEditModal(index)
    })
  })

  document.querySelectorAll(".action-send").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation()
      const index = Number.parseInt(btn.dataset.index)
      sendAction(index)
    })
  })
}

function getActionIcon(type) {
  switch (type) {
    case "crm":
      return "📊"
    case "email":
      return "✉️"
    case "recovery":
      return "🔄"
    default:
      return "📋"
  }
}

function approveAction(index) {
  state.approvedActions.add(index)
  if (state.selectedAlert) {
    renderActions(state.selectedAlert.actions)
  }
  showToast("success", "Action Approved", "The action has been queued for execution")
}

function sendAction(index) {
  state.approvedActions.add(index)
  if (state.selectedAlert) {
    renderActions(state.selectedAlert.actions)
  }
  showToast("success", "Action Sent", "The action has been executed immediately")
}

function approveAllActions() {
  if (state.selectedAlert) {
    state.selectedAlert.actions.forEach((_, index) => {
      state.approvedActions.add(index)
    })
    renderActions(state.selectedAlert.actions)
    showToast("success", "All Actions Approved", `${state.selectedAlert.actions.length} actions have been queued`)
  }
}

// ========================================
// Edit Action Modal
// ========================================

function openEditModal(index) {
  if (!state.selectedAlert) return

  state.editingActionIndex = index
  const action = state.selectedAlert.actions[index]
  const editedAction = state.editedActions.get(index) || action

  // Create edit modal if it doesn't exist
  let editModal = document.getElementById("editActionModal")
  if (!editModal) {
    createEditModal()
    editModal = document.getElementById("editActionModal")
  }

  // Populate form fields
  document.getElementById("editActionTitle").value = editedAction.title
  document.getElementById("editActionDescription").value = editedAction.description
  document.getElementById("editActionDue").value = editedAction.due
  document.getElementById("editActionOwner").value = editedAction.owner
  document.getElementById("editActionImpact").value = editedAction.impact

  // Show modal
  document.getElementById("editModalOverlay").classList.add("active")
}

function createEditModal() {
  const modalHTML = `
    <div class="modal-overlay" id="editModalOverlay">
      <div class="modal edit-modal" id="editActionModal">
        <div class="modal-header">
          <h2>Edit Action</h2>
          <button class="modal-close" id="editModalClose">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <div class="modal-body">
          <div class="form-group">
            <label for="editActionTitle">Action Title</label>
            <input type="text" id="editActionTitle" placeholder="Enter action title">
          </div>
          <div class="form-group">
            <label for="editActionDescription">Description</label>
            <textarea id="editActionDescription" placeholder="Describe the action..." rows="3"></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="editActionDue">Due Date</label>
              <select id="editActionDue">
                <option value="Immediate">Immediate</option>
                <option value="Today">Today</option>
                <option value="Tomorrow">Tomorrow</option>
                <option value="This week">This week</option>
                <option value="Next week">Next week</option>
              </select>
            </div>
            <div class="form-group">
              <label for="editActionOwner">Owner</label>
              <input type="text" id="editActionOwner" placeholder="Assign owner">
            </div>
          </div>
          <div class="form-group">
            <label for="editActionImpact">Impact Level</label>
            <select id="editActionImpact">
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
              <option value="Critical">Critical</option>
            </select>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn btn-ghost" id="editModalCancel">Cancel</button>
          <button class="btn btn-primary" id="editModalSave">Save Changes</button>
        </div>
      </div>
    </div>
  `

  document.body.insertAdjacentHTML("beforeend", modalHTML)

  // Add event listeners
  document.getElementById("editModalClose").addEventListener("click", closeEditModal)
  document.getElementById("editModalCancel").addEventListener("click", closeEditModal)
  document.getElementById("editModalSave").addEventListener("click", saveEditedAction)
  document.getElementById("editModalOverlay").addEventListener("click", (e) => {
    if (e.target.id === "editModalOverlay") closeEditModal()
  })
}

function closeEditModal() {
  document.getElementById("editModalOverlay").classList.remove("active")
  state.editingActionIndex = null
}

function saveEditedAction() {
  if (state.editingActionIndex === null || !state.selectedAlert) return

  const editedData = {
    title: document.getElementById("editActionTitle").value,
    description: document.getElementById("editActionDescription").value,
    due: document.getElementById("editActionDue").value,
    owner: document.getElementById("editActionOwner").value,
    impact: document.getElementById("editActionImpact").value,
  }

  state.editedActions.set(state.editingActionIndex, editedData)

  // Re-render actions
  renderActions(state.selectedAlert.actions)

  // Close modal and show toast
  closeEditModal()
  showToast("success", "Action Updated", "Your changes have been saved")
}

// ========================================
// Theme Toggle
// ========================================

function toggleTheme() {
  state.theme = state.theme === "dark" ? "light" : "dark"
  document.documentElement.setAttribute("data-theme", state.theme)
}

// ========================================
// Modal Management
// ========================================

function openModal() {
  state.modalStep = 1
  updateModalStep()
  elements.modalOverlay.classList.add("active")
}

function closeModal() {
  elements.modalOverlay.classList.remove("active")
  state.modalStep = 1
  updateModalStep()
}

function nextModalStep() {
  if (state.modalStep < 4) {
    state.modalStep++
    updateModalStep()
  } else {
    createAgent()
  }
}

function prevModalStep() {
  if (state.modalStep > 1) {
    state.modalStep--
    updateModalStep()
  }
}

function updateModalStep() {
  // Update step indicators
  document.querySelectorAll(".progress-step").forEach((step) => {
    const stepNum = Number.parseInt(step.dataset.step)
    step.classList.remove("active", "completed")
    if (stepNum === state.modalStep) {
      step.classList.add("active")
    } else if (stepNum < state.modalStep) {
      step.classList.add("completed")
    }
  })

  // Update step content
  document.querySelectorAll(".modal-step").forEach((step) => {
    step.classList.toggle("active", Number.parseInt(step.dataset.step) === state.modalStep)
  })

  // Update buttons
  elements.modalBack.style.display = state.modalStep > 1 ? "block" : "none"
  elements.modalNext.textContent = state.modalStep === 4 ? "Create Agent" : "Next"

  // Update preview if on last step
  if (state.modalStep === 4) {
    updatePreview()
  }
}

function updatePreview() {
  const name = document.getElementById("agentNameInput")?.value || "New Agent"
  const type = document.getElementById("agentTypeSelect")?.value || "churn"
  const threshold = document.getElementById("thresholdInput")?.value || "70"
  const triggers = document.querySelectorAll(".checkbox-group input:checked").length
  const sources = document.querySelectorAll(".data-source.active").length

  const typeLabels = {
    expansion: "Expansion",
    churn: "Churn Prevention",
    quality: "Quality Incidents", // Updated label for Quality Incidents
    qbr: "QBR Auto-Generation", // Added label for QBR
    supply: "Supply Chain", // Added label for Supply Chain
  }

  document.getElementById("previewName").textContent = name || "New Agent"
  document.getElementById("previewType").textContent = typeLabels[type]
  document.getElementById("previewTriggers").textContent = triggers
  document.getElementById("previewSources").textContent = sources
  document.getElementById("previewThreshold").textContent = threshold
}

function createAgent() {
  const name = document.getElementById("agentNameInput")?.value || "New Custom Agent"
  const type = document.getElementById("agentTypeSelect")?.value || state.currentUseCase

  // Create new alert
  const newAlert = {
    id: `custom-${Date.now()}`,
    company: name,
    type: "Custom Agent Alert",
    severity: "medium",
    score: 75,
    metrics: { status: "Active", triggers: "3" },
    timestamp: "Just now",
    analysis: {
      summary: `${name} has been activated and is now monitoring your selected data sources. Initial analysis is in progress, and actionable insights will appear here as patterns are detected.`,
      patterns: [
        { icon: "🚀", label: "Status", value: "Active and monitoring" },
        {
          icon: "📊",
          label: "Data Sources",
          value: `${document.querySelectorAll(".data-source.active").length} connected`,
        },
        {
          icon: "🎯",
          label: "Triggers",
          value: `${document.querySelectorAll(".checkbox-group input:checked").length} configured`,
        },
        { icon: "⏱️", label: "Next Analysis", value: "In 5 minutes" },
      ],
      scenarios: [
        { title: "Monitoring Active", impact: "Real-time insights enabled" },
        { title: "Pattern Detection", impact: "Learning from data" },
        { title: "Alert Configuration", impact: "Thresholds set" },
      ],
    },
    actions: [
      {
        type: "crm",
        title: "Review Agent Settings",
        description: "Verify configuration matches requirements",
        due: "Today",
        owner: "You",
        impact: "Medium",
      },
      {
        type: "email",
        title: "Setup Notifications",
        description: "Configure alert delivery preferences",
        due: "Today",
        owner: "You",
        impact: "Low",
      },
    ],
  }

  // Add to current use case
  alertsData[type].unshift(newAlert)

  // Switch to that use case if different
  if (type !== state.currentUseCase) {
    switchUseCase(type)
  } else {
    renderAlerts()
  }

  // Select the new alert
  selectAlert(newAlert)

  // Close modal
  closeModal()

  // Show success toast
  showToast("success", "Agent Created", `${name} is now active and monitoring`)
}

// ========================================
// Toast Notifications
// ========================================

function showToast(type, title, message) {
  const toast = document.createElement("div")
  toast.className = `toast ${type}`

  const icons = {
    success: "✓",
    error: "✕",
    info: "ℹ",
    warning: "⚠",
  }

  toast.innerHTML = `
    <span class="toast-icon">${icons[type]}</span>
    <div class="toast-content">
      <div class="toast-title">${title}</div>
      <div class="toast-message">${message}</div>
    </div>
  `

  elements.toastContainer.appendChild(toast)

  // Remove after animation
  setTimeout(() => {
    toast.remove()
  }, 3000)
}

// ========================================
// Quality Incident Action Rendering
// ========================================

function renderQualityIncidentActions(data, container) {
  console.log("[v0] renderQualityIncidentActions called")
  console.log("[v0] Container:", container)
  console.log("[v0] Container ID:", container?.id)

  const panelRight = document.querySelector(".panel-right")
  const scrollContainer = document.querySelector(".actions-scroll-container")

  console.log("[v0] Panel Right:", panelRight)
  console.log("[v0] Scroll Container:", scrollContainer)

  if (panelRight) {
    const styles = window.getComputedStyle(panelRight)
    console.log("[v0] Panel Right computed styles:", {
      height: styles.height,
      overflow: styles.overflow,
      display: styles.display,
      flexDirection: styles.flexDirection,
    })
  }

  if (scrollContainer) {
    const styles = window.getComputedStyle(scrollContainer)
    console.log("[v0] Scroll Container computed styles:", {
      height: styles.height,
      maxHeight: styles.maxHeight,
      overflowY: styles.overflowY,
      flex: styles.flex,
      minHeight: styles.minHeight,
    })
  }

  // After rendering, check content height
  setTimeout(() => {
    if (container) {
      console.log("[v0] Container scroll height:", container.scrollHeight)
      console.log("[v0] Container client height:", container.clientHeight)
      console.log("[v0] Container offsetHeight:", container.offsetHeight)
      console.log("[v0] Should scroll:", container.scrollHeight > container.clientHeight)
    }
    if (scrollContainer) {
      console.log("[v0] Scroll Container scroll height:", scrollContainer.scrollHeight)
      console.log("[v0] Scroll Container client height:", scrollContainer.clientHeight)
      console.log("[v0] Scroll Container should scroll:", scrollContainer.scrollHeight > scrollContainer.clientHeight)
    }
  }, 100)

  if (!container) {
    console.log("[v0] ERROR: container not provided for renderQualityIncidentActions!")
    return
  }

  const email = data.email || {}
  const brief = data.brief || {}
  const actions = data.actions || []

  console.log(
    "[v0] About to render - email:",
    !!email.to,
    "brief:",
    !!brief.executive_summary,
    "actions:",
    actions.length,
  )

  let html = '<div class="qi-actions-container">'

  // Action 1: Send Apology Email
  if (email.to || email.subject || email.body) {
    html += `
      <div class="qi-action-card">
        <div class="qi-action-header">
          <!-- Removed action badge -->
          <h3 class="qi-action-title">Send Apology Email</h3>
        </div>
        <div class="qi-email-editor">
          <div class="qi-email-field">
            <label>To:</label>
            <input type="text" class="qi-email-input" value="${email.to || ""}" data-field="to" />
          </div>
          <div class="qi-email-field">
            <label>Subject:</label>
            <input type="text" class="qi-email-input" value="${email.subject || ""}" data-field="subject" />
          </div>
          <div class="qi-email-field">
            <label>Body:</label>
            <textarea class="qi-email-textarea" rows="8" data-field="body">${email.body || ""}</textarea>
          </div>
        </div>
        <div class="qi-action-buttons">
          <button class="qi-btn qi-btn-secondary" onclick="editEmailAction(this)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            Edit
          </button>
          <button class="qi-btn qi-btn-primary" onclick="sendEmail(this)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
            Send
          </button>
          <button class="qi-btn qi-btn-ghost" onclick="saveDraft(this)">Save Draft</button>
        </div>
      </div>
    `
  }

  // Action 2: Download Quality Brief
  if (brief.executive_summary || brief.key_findings) {
    html += `
      <div class="qi-action-card">
        <div class="qi-action-header">
          <!-- Removed action badge -->
          <h3 class="qi-action-title">Download Quality Brief</h3>
        </div>
        <div class="qi-brief-preview">
          <p class="qi-brief-description">Complete quality incident analysis with executive summary, key findings, and action plan.</p>
          <div class="qi-brief-stats">
            <div class="qi-stat-item">
              <span class="qi-stat-label">Sections</span>
              <span class="qi-stat-value">5</span>
            </div>
            <div class="qi-stat-item">
              <span class="qi-stat-label">Format</span>
              <span class="qi-stat-value">PDF</span>
            </div>
          </div>
        </div>
        <div class="qi-action-buttons">
          <button class="qi-btn qi-btn-primary" onclick="downloadBrief(this)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            Download Brief
          </button>
        </div>
      </div>
    `
  }

  // Action 3: Create Ops Tasks
  if (actions) {
    html += `
      <div class="qi-action-card">
        <div class="qi-action-header">
          <!-- Removed action badge -->
          <h3 class="qi-action-title">Create Ops Tasks</h3>
        </div>
        <div class="qi-tasks-list">
    `

    if (actions.length > 0) {
      actions.forEach((action, index) => {
        html += `
          <div class="qi-task-item" data-task-index="${index}">
            <div class="qi-task-header">
              <span class="qi-task-number">${index + 1}</span>
              <input type="text" class="qi-task-title-input" value="${action.title || ""}" />
            </div>
            <textarea class="qi-task-description" rows="2" placeholder="Add task description...">${action.description || ""}</textarea>
          </div>
        `
      })
    } else {
      html += `
        <div class="qi-empty-tasks">
          <p>No tasks yet. Click "Create Task" to add new operational tasks.</p>
          <!-- Added button to create new task -->
          <button class="qi-btn qi-btn-secondary" onclick="addNewTask(this)" style="margin-top: 12px;">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            Create Task
          </button>
        </div>
      `
    }

    html += `
        </div>
        <div class="qi-action-buttons">
          <button class="qi-btn qi-btn-secondary" onclick="editTasks(this)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            Edit
          </button>
          <button class="qi-btn qi-btn-primary" onclick="createTasks(this)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
            Approve & Create
          </button>
        </div>
      </div>
    `
  }

  html += "</div>"
  container.innerHTML = html
}

// Action handlers
function editEmailAction(button) {
  const card = button.closest(".qi-action-card")
  const inputs = card.querySelectorAll("input, textarea")
  inputs.forEach((input) => {
    input.disabled = false
    input.classList.add("editing")
  })
  button.textContent = "Done Editing"
  button.onclick = () => {
    inputs.forEach((input) => {
      input.disabled = true
      input.classList.remove("editing")
    })
    button.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg> Edit`
    button.onclick = () => editEmailAction(button)
  }
}

function sendEmail(button) {
  const card = button.closest(".qi-action-card")
  const emailData = {
    to: card.querySelector('[data-field="to"]').value,
    subject: card.querySelector('[data-field="subject"]').value,
    body: card.querySelector('[data-field="body"]').value,
    account_id: state.selectedAlert?.id,
    agent_run_id: state.selectedAlert?.agentRunId,
  }

  console.log("[v0] Sending email:", emailData)

  // TODO: Make POST API call to send email
  fetch(`${API_CONFIG.baseUrl}/agent/action/send-email`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(emailData),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("[v0] Email sent successfully:", data)
      // alert("Email sent successfully!")
      showToast("success", "Email Sent", "Email sent successfully:")
    })
    .catch((error) => {
      console.error("[v0] Error sending email:", error)
      alert("Failed to send email. Check console for details.")
    })
  showToast("success", "Email Sent", `Retention email sent to ${emailData.to}`)
}

function saveDraft(button) {
  const card = button.closest(".qi-action-card")
  const emailData = {
    to: card.querySelector('[data-field="to"]').value,
    subject: card.querySelector('[data-field="subject"]').value,
    body: card.querySelector('[data-field="body"]').value,
  }
  console.log("[v0] Saving draft:", emailData)
  alert("Draft saved!")
}

function downloadBrief(button) {
  const alertData = state.selectedAlert
  const briefContent = state.selectedAlert?.detailedData?.brief

  console.log("[v0] Downloading brief for:", alertData)

  fetch(`${API_CONFIG.baseUrl}/agent/action/download-brief`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      account_id: alertData?.id,
      agent_run_id: alertData?.agentRunId,
      brief: briefContent,
      company_name: alertData?.company,
    }),
  })
    .then((response) => response.blob())
    .then((blob) => {
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `quality-brief-${alertData?.company}.pdf`
      a.click()
    })
    .catch((error) => {
      console.error("[v0] Error downloading brief:", error)
      alert("Failed to download brief. Check console for details.")
    })
}

function editTasks(button) {
  const card = button.closest(".qi-action-card")
  // Implementation for editing tasks would go here
  console.log("[v0] Editing tasks...")
}

function addNewTask(button) {
  const card = button.closest(".qi-action-card")
  const tasksList = card.querySelector(".qi-tasks-list")

  // Remove empty state if exists
  const emptyState = card.querySelector(".qi-empty-tasks")
  if (emptyState) {
    emptyState.remove()
  }

  // Get current task count
  const taskCount = card.querySelectorAll(".qi-task-item").length

  // Create new task HTML
  const newTaskHTML = `
    <div class="qi-task-item" data-task-index="${taskCount}">
      <div class="qi-task-header">
        <span class="qi-task-number">${taskCount + 1}</span>
        <input type="text" class="qi-task-title-input" placeholder="Enter task title..." />
      </div>
      <textarea class="qi-task-description" rows="2" placeholder="Add task description..."></textarea>
    </div>
  `

  tasksList.insertAdjacentHTML("beforeend", newTaskHTML)
  console.log("[v0] New task added")
}

function createTasks(button) {
  const card = button.closest(".qi-action-card")
  const taskItems = card.querySelectorAll(".qi-task-item")
  const tasks = Array.from(taskItems).map((item) => ({
    title: item.querySelector(".qi-task-title-input").value,
    description: item.querySelector(".qi-task-description").value,
  }))

  const taskData = {
    tasks,
    account_id: state.selectedAlert?.id,
    agent_run_id: state.selectedAlert?.agentRunId,
  }

  console.log("[v0] Creating tasks:", taskData)

  // TODO: Make POST API call to create tasks
  fetch(`${API_CONFIG.baseUrl}/agent/action/create-tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(taskData),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("[v0] Tasks created successfully:", data)
      showToast("success", "Task Logged", "Tasks created successfully")
      // alert("Tasks created successfully!")
    })
    .catch((error) => {
      console.error("[v0] Error creating tasks:", error)
      alert("Failed to create tasks. Check console for details.")
    })
}

function renderExpansionOpportunityView(middlePanel, container) {
  const {
    primary_signal,
    competitor_risk,
    estimated_upside,
    signal_confidence,
    executive_summary,
    detected_signals,
    commercial_intelligence,
    revenue_opportunity,
  } = middlePanel

  const confidencePercent = (signal_confidence * 100).toFixed(0)
  const upsideFormatted = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(estimated_upside || 0)

  const html = `
    <div class="expansion-view">
      <!-- Executive Summary Card -->
      <div class="eo-section eo-executive-summary">
        <div class="eo-section-title">📌 Expansion Opportunity Summary</div>
        <div class="eo-summary-grid">
          <div class="eo-metric">
            <div class="eo-label">Primary Signal</div>
            <div class="eo-value">${primary_signal || "N/A"}</div>
          </div>
          <div class="eo-metric">
            <div class="eo-label">Competitor Risk</div>
            <div class="eo-value">${competitor_risk || "N/A"}</div>
          </div>
          <div class="eo-metric">
            <div class="eo-label">Estimated Upside</div>
            <div class="eo-value eo-upside">${upsideFormatted}</div>
          </div>
          <div class="eo-metric">
            <div class="eo-label">Signal Confidence</div>
            <div class="eo-confidence-bar">
              <div class="eo-confidence-fill" style="width: ${confidencePercent}%"></div>
              <span class="eo-confidence-text">${confidencePercent}%</span>
            </div>
          </div>
        </div>
        <div class="eo-summary-text">${executive_summary || ""}</div>
      </div>

      <!-- Detected Signals -->
      <div class="eo-section">
        <div class="eo-section-title">📊 Detected Operational Signals</div>
        
        ${
          detected_signals?.usage_anomalies?.length
            ? `
          <div class="eo-signals-subsection">
            <div class="eo-subsection-title">🔹 Usage Anomalies</div>
            ${detected_signals.usage_anomalies
              .map(
                (anomaly) => `
              <div class="eo-signal-item">
                <div class="eo-signal-sku">${anomaly.sku || "N/A"}</div>
                <div class="eo-signal-pattern">${anomaly.pattern || "N/A"}</div>
                <div class="eo-signal-confidence">
                  <span class="eo-conf-badge">${(anomaly.confidence * 100).toFixed(0)}%</span>
                </div>
              </div>
            `,
              )
              .join("")}
          </div>
        `
            : ""
        }

        ${
          detected_signals?.competitor_dependency?.length
            ? `
          <div class="eo-signals-subsection">
            <div class="eo-subsection-title">🔹 Competitor Dependency</div>
            ${detected_signals.competitor_dependency
              .map(
                (dep) => `
              <div class="eo-signal-item">
                <div class="eo-signal-label">Our SKU: <span>${dep.our_sku || "N/A"}</span></div>
                <div class="eo-signal-label">Their SKU: <span>${dep.their_sku || "N/A"}</span></div>
                <div class="eo-signal-label">Evidence: <span>${dep.evidence || "N/A"}</span></div>
              </div>
            `,
              )
              .join("")}
          </div>
        `
            : ""
        }

        ${
          detected_signals?.bom_gaps?.length
            ? `
          <div class="eo-signals-subsection">
            <div class="eo-subsection-title">🔹 BOM Gaps</div>
            ${detected_signals.bom_gaps
              .map(
                (gap) => `
              <div class="eo-signal-item">
                <div class="eo-signal-label">Missing SKU: <span>${gap.missing_sku || "N/A"}</span></div>
                <div class="eo-signal-label">Reason: <span>${gap.reason || "N/A"}</span></div>
                <div class="eo-signal-label">Linked SKU: <span>${gap.linked_sku || "N/A"}</span></div>
              </div>
            `,
              )
              .join("")}
          </div>
        `
            : ""
        }
      </div>

      <!-- Commercial Intelligence -->
      <div class="eo-section">
        <div class="eo-section-title">🧠 Commercial Insights</div>
        <div class="eo-commercial-card">
          <div class="eo-commercial-label">Executive Summary</div>
          <div class="eo-commercial-text">${commercial_intelligence?.brief_summary || ""}</div>
          
          ${
            commercial_intelligence?.commercial_insight?.length
              ? `
            <div class="eo-commercial-insights">
              ${commercial_intelligence.commercial_insight
                .map(
                  (insight) => `
                <div class="eo-insight-item">
                  <div class="eo-insight-pattern">${insight.pattern || ""}</div>
                  <div class="eo-insight-impact">${insight.impact || ""}</div>
                </div>
              `,
                )
                .join("")}
            </div>
          `
              : ""
          }
        </div>
      </div>

      <!-- Revenue Opportunity -->
      <div class="eo-section">
        <div class="eo-section-title">💰 Revenue Impact Model</div>
        <div class="eo-revenue-metrics">
          <div class="eo-revenue-card">
            <div class="eo-revenue-label">Monthly Revenue</div>
            <div class="eo-revenue-value">${new Intl.NumberFormat("en-US", {
              style: "currency",
              currency: revenue_opportunity?.currency || "USD",
              maximumFractionDigits: 0,
            }).format(revenue_opportunity?.estimated_monthly_revenue || 0)}</div>
          </div>
          <div class="eo-revenue-card">
            <div class="eo-revenue-label">Annual Revenue</div>
            <div class="eo-revenue-value">${new Intl.NumberFormat("en-US", {
              style: "currency",
              currency: revenue_opportunity?.currency || "USD",
              maximumFractionDigits: 0,
            }).format(revenue_opportunity?.estimated_annual_revenue || 0)}</div>
          </div>
        </div>
        ${
          revenue_opportunity?.assumptions?.length
            ? `
          <div class="eo-assumptions">
            <div class="eo-assumptions-title">Assumptions</div>
            <ul class="eo-assumptions-list">
              ${revenue_opportunity.assumptions.map((assumption) => `<li>${assumption}</li>`).join("")}
            </ul>
          </div>
        `
            : ""
        }
      </div>
    </div>
  `

  container.innerHTML = html
}

function renderExpansionActions(rightPanel, container) {
  console.log("[v0] renderExpansionActions called")
  console.log("[v0] Container:", container)
  console.log("[v0] Container ID:", container?.id)

  const panelRight = document.querySelector(".panel-right")
  const scrollContainer = document.querySelector(".actions-scroll-container")

  console.log("[v0] Panel Right:", panelRight)
  console.log("[v0] Scroll Container:", scrollContainer)

  if (panelRight) {
    const styles = window.getComputedStyle(panelRight)
    console.log("[v0] Panel Right computed styles:", {
      height: styles.height,
      overflow: styles.overflow,
      display: styles.display,
      flexDirection: styles.flexDirection,
    })
  }

  if (scrollContainer) {
    const styles = window.getComputedStyle(scrollContainer)
    console.log("[v0] Scroll Container computed styles:", {
      height: styles.height,
      maxHeight: styles.maxHeight,
      overflowY: styles.overflowY,
      flex: styles.flex,
      minHeight: styles.minHeight,
    })
  }

  // After rendering, check content height
  setTimeout(() => {
    if (container) {
      console.log("[v0] Container scroll height:", container.scrollHeight)
      console.log("[v0] Container client height:", container.clientHeight)
      console.log("[v0] Container offsetHeight:", container.offsetHeight)
      console.log("[v0] Should scroll:", container.scrollHeight > container.clientHeight)
    }
    if (scrollContainer) {
      console.log("[v0] Scroll Container scroll height:", scrollContainer.scrollHeight)
      console.log("[v0] Scroll Container client height:", scrollContainer.clientHeight)
      console.log("[v0] Scroll Container should scroll:", scrollContainer.scrollHeight > scrollContainer.clientHeight)
    }
  }, 100)

  const { actions = [], deck = {} } = rightPanel || {}

  // Check if there's actual data to display
  if (!actions || actions.length === 0) {
    container.innerHTML = '<div class="empty-state">No actions or deck available</div>'
    return
  }

  let html = '<div class="eo-actions-container">'

  // ========== ACTION 1: Log CRM Task ==========
  html += '<div class="eo-action-card">'
  html += '<div class="eo-action-header">'
  html += '<span class="eo-action-title">Log CRM Task</span>'
  html += "</div>"

  const typeLabels = {
    meeting: "📅 Schedule Review Meeting",
    task: "✅ Create Action Plan",
    email: "📧 Alert Supply Chain",
  }

  html += '<div class="eo-task-list">'
  actions.forEach((action) => {
    const priorityClass = `priority-${action.priority}`
    html += `
      <div class="eo-task-item ${priorityClass}">
        <div class="eo-task-priority">P${action.priority}</div>
        <div class="eo-task-content">
          <div class="eo-task-type">${typeLabels[action.type] || action.type || "Task"}</div>
          <div class="eo-task-rationale">${action.rationale || ""}</div>
        </div>
        <button class="eo-task-btn" onclick="logCRMTask('${action.type}', ${JSON.stringify(action).replace(/"/g, "&quot;")})">
          Log Task
        </button>
      </div>
    `
  })
  html += "</div>"
  html += "</div>"

  // ========== ACTION 2: Commercial Opportunity Deck ==========
  if (deck.slides && deck.slides.length > 0) {
    html += '<div class="eo-action-card">'
    html += '<div class="eo-action-header">'
    html += '<span class="eo-action-title">Commercial Opportunity Deck</span>'
    html += "</div>"
    html += '<div class="eo-deck-preview">'
    html += `<div class="eo-deck-title">${deck.deck_title || "Expansion Opportunity Analysis"}</div>`
    html += '<div class="eo-slides-list">'

    deck.slides.forEach((slide, index) => {
      html += `
        <div class="eo-slide-item">
          <span class="eo-slide-number">${index + 1}</span>
          <span class="eo-slide-title">${slide.slide_title || slide.title || "Slide " + (index + 1)}</span>
        </div>
      `
    })

    html += "</div>"
    html += '<div class="eo-deck-actions">'
    html += `<button class="eo-deck-btn" onclick="downloadExpansionDeck('${deck.deck_title}', ${JSON.stringify(deck).replace(/"/g, "&quot;")})">Download Deck</button>`
    html += "</div>"
    html += "</div>"
  }

  html += "</div>"
  container.innerHTML = html
}

function logCRMTask(actionType, actionData) {
  console.log("[v0] Logging CRM task:", actionType, actionData)

  const typeLabels = {
    meeting: "Schedule Review Meeting",
    task: "Create Action Plan",
    email: "Alert Supply Chain",
  }

  const payload = {
    account_id: state.selectedAlert?.id,
    agent_run_id: state.selectedAlert?.agentRunId,
    tasks: [
      {
        title: typeLabels[actionType] || actionData.type || "CRM Task",
        description: actionData.rationale || actionData.description || actionData.details || "",
      },
    ],
  }

  fetch(`${API_CONFIG.baseUrl}/agent/action/create-crm-task`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("[v0] CRM task logged successfully:", data)
      showToast("success", "CRM Task Logged", "Task details have been added to your CRM.")
    })
    .catch((error) => {
      console.error("[v0] Error logging CRM task:", error)
      showToast("error", "Failed to Log CRM Task", "Please check console for details.")
    })
}

function downloadExpansionDeck(deckTitle, deckData) {
  console.log("[v0] Downloading deck:", deckTitle)
  // POST to /agent/action/download-deck with deckData and accountId, agentRunId
  const payload = {
    ...deckData,
    deck_title: deckTitle,
    account_id: state.selectedAlert?.id,
    agent_run_id: state.selectedAlert?.agentRunId,
  }
  fetch(`${API_CONFIG.baseUrl}/agent/action/download-deck`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
    .then((response) => response.blob())
    .then((blob) => {
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `${deckTitle.replace(/\s+/g, "-")}.pptx` // Sanitize title for filename
      a.click()
      showToast("success", "Deck Downloaded", "Your commercial opportunity deck has been generated.")
    })
    .catch((error) => {
      console.error("[v0] Error downloading deck:", error)
      showToast("error", "Failed to Download Deck", "Please check console for details.")
    })
}

// RENDER QBR ACTIONS - START
function renderQBRActions(data, container) {
  console.log("[v0] renderQBRActions called with data:", data)
  console.log("[v0] Container:", container)

  const actions = data?.actions || []
  const deck = data?.deck || {}
  const talkingPoints = data?.talking_points || []

  console.log("[v0] Actions:", actions)
  console.log("[v0] Deck:", deck)
  console.log("[v0] Talking Points:", talkingPoints)

  let html = `<div class="qbr-actions-container">`

  if (actions.length > 0) {
    html += `
      <div class="eo-action-card">
        <div class="eo-action-header">
          <span class="eo-action-title">Log CRM Task</span>
        </div>
        <div class="eo-action-list">
          ${actions
            .map(
              (action) => `
            <div class="eo-action-item">
              <div class="eo-action-priority ${action.priority || "medium"}">
                <span class="eo-priority-badge">${action.priority?.toUpperCase() || "MEDIUM"}</span>
              </div>
              <div class="eo-action-content">
                <div class="eo-action-type">
                  <span class="eo-type-icon">${action.type === "meeting" ? "📅" : action.type === "email" ? "📧" : "✅"}</span>
                  <span class="eo-action-name">${action.title || action.type || "Task"}</span>
                </div>
                <div class="eo-action-description">${action.description || ""}</div>
              </div>
              <button class="eo-task-btn" onclick="logCRMTask('${action.type}', ${JSON.stringify(action).replace(/"/g, "&quot;")})">Log Task</button>
            </div>
          `,
            )
            .join("")}
        </div>
      </div>
    `
  }

  if (deck.slides && deck.slides.length > 0) {
    html += `
      <div class="eo-action-card">
        <div class="eo-action-header">
          <span class="eo-action-title">${deck.deck_title || "QBR Deck"}</span>
        </div>
        <div class="eo-deck-preview">
          <div class="eo-deck-title">${deck.subtitle || "QBR - " + (state.selectedAlert?.accountName || "Account")}</div>
          <div class="eo-slides-list">
            ${deck.slides
              .map(
                (slide, index) => `
              <div class="eo-slide-item">
                <span class="eo-slide-number">${index + 1}</span>
                <span class="eo-slide-title">${slide.slide_title || slide.title || "Slide " + (index + 1)}</span>
              </div>
            `,
              )
              .join("")}
          </div>
          <div class="eo-deck-actions">
            <button class="eo-deck-btn" onclick="downloadQBRDeck('${deck.deck_title}', ${JSON.stringify(deck).replace(/"/g, "&quot;")})">Download Deck</button>
          </div>
        </div>
      </div>
    `
  }

  if (talkingPoints.length > 0) {
    html += `
      <div class="eo-action-card">
        <div class="eo-action-header">
          <span class="eo-action-title">Talking Points</span>
        </div>
        <ul class="qbr-talking-points-list">
          ${talkingPoints.map((point) => `<li><span class="qbr-talking-point-icon">💡</span>${point}</li>`).join("")}
        </ul>
      </div>
    `
  }

  html += `</div>`

  console.log("[v0] Setting innerHTML for qbrActions container")
  container.innerHTML = html
  console.log("[v0] renderQBRActions complete")
}
// RENDER QBR ACTIONS - END

// ADDED FUNCTION: renderQBRView
function renderQBRView(data, container) {
  console.log("[v0] renderQBRView called with data:", data)
  console.log("[v0] renderQBRView container:", container)

  if (!container) {
    console.error("[v0] renderQBRView: container is null, cannot render QBR view")
    return
  }

  const trends = data?.trends || {}
  const rootCauses = data?.root_causes || []
  const brief = data?.brief || {}
  const opportunities = data?.opportunities || []
  const signals = data?.signals || {}

  const html = `
    <div class="qbr-view">
      <!-- RCA & Trends Section -->
      <div class="qbr-section">
        <h3 class="qbr-section-title">
          <span class="qbr-icon">📊</span>
          RCA & Trends
        </h3>
        <div class="qbr-metrics-grid">
          <div class="qbr-metric-card">
            <div class="qbr-metric-label">Orders</div>
            <div class="qbr-metric-value">${trends.orders || "N/A"}</div>
          </div>
          <div class="qbr-metric-card">
            <div class="qbr-metric-label">Usage</div>
            <div class="qbr-metric-value">${trends.usage || "N/A"}</div>
          </div>
          <div class="qbr-metric-card">
            <div class="qbr-metric-label">Quality</div>
            <div class="qbr-metric-value">${trends.quality || "N/A"}</div>
          </div>
          <div class="qbr-metric-card">
            <div class="qbr-metric-label">Tickets</div>
            <div class="qbr-metric-value">${trends.tickets || "N/A"}</div>
          </div>
        </div>

        ${
          rootCauses.length > 0
            ? `
          <div class="qbr-root-causes">
            <h4 class="qbr-subsection-title">Root Causes</h4>
            <div class="qbr-root-causes-list">
              ${rootCauses
                .map(
                  (cause) => `
                <div class="qbr-root-cause-item">
                  <div class="qbr-cause-header">
                    <span class="qbr-cause-issue">${cause.issue || "N/A"}</span>
                    <span class="qbr-cause-confidence">${((cause.confidence || 0) * 100).toFixed(0)}% confidence</span>
                  </div>
                </div>
              `,
                )
                .join("")}
            </div>
          </div>
        `
            : ""
        }

        ${
          signals?.wins?.length > 0
            ? `
          <div class="qbr-signals">
            <h4 class="qbr-subsection-title">Key Signals</h4>
            <div class="qbr-signals-list">
              ${signals.wins
                .map(
                  (signal) => `
                <div class="qbr-signal-item">
                  <span class="qbr-signal-type">${signal.signal_type || "N/A"}</span>
                  <span class="qbr-signal-strength">${signal.strength || "N/A"}</span>
                </div>
              `,
                )
                .join("")}
            </div>
          </div>
        `
            : ""
        }
      </div>

      <!-- Executive Summary -->
      <div class="qbr-section">
        <h3 class="qbr-section-title">
          <span class="qbr-icon">📝</span>
          Executive Summary
        </h3>
        <p class="qbr-summary-text">${brief.executive_summary || "No summary available"}</p>

        ${
          brief.key_risks?.length > 0
            ? `
          <div class="qbr-brief-subsection">
            <h4 class="qbr-subsection-title">Key Risks</h4>
            <ul class="qbr-brief-list">
              ${brief.key_risks.map((risk) => `<li>${risk}</li>`).join("")}
            </ul>
          </div>
        `
            : ""
        }

        ${
          brief.opportunities_summary?.length > 0
            ? `
          <div class="qbr-brief-subsection">
            <h4 class="qbr-subsection-title">Opportunities Summary</h4>
            <ul class="qbr-brief-list">
              ${brief.opportunities_summary.map((opp) => `<li>${opp}</li>`).join("")}
            </ul>
          </div>
        `
            : ""
        }
      </div>

      <!-- Revenue Opportunities -->
      ${
        opportunities.length > 0
          ? `
        <div class="qbr-section">
          <h3 class="qbr-section-title">
            <span class="qbr-icon">💰</span>
            Revenue Opportunities
          </h3>
          <div class="qbr-opportunities-grid">
            ${opportunities
              .map(
                (opp) => `
              <div class="qbr-opportunity-card">
                <div class="qbr-opp-type">${opp.type || "N/A"}</div>
                <div class="qbr-opp-description">${opp.description || ""}</div>
                <div class="qbr-opp-value">${new Intl.NumberFormat("en-US", {
                  style: "currency",
                  currency: "USD",
                  maximumFractionDigits: 0,
                }).format(opp.estimated_value || 0)}</div>
              </div>
            `,
              )
              .join("")}
          </div>
        </div>
      `
          : ""
      }
    </div>
  `

  container.innerHTML = html
}

// ADDED FUNCTION: downloadQBRDeck
function downloadQBRDeck(deckTitle, deckData) {
  console.log("[v0] Downloading QBR deck:", deckTitle)
  const payload = {
    ...deckData,
    deck_title: deckTitle,
    account_id: state.selectedAlert?.id,
    agent_run_id: state.selectedAlert?.agentRunId,
  }
  fetch(`${API_CONFIG.baseUrl}/agent/action/download-deck`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
    .then((response) => response.blob())
    .then((blob) => {
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `${deckTitle.replace(/\s+/g, "-")}.pptx`
      a.click()
      showToast("success", "QBR Deck Downloaded", "Your QBR deck has been generated.")
    })
    .catch((error) => {
      console.error("[v0] Error downloading QBR deck:", error)
      showToast("error", "Failed to Download Deck", "Please check console for details.")
    })
}

// ADDED FUNCTION: renderChurnView
function renderChurnView(data, container) {
  if (!container) {
    console.error("[v0] renderChurnView: container is null")
    return
  }

  const { commercial_brief = {}, detected_root_causes = [], risk_summary = {} } = data || {}

  const brief = commercial_brief || {}
  const rootCauses = detected_root_causes || []
  const risk = risk_summary || {}

  const html = `
    <div class="churn-view">
      <!-- Risk Summary Section -->
      <div class="churn-risk-summary">
        <div class="risk-header">
          <div class="risk-level risk-${risk.risk_level?.toLowerCase() || "medium"}">
            <span class="risk-icon">⚠️</span>
            <span class="risk-label">${risk.risk_level?.toUpperCase() || "MEDIUM"} RISK</span>
          </div>
          <div class="risk-confidence">
            Confidence: ${Math.round((Number.parseFloat(risk.confidence_score) || 0) * 100)}%
          </div>
        </div>
        <div class="risk-impact">
          <div class="impact-label">SUMMARY</div>
          <div class="impact-text">${risk.executive_summary || "No summary available"}</div>
        </div>
        ${
          risk.estimated_impact
            ? `
        <div class="risk-impact">
          <div class="impact-label">ESTIMATED IMPACT</div>
          <div class="impact-text">${risk.estimated_impact}</div>
        </div>
        `
            : ""
        }
        ${
          risk.primary_driver
            ? `
        <div class="risk-driver">
          <div class="driver-label">PRIMARY DRIVER</div>
          <div class="driver-text">${risk.primary_driver}</div>
        </div>
        `
            : ""
        }
      </div>

      <!-- Root Causes Section -->
      ${
        rootCauses.length > 0
          ? `
      <div class="churn-section">
        <h3 class="churn-section-title">
          <span class="section-icon">🔍</span>
          Detected Root Causes
        </h3>
        <div class="root-causes-list">
          ${rootCauses
            .map(
              (rc) => `
            <div class="root-cause-item">
              <div class="root-cause-content">
                <div class="root-cause-text">${rc.cause}</div>
                <div class="confidence-badge">
                  ${Math.round((rc.confidence || 0) * 100)}% confidence
                </div>
              </div>
            </div>
          `,
            )
            .join("")}
        </div>
      </div>
      `
          : ""
      }

      <!-- Commercial Brief Section -->
      ${
        brief.title
          ? `
      <div class="churn-section">
        <h3 class="churn-section-title">
          <span class="section-icon">📊</span>
          ${brief.title || "Commercial Brief"}
        </h3>
        <div class="commercial-brief-content">
          ${
            brief.executive_summary
              ? `
          <div class="brief-item">
            <div class="brief-label">Executive Summary</div>
            <div class="brief-text">${brief.executive_summary}</div>
          </div>
          `
              : ""
          }
          ${
            brief.key_drivers && brief.key_drivers.length > 0
              ? `
          <div class="brief-item">
            <div class="brief-label">Key Drivers</div>
            <ul class="brief-list">
              ${brief.key_drivers.map((driver) => `<li>${driver}</li>`).join("")}
            </ul>
          </div>
          `
              : ""
          }
          ${
            brief.recommended_focus
              ? `
          <div class="brief-item">
            <div class="brief-label">Recommended Focus</div>
            <div class="brief-text">${brief.recommended_focus}</div>
          </div>
          `
              : ""
          }
        </div>
      </div>
      `
          : ""
      }
    </div>
  `

  container.innerHTML = html
}

// ADDED FUNCTION: renderChurnActions
function renderChurnActions(container, data, alertData) {
  console.log("[v0] renderChurnActions called")
  console.log("[v0] Container:", container)
  console.log("[v0] Data:", data)
  console.log("[v0] AlertData:", alertData)

  if (!container) {
    console.error("[v0] renderChurnActions: container is null")
    return
  }

  if (!data) {
    console.warn("[v0] renderChurnActions: no data provided")
    container.innerHTML = '<div style="padding: 1rem; text-align: center; color: #94a3b8;">No data available</div>'
    return
  }

  const actions = data.actions || []
  const emailDraft = data.email_draft || {}

  let html = '<div class="churn-actions-container">'

  // Action 1: Email Draft
  if (emailDraft && (emailDraft.subject || emailDraft.body_text)) {
    const customerEmail = alertData?.company ? `${alertData.company.toLowerCase().replace(/\s+/g, "")}@company.com` : ""
    // Clean up escaped quotes from the API response
    const cleanValue = (val) => (val ? val.replace(/^"|"$/g, "").replace(/\\"/g, '"') : "")
    const emailTo = cleanValue(emailDraft.to) || customerEmail || "customer@company.com"
    const emailSubject = cleanValue(emailDraft.subject) || ""
    const emailBody = cleanValue(emailDraft.body_text) || ""

    html += `
      <div class="churn-action-card">
        <div class="churn-action-header">
          <h3 class="churn-action-title">Send Retention Email</h3>
        </div>
        <div class="churn-email-editor">
          <div class="churn-email-field">
            <label>To:</label>
            <input type="text" class="churn-email-input" value="${emailTo}" data-field="to" />
          </div>
          <div class="churn-email-field">
            <label>Subject:</label>
            <input type="text" class="churn-email-input" value="${emailSubject}" data-field="subject" />
          </div>
          <div class="churn-email-field">
            <label>Body:</label>
            <textarea class="churn-email-textarea" rows="8" data-field="body">${emailBody}</textarea>
          </div>
        </div>
        <div class="churn-action-buttons">
          <button class="churn-btn churn-btn-secondary" onclick="editChurnEmail(this)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            Edit
          </button>
          <button class="churn-btn churn-btn-primary" onclick="sendChurnEmail(this)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
            Send
          </button>
        </div>
        <button class="churn-btn churn-btn-ghost" onclick="saveChurnDraft(this)" style="margin-top: 8px;">Save Draft</button>
      </div>
    `
  }

  // Action 2: Retention Actions with fixed layout
  if (actions && actions.length > 0) {
    html += `
      <div class="churn-action-card">
        <div class="churn-action-header">
          <h3 class="churn-action-title">Retention Actions</h3>
        </div>
        <div class="churn-actions-list">
    `

    actions.forEach((action, index) => {
      const priorityClass = action.priority ? `priority-${action.priority.toLowerCase()}` : "priority-medium"
      const priorityLabel = action.priority || "Medium"
      const actionTitle = action.title || action.action || "Action"
      const actionDesc = action.description || action.rationale || ""
      const dueDate = action.due_date || "" // Use due_date if available, otherwise leave empty

      html += `
        <div class="churn-action-item">
          <div class="churn-action-content">
            <span class="churn-priority-badge ${priorityClass}">${priorityLabel.toUpperCase()}</span>
            <h4 class="churn-action-item-title">${actionTitle}</h4>
            <p class="churn-action-description">${actionDesc}</p>
            ${dueDate ? `<span class="churn-due-date">Due: ${dueDate}</span>` : ""}
          </div>
          <button class="churn-btn churn-btn-primary churn-btn-task" onclick="logChurnTask(${index}, ${JSON.stringify(action).replace(/"/g, "&quot;")})">
            Log Task
          </button>
        </div>
      `
    })

    html += `
        </div>
      </div>
    `
  }

  html += "</div>"

  console.log("[v0] Setting innerHTML with", html.length, "characters")
  container.innerHTML = html
  console.log("[v0] innerHTML set successfully")
}

// Email action handlers for Churn
function editChurnEmail(button) {
  const card = button.closest(".churn-action-card")
  const inputs = card.querySelectorAll(".churn-email-input, .churn-email-textarea")

  inputs.forEach((input) => {
    input.disabled = false
    input.focus()
  })

  showToast("info", "Edit Mode", "You can now edit the email fields")
}

function sendChurnEmail(button) {
  const card = button.closest(".churn-action-card")
  const to = card.querySelector('[data-field="to"]').value
  const subject = card.querySelector('[data-field="subject"]').value
  const body = card.querySelector('[data-field="body"]').value

  console.log("[v0] Sending churn email:", { to, subject, body })

  // TODO: Implement actual email sending
  showToast("success", "Email Sent", `Retention email sent to ${to}`)
}

function saveChurnDraft(button) {
  const card = button.closest(".churn-action-card")
  const to = card.querySelector('[data-field="to"]').value
  const subject = card.querySelector('[data-field="subject"]').value
  const body = card.querySelector('[data-field="body"]').value

  console.log("[v0] Saving churn email draft:", { to, subject, body })

  showToast("success", "Draft Saved", "Email draft saved successfully")
}

function logChurnTask(index, actionData) {
  console.log("[v0] Logging churn task:", index, actionData)

  // Prepare payload matching the create-crm-task structure
  const payload = {
    account_id: state.selectedAlert?.id, // Use selectedAlert.id for account ID
    agent_run_id: state.selectedAlert?.agentRunId, // Use selectedAlert.agentRunId
    tasks: [
      {
        title: actionData.title || actionData.action || "Retention Task",
        description: actionData.description || actionData.rationale || "",
      },
    ],
  }

  console.log("[v0] Sending task payload:", payload)

  // TODO: Implement actual API call
  fetch(`${API_CONFIG.baseUrl}/agent/action/create-crm-task`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("[v0] Task logged successfully:", data)
      showToast("success", "Task Logged", "Retention task logged to CRM")
    })
    .catch((error) => {
      console.error("[v0] Error logging task:", error)
      showToast("error", "Failed to Log Task", "Please check console for details.")
    })
}

// ADDED FUNCTION: renderSupplyView
function renderSupplyView(data, container) {
  if (!container) {
    console.error("[v0] renderSupplyView: container is null")
    return
  }

  const { risk_summary = {}, detected_root_causes = [], commercial_brief = {} } = data || {}

  const riskLevel = risk_summary.risk_level || "Medium"
  const confidenceScore = Math.round((risk_summary.confidence_score || 0.5) * 100)
  const executiveSummary = risk_summary.executive_summary || "No summary available"
  const estimatedImpact = risk_summary.estimated_impact || ""
  const primaryDriver = risk_summary.primary_driver || ""

  const html = `
    <div class="churn-view">
      <!-- Risk Summary Section -->
      <div class="churn-risk-summary">
        <div class="risk-header">
          <div class="risk-level risk-${riskLevel.toLowerCase()}">
            <span class="risk-icon">⚠️</span>
            <span class="risk-label">${riskLevel.toUpperCase()} RISK</span>
          </div>
          <div class="risk-confidence">
            Score: ${confidenceScore}%
          </div>
        </div>
        <div class="risk-impact">
          <div class="impact-label">SUMMARY</div>
          <div class="impact-text">${executiveSummary}</div>
        </div>
        ${
          estimatedImpact
            ? `
        <div class="risk-impact">
          <div class="impact-label">ESTIMATED IMPACT</div>
          <div class="impact-text">${estimatedImpact}</div>
        </div>
        `
            : ""
        }
        ${
          primaryDriver
            ? `
        <div class="risk-driver">
          <div class="driver-label">PRIMARY DRIVER</div>
          <div class="driver-text">${primaryDriver}</div>
        </div>
        `
            : ""
        }
      </div>

      <!-- Root Causes Section -->
      ${
        detected_root_causes.length > 0
          ? `
      <div class="churn-section">
        <h3 class="churn-section-title">
          <span class="section-icon">🔍</span>
          Detected Root Causes
        </h3>
        <div class="root-causes-list">
          ${detected_root_causes
            .map(
              (cause) => `
            <div class="root-cause-item">
              <div class="root-cause-content">
                <div class="root-cause-text">${cause.cause}</div>
                <div class="confidence-badge">
                  ${Math.round((cause.confidence || 0) * 100)}% confidence
                </div>
              </div>
            </div>
          `,
            )
            .join("")}
        </div>
      </div>
      `
          : ""
      }

      <!-- Commercial Brief Section -->
      ${
        commercial_brief.title
          ? `
      <div class="churn-section">
        <h3 class="churn-section-title">
          <span class="section-icon">📊</span>
          ${commercial_brief.title || "Commercial Brief"}
        </h3>
        <div class="commercial-brief-content">
          ${
            commercial_brief.executive_summary
              ? `
          <div class="brief-item">
            <div class="brief-label">Executive Summary</div>
            <div class="brief-text">${commercial_brief.executive_summary}</div>
          </div>
          `
              : ""
          }
          ${
            commercial_brief.key_drivers && commercial_brief.key_drivers.length > 0
              ? `
          <div class="brief-item">
            <div class="brief-label">Key Drivers</div>
            <ul class="brief-list">
              ${commercial_brief.key_drivers.map((driver) => `<li>${driver}</li>`).join("")}
            </ul>
          </div>
          `
              : ""
          }
          ${
            commercial_brief.recommended_focus
              ? `
          <div class="brief-item">
            <div class="brief-label">Recommended Focus</div>
            <div class="brief-text">${commercial_brief.recommended_focus}</div>
          </div>
          `
              : ""
          }
        </div>
      </div>
      `
          : ""
      }
    </div>
  `

  container.innerHTML = html
}

// ADDED FUNCTION: renderSupplyActions
function renderSupplyActions(container, data, alertData) {
  console.log("[v0] renderSupplyActions called")
  console.log("[v0] Container:", container)
  console.log("[v0] Data:", data)
  console.log("[v0] AlertData:", alertData)

  if (!container) {
    console.error("[v0] renderSupplyActions: container is null")
    return
  }

  if (!data) {
    console.warn("[v0] renderSupplyActions: no data provided")
    container.innerHTML = '<div style="padding: 1rem; text-align: center; color: #94a3b8;">No data available</div>'
    return
  }

  const actions = data.actions || []
  const email = data.email || {}

  let html = '<div class="churn-actions-container">'

  // Action 1: Email Draft
  if (email && (email.subject || email.body_text)) {
    const customerEmail = alertData?.company ? `${alertData.company.toLowerCase().replace(/\s+/g, "")}@company.com` : ""
    const cleanValue = (val) => (val ? val.replace(/^"|"$/g, "").replace(/\\"/g, '"') : "")
    const emailTo = cleanValue(email.to) || customerEmail || "customer@company.com"
    const emailSubject = cleanValue(email.subject) || ""
    const emailBody = cleanValue(email.body_text) || ""

    html += `
      <div class="churn-action-card">
        <div class="churn-action-header">
          <h3 class="churn-action-title">Send Supply Alert Email</h3>
        </div>
        <div class="churn-email-editor">
          <div class="churn-email-field">
            <label>To:</label>
            <input type="text" class="churn-email-input" value="${emailTo}" data-field="to" />
          </div>
          <div class="churn-email-field">
            <label>Subject:</label>
            <input type="text" class="churn-email-input" value="${emailSubject}" data-field="subject" />
          </div>
          <div class="churn-email-field">
            <label>Body:</label>
            <textarea class="churn-email-textarea" rows="8" data-field="body">${emailBody}</textarea>
          </div>
        </div>
        <div class="churn-action-buttons">
          <button class="churn-btn churn-btn-secondary" onclick="editSupplyEmail(this)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            Edit
          </button>
          <button class="churn-btn churn-btn-primary" onclick="sendSupplyEmail(this)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
            Send
          </button>
        </div>
        <button class="churn-btn churn-btn-ghost" onclick="saveSupplyDraft(this)" style="margin-top: 8px;">Save Draft</button>
      </div>
    `
  }

  // Action 2: Supply Actions
  if (actions && actions.length > 0) {
    html += `
      <div class="churn-action-card">
        <div class="churn-action-header">
          <h3 class="churn-action-title">Supply Chain Actions</h3>
        </div>
        <div class="churn-actions-list">
    `

    actions.forEach((action, index) => {
      const priorityClass = action.priority ? `priority-${action.priority.toLowerCase()}` : "priority-medium"
      const priorityLabel = action.priority || "Medium"
      const actionTitle = action.title || action.action || "Action"
      const actionDesc = action.description || action.owner || ""
      const dueDate = action.due_date || ""

      html += `
        <div class="churn-action-item">
          <div class="churn-action-content">
            <span class="churn-priority-badge ${priorityClass}">${priorityLabel.toUpperCase()}</span>
            <h4 class="churn-action-item-title">${actionTitle}</h4>
            ${actionDesc ? `<p class="churn-action-description">${actionDesc}</p>` : ""}
            ${dueDate ? `<span class="churn-due-date">Due: ${dueDate}</span>` : ""}
          </div>
          <button class="churn-btn churn-btn-primary churn-btn-task" onclick="logSupplyTask(${index}, ${JSON.stringify(action).replace(/"/g, "&quot;")})">
            Log Task
          </button>
        </div>
      `
    })

    html += `
        </div>
      </div>
    `
  }

  html += "</div>"

  console.log("[v0] Setting innerHTML for supplyActions container")
  container.innerHTML = html
  console.log("[v0] renderSupplyActions complete")
}

// Email action handlers for Supply
function editSupplyEmail(button) {
  const card = button.closest(".churn-action-card")
  const inputs = card.querySelectorAll(".churn-email-input, .churn-email-textarea")

  inputs.forEach((input) => {
    input.disabled = false
    input.focus()
  })

  showToast("info", "Edit Mode", "You can now edit the email fields")
}

function sendSupplyEmail(button) {
  const card = button.closest(".churn-action-card")
  const to = card.querySelector('[data-field="to"]').value
  const subject = card.querySelector('[data-field="subject"]').value
  const body = card.querySelector('[data-field="body"]').value

  console.log("[v0] Sending supply email:", { to, subject, body })

  showToast("success", "Email Sent", `Supply alert email sent to ${to}`)
}

function saveSupplyDraft(button) {
  const card = button.closest(".churn-action-card")
  const to = card.querySelector('[data-field="to"]').value
  const subject = card.querySelector('[data-field="subject"]').value
  const body = card.querySelector('[data-field="body"]').value

  console.log("[v0] Saving supply email draft:", { to, subject, body })

  showToast("success", "Draft Saved", "Email draft saved successfully")
}

function logSupplyTask(index, actionData) {
  console.log("[v0] Logging supply task:", index, actionData)

  const payload = {
    account_id: state.selectedAlert?.id,
    agent_run_id: state.selectedAlert?.agentRunId,
    tasks: [
      {
        title: actionData.title || actionData.action || "Supply Chain Task",
        description: actionData.description || actionData.owner || "",
      },
    ],
  }

  console.log("[v0] Sending task payload:", payload)

  fetch(`${API_CONFIG.baseUrl}/agent/action/create-crm-task`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("[v0] Task logged successfully:", data)
      showToast("success", "Task Logged", "Supply chain task logged to CRM")
    })
    .catch((error) => {
      console.error("[v0] Error logging task:", error)
      showToast("error", "Failed to Log Task", "Please check console for details.")
    })
}

// ========================================
// Initialize on DOM Ready
// ========================================

document.addEventListener("DOMContentLoaded", init)
