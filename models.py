from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional, Any

class ThreatSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ResponseStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class ActionType(Enum):
    ALERT = "alert"
    LOG = "log"
    BLOCK_IP = "block_ip"
    BLOCK_PORT = "block_port"
    ISOLATE_SERVICE = "isolate_service"
    RATE_LIMIT = "rate_limit"
    QUARANTINE = "quarantine"
    CUSTOM = "custom"

@dataclass
class ThreatEvent:
    event_id: str
    timestamp: datetime
    source_ip: str
    target_ip: str
    target_ports: List[int]
    severity: ThreatSeverity
    threat_type: str
    description: str
    scan_id: Optional[str] = None
    cve_ids: List[str] = field(default_factory=list)
    service_info: Dict[str, Any] = field(default_factory=dict)
    confidence_score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ResponseAction:
    action_id: str
    action_type: ActionType
    target: str
    parameters: Dict[str, Any]
    priority: int = 5
    timeout: int = 30
    retry_count: int = 0
    max_retries: int = 3
    description: str = ""

@dataclass
class ResponseResult:
    action_id: str
    status: ResponseStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    success: bool = False
    error_message: Optional[str] = None
    output: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AlertConfig:
    enabled: bool = True
    channels: List[str] = field(default_factory=lambda: ["log"])
    email_recipients: List[str] = field(default_factory=list)
    webhook_urls: List[str] = field(default_factory=list)
    min_severity: ThreatSeverity = ThreatSeverity.MEDIUM
    rate_limit_seconds: int = 60
    aggregation_window: int = 300

@dataclass
class ResponsePlaybook:
    playbook_id: str
    name: str
    description: str
    severity: ThreatSeverity
    threat_types: List[str]
    actions: List[ResponseAction]
    enabled: bool = True
    auto_execute: bool = False
    requires_approval: bool = True

