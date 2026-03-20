from sqlalchemy import Column, BigInteger, String, Boolean, Text, ARRAY, ForeignKey, Sequence
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import uuid


class Region(Base):
    __tablename__ = "region"

    id = Column(BigInteger, primary_key=True)
    region_name = Column(String)


class Court(Base):
    __tablename__ = "court"

    id = Column(BigInteger, primary_key=True)
    city = Column(String)
    name = Column(String)
    region_id = Column(BigInteger, ForeignKey("region.id"), nullable=False)


class CourtCase(Base):
    __tablename__ = "court_case"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    start_time_epoch = Column(BigInteger, nullable=False)
    court_id = Column(BigInteger, ForeignKey("court.id"), nullable=False)
    case_id = Column(String)
    claimant = Column(String)
    defendant = Column(String)
    duration = Column(BigInteger)
    hearing_channel = Column(String)
    hearing_type = Column(String)
    case_details = Column(Text)
    created_at = Column(BigInteger)
    is_minor = Column(Boolean)


subscription_id_seq = Sequence("subscription_seq")


class Subscription(Base):
    __tablename__ = "subscription"

    id = Column(BigInteger, subscription_id_seq, primary_key=True, server_default=subscription_id_seq.next_value())
    chat_id = Column(BigInteger)
    alert_terms_claimant = Column(ARRAY(String), default=[])
    alert_terms_defendant = Column(ARRAY(String), default=[])
    last_notified_timestamp = Column(BigInteger)
