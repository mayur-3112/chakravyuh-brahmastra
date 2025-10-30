"""
Data models for Surya reconnaissance module
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class PortInfo(BaseModel):
    """Information about a scanned port"""
    port: int
    protocol: str
    state: str
    service: str = ""
    version: str = ""
    product: str = ""
    extra_info: str = ""


class HostInfo(BaseModel):
    """Information about a scanned host"""
    ip: str
    hostname: str = ""
    state: str
    ports: List[PortInfo] = Field(default_factory=list)
    os_info: str = ""


class ScanResult(BaseModel):
    """Complete scan result"""
    scan_id: str
    target: str
    timestamp: datetime
    hosts: List[HostInfo]
    command: str = ""
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
