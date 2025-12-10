from sqlalchemy import Column, String, UUID, DateTime, Date, Numeric, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from database import Base
from sqlalchemy.inspection import inspect

class BaseModel:
    def to_dict(self):
        return {
            c.key: str(getattr(self, c.key)) 
            for c in inspect(self).mapper.column_attrs
        }

class Accounts(BaseModel, Base):
    __tablename__ = "accounts"

    account_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_name = Column(String(255), nullable=False)
    industry = Column(String(100))
    region = Column(String(100))
    segment = Column(String(50))
    status = Column(String(50), default="active")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Customers(BaseModel, Base):
    __tablename__ = "customers"

    customer_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True))
    customer_name = Column(String(255), nullable=False)
    customer_type = Column(String(50))
    email = Column(String(255))
    phone = Column(String(50))
    country = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())

class Plants(BaseModel, Base):
    __tablename__ = "plants"

    plant_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.account_id"))
    plant_name = Column(String(255))
    country = Column(String(100))
    city = Column(String(100))
    capacity = Column(Numeric(12,2))
    created_at = Column(DateTime, server_default=func.now())

class Products(BaseModel, Base):
    __tablename__ = "products"

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sku = Column(String(100), unique=True, nullable=False)
    product_name = Column(String(255), nullable=False)
    product_category = Column(String(100))
    unit_of_measure = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())

class Contracts(BaseModel, Base):
    __tablename__ = "contracts"

    contract_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True))
    contract_number = Column(String(100), unique=True)
    start_date = Column(Date)
    end_date = Column(Date)
    contract_value = Column(Numeric(14,2))
    sla_level = Column(String(50))
    status = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())

class Users(BaseModel, Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(String(50))
    region = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())

class Orders(BaseModel, Base):
    __tablename__ = "orders"

    order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True))
    customer_id = Column(UUID(as_uuid=True))
    plant_id = Column(UUID(as_uuid=True))
    contract_id = Column(UUID(as_uuid=True))
    order_date = Column(Date, nullable=False)
    order_status = Column(String(50))
    total_amount = Column(Numeric(14,2))
    created_at = Column(DateTime, server_default=func.now())

class OrderLines(BaseModel, Base):
    __tablename__ = "order_lines"

    order_line_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True))
    product_id = Column(UUID(as_uuid=True))
    quantity = Column(Numeric(12,2))
    unit_price = Column(Numeric(12,2))
    line_amount = Column(Numeric(14,2))

class Shipments(BaseModel, Base):
    __tablename__ = "shipments"

    shipment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True))
    shipment_date = Column(Date)
    carrier = Column(String(100))
    tracking_number = Column(String(100))
    delivery_status = Column(String(50))

class Invoices(BaseModel, Base):
    __tablename__ = "invoices"

    invoice_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True))
    invoice_date = Column(Date)
    due_date = Column(Date)
    invoice_amount = Column(Numeric(14,2))
    payment_status = Column(String(50))

class UsageMetrics(BaseModel, Base):
    __tablename__ = "usage_metrics"

    usage_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True))
    product_id = Column(UUID(as_uuid=True))
    usage_date = Column(Date)
    usage_volume = Column(Numeric(14,2))
    usage_unit = Column(String(50))

class QualityIncidents(BaseModel, Base):
    __tablename__ = "quality_incidents"

    incident_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True))
    product_id = Column(UUID(as_uuid=True))
    plant_id = Column(UUID(as_uuid=True))
    incident_date = Column(Date)
    defect_type = Column(String(255))
    severity = Column(String(50))
    resolution_status = Column(String(50))

class OeeMetrics(BaseModel, Base):
    __tablename__ = "oee_metrics"

    oee_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plant_id = Column(UUID(as_uuid=True))
    metric_date = Column(Date)
    availability = Column(Numeric(5,2))
    performance = Column(Numeric(5,2))
    quality = Column(Numeric(5,2))
    oee_score = Column(Numeric(5,2))

class SupportTickets(BaseModel, Base):
    __tablename__ = "support_tickets"

    ticket_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True))
    product_id = Column(UUID(as_uuid=True))
    opened_date = Column(Date)
    closed_date = Column(Date)
    issue_type = Column(String(255))
    priority = Column(String(50))
    status = Column(String(50))

class AgentRuns(BaseModel,Base):
    __tablename__ = "agent_runs"

    agent_run_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    run_type = Column(String(50))
    status = Column(String(50))

    # def to_dict(self):
    #     return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Signals(BaseModel, Base):
    __tablename__ = "signals"

    signal_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_run_id = Column(UUID(as_uuid=True))
    account_id = Column(UUID(as_uuid=True))
    signal_type = Column(String(100))          # churn, growth, risk etc.
    signal_strength = Column(Numeric(5,2))
    detected_at = Column(DateTime, server_default=func.now())
    extras = Column(JSONB)

