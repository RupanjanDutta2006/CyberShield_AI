"""CyberShield AI — Database Models (Part 19)

SQLAlchemy ORM models for off-chain persistence of Unified Threat Reports,
canonical hash indexing, and lookup history.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ThreatReportModel(Base):
    """Off-chain database storage model for Unified Threat Reports."""

    __tablename__ = "threat_reports"

    scan_id = Column(String(36), primary_key=True, index=True)
    target_type = Column(String(32), nullable=False)
    target_value = Column(String(2048), nullable=False, index=True)
    risk_classification = Column(String(64), nullable=False, index=True)
    risk_score = Column(Integer, nullable=True)
    canonical_hash = Column(String(66), nullable=True, index=True)
    created_at = Column(
        String(64),
        default=lambda: datetime.now(timezone.utc).isoformat(),
        nullable=False,
    )
    report_json = Column(Text, nullable=False)
    retrieval_count = Column(Integer, default=0, nullable=False)

    # Blockchain tracking fields
    on_chain_tx_hash = Column(String(66), nullable=True)
    on_chain_status = Column(String(32), default="not_registered", nullable=False)
    registered_at = Column(String(64), nullable=True)

