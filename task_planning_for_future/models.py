import datetime

from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, DateTime, Integer, Enum

Base = declarative_base()


class AuditMixin:
    # in prod is better to use datetime.utcnow
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


TaskTypes = Enum(
    "send_feedback_email_to_customer",
    "send_confirmation_email_for_host",
    name="task_type",
)


class TaskPlan(AuditMixin, Base):
    task_plan_id = Column(Integer, primary_key=True)
    task_type = Column(TaskTypes, default="send_invoice")
    execution_date = Column(DateTime)
    kwargs = Column(JSON)
    active = Column(Boolean, default=True)