class ChurnRiskAssessments(BaseModel, Base):
    __tablename__ = "churn_risk_assessments"

    assessment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id = Column(UUID(as_uuid=True))
    account_id = Column(UUID(as_uuid=True))
    risk_score = Column(Numeric(5,2))
    risk_level = Column(String(50))
    assessed_at = Column(DateTime, server_default=func.now())

class RcaAnalysis(BaseModel, Base):
    __tablename__ = "rca_analysis"

    rca_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id = Column(UUID(as_uuid=True))
    root_causes = Column(JSONB)                # JSON payload from LLM
    confidence_score = Column(Numeric(5,2))
    created_at = Column(DateTime, server_default=func.now())

class ChurnBriefs(BaseModel, Base):
    __tablename__ = "churn_briefs"

    brief_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id = Column(UUID(as_uuid=True))
    account_id = Column(UUID(as_uuid=True))
    brief_text = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

class EmailDrafts(BaseModel, Base):
    __tablename__ = "email_drafts"

    email_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id = Column(UUID(as_uuid=True))
    to_email = Column(String(255))
    subject = Column(String(255))
    body_text = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

class CrmActivities(BaseModel, Base):
    __tablename__ = "crm_activities"

    activity_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True))
    signal_id = Column(UUID(as_uuid=True))
    activity_type = Column(String(100))        # call/task/meeting etc.
    description = Column(Text)
    due_date = Column(Date)
    status = Column(String(50))

class Recommendations(BaseModel, Base):
    __tablename__ = "recommendations"

    recommendation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id = Column(UUID(as_uuid=True))
    account_id = Column(UUID(as_uuid=True))
    action_type = Column(String(100))
    action_details = Column(Text)
    priority = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())

class LlmPrompts(BaseModel, Base):
    __tablename__ = "llm_prompts"

    prompt_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt_name = Column(String(255))
    prompt_template = Column(Text)
    version = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())

class VectorIndexMetadata(BaseModel, Base):
    __tablename__ = "vector_index_metadata"

    vector_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = Column(String(100))
    entity_id = Column(UUID(as_uuid=True))     # refers to signal/account/rca etc.
    embedding_model = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())

class AgentMemory(BaseModel, Base):
    __tablename__ = "agent_memory"

    memory_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_run_id = Column(UUID(as_uuid=True))
    memory_type = Column(String(100))          # short_term / long_term
    memory_payload = Column(JSONB)
    created_at = Column(DateTime, server_default=func.now())

class LLMSignalPayloads(Base):
    __tablename__ = "llm_signal_payloads"

    payload_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_run_id = Column(UUID(as_uuid=True), nullable=False)
    account_id = Column(UUID(as_uuid=True), nullable=False)
    use_case_name = Column(String(100), nullable=False)
    final_score = Column(Numeric(5, 2), nullable=False)
    payload_json = Column(JSONB, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class ExpansionRcaAnalysis(Base):
    __tablename__ = "expansion_rca_analysis"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_run_id = Column(UUID(as_uuid=True), nullable=False)

    usage_anomalies = Column(JSONB, nullable=True)
    competitor_dependency = Column(JSONB, nullable=True)
    bom_gaps = Column(JSONB, nullable=True)
    revenue_leakage_estimate = Column(JSONB, nullable=True)

    created_at = Column(DateTime, server_default=func.now())


class ExpansionBrief(Base):
    __tablename__ = "expansion_briefs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_run_id = Column(UUID(as_uuid=True), nullable=False)

    brief_summary = Column(Text, nullable=False)
    whitespace_opportunities = Column(JSONB, nullable=True)
    cross_sell_targets = Column(JSONB, nullable=True)

    created_at = Column(DateTime, server_default=func.now())


class ExpansionRevenueEstimate(Base):
    __tablename__ = "expansion_revenue_estimates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_run_id = Column(UUID(as_uuid=True), nullable=False)

    estimated_monthly_revenue = Column(Numeric, nullable=False)
    estimated_annual_revenue = Column(Numeric, nullable=False)
    currency = Column(String(10), nullable=False)

    assumptions = Column(JSONB, nullable=True)

    created_at = Column(DateTime, server_default=func.now())


class ExpansionRecommendation(Base):
    __tablename__ = "expansion_recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_run_id = Column(UUID(as_uuid=True), nullable=False)

    priority = Column(Integer, nullable=False)
    recommendation_type = Column(String(50), nullable=False)

    target_sku = Column(String(100), nullable=True)
    rationale = Column(Text, nullable=True)
    expected_lift = Column(Numeric, nullable=True)

    created_at = Column(DateTime, server_default=func.now())


class ExpansionDeck(Base):
    __tablename__ = "expansion_decks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_run_id = Column(UUID(as_uuid=True), nullable=False)

    deck_title = Column(Text, nullable=False)
    slide_count = Column(Integer, nullable=False)

    deck_outline = Column(JSONB, nullable=True)

    created_at = Column(DateTime, server_default=func.now())