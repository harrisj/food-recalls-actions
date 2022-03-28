#!/usr/bin/env python3
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, HttpUrl
from datetime import datetime

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
    HIGH = "High"
    LOW = "Low"
    MARGINAL = "Marginal"


class UsdaRecall(BaseModel):
    id: str
    title: str
    url: HttpUrl
    reasons: List[RecallReason]
    status: RecallStatus
    risk_level: Optional[RiskLevel] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    summary: Optional[str] = None
    impacted_products: List[str] = []
    quantity_recovered: Optional[int] = None
    quantity_unit: Optional[str] = None
    states: List[str] = None
