#!/usr/bin/env python3
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, HttpUrl
from datetime import date

class RecallReason(Enum):
    MISBRANDING = 'Misbranding'
    CONTAMINATION = 'Product Contamination'
    ALLERGENS = 'Unreported Allergens'
    UNINSPECTED = 'Produced Without Benefit of Inspection'
    MISLABELING = 'Mislabeling'
    PROCESSING = 'Processing Defect'
    IMPORT_VIOLATION = 'Import Violation'
    UNFIT = 'Unfit for Human Consumption'
    INSANITARY = 'Insanitary Conditions'


class RecallStatus(Enum):
    ACTIVE = "Active"
    CLOSED = "Closed"


class RiskLevel(Enum):
    URGENT = "Urgent"
    HIGH = "High"
    LOW = "Low"
    MARGINAL = "Marginal"


class UsdaEstablishment(BaseModel):
    id: Optional[str] = None
    url: HttpUrl
    slug: str
    name: Optional[str] = None
    address: Optional[str] = None
    telephone: Optional[str] = None
    grant_date: Optional[date] = None
    activities: List[str] = []


class UsdaRecall(BaseModel):
    id: str
    title: str
    url: HttpUrl
    reasons: List[RecallReason]
    status: RecallStatus
    risk_level: Optional[RiskLevel] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    summary: Optional[str] = None
    establishment: Optional[UsdaEstablishment] = None
    impacted_products: List[str] = []
    quantity_recovered: Optional[int] = None
    quantity_unit: Optional[str] = None
    states: Optional[List[str]] = None
