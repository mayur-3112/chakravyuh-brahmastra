"""
Brahmastra REST API
FastAPI server for threat response engine
Save as: ~/chakravyuh/brahmastra/brahmastra/api.py
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum
import asyncio
import uuid

from brahmastra.engine import BrahmastraEngine
from brahmastra.models import (
    ThreatEvent, ThreatSeverity, ResponseStatus,
    ResponsePlaybook, ResponseAction
)
from brahmastra.playbooks import default_playbooks


# ==================== REQUEST/RESPONSE MODELS ====================

class ThreatSeverityEnum(str, Enum):
    """Severity levels for API"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ThreatEventRequest(BaseModel):
    """Request model for threat events"""
    source_ip: str = Field(..., example="192.168.1.100")
    target_ip: str = Field(..., example="10.0.0.5")
    target_ports: Optional[List[int]] = Field(default=[], example=[22, 80, 443])
    severity: ThreatSeverityEnum = Field(..., example="HIGH")
    threat_type: str = Field(..., example="intrusion")
    description: Optional[str] = Field(default="", example="Unauthorized access attempt")
    cve_ids: Optional[List[str]] = Field(default=[], example=["CVE-2021-44228"])
    confidence_score: Optional[float] = Field(default=1.0, ge=0.0, le=1.0, example=0.95)

    class Config:
        schema_extra = {
            "example": {
                "source_ip": "203.0.113.45",
                "target_ip": "10.0.0.10",
                "target_ports": [22],
                "severity": "HIGH",
                "threat_type": "intrusion",
                "description": "SSH brute force attack detected",
                "confidence_score": 0.95
            }
        }


class ResponseResultModel(BaseModel):
    """Response model for action results"""
    action_id: str
    status: str
    success: bool
    started_at: Optional[str]
    completed_at: Optional[str]
    error_message: Optional[str] = None


class ThreatResponseModel(BaseModel):
    """Response model for threat handling"""
    event_id: str
    status: str
    matched_playbooks: int
    actions_executed: int
    results: List[ResponseResultModel]
    timestamp: str


class PlaybookModel(BaseModel):
    """Model for playbook information"""
    playbook_id: str
    name: str
    description: str
    severity: str
    threat_types: List[str]
    action_count: int
    enabled: bool
    auto_execute: bool


class HealthCheckModel(BaseModel):
    """Health check response"""
    status: str
    version: str
    playbooks_loaded: int
    uptime_seconds: float


# ==================== FASTAPI APPLICATION ====================

app = FastAPI(
    title="Brahmastra Threat Response API",
    description="Automated threat response orchestration engine for Project Chakravyuh",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global engine instance
engine = BrahmastraEngine()
start_time = datetime.utcnow()


# ==================== STARTUP/SHUTDOWN EVENTS ====================

@app.on_event("startup")
async def startup_event():
    """Load playbooks on startup"""
    for playbook in default_playbooks():
        engine.register_playbook(playbook)
    print(f"✅ Brahmastra API started with {len(engine.playbooks)} playbooks")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 Brahmastra API shutting down...")


# ==================== API ENDPOINTS ====================

@app.get("/", tags=["Root"])
async def root():
    """API root endpoint"""
    return {
        "message": "Brahmastra Threat Response API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthCheckModel, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    uptime = (datetime.utcnow() - start_time).total_seconds()
    return {
        "status": "healthy",
        "version": "1.0.0",
        "playbooks_loaded": len(engine.playbooks),
        "uptime_seconds": uptime
    }


@app.get("/playbooks", response_model=List[PlaybookModel], tags=["Playbooks"])
async def list_playbooks():
    """List all registered playbooks"""
    playbooks = []
    for pb in engine.playbooks:
        playbooks.append({
            "playbook_id": pb.playbook_id,
            "name": pb.name,
            "description": pb.description,
            "severity": pb.severity.value,
            "threat_types": pb.threat_types,
            "action_count": len(pb.actions),
            "enabled": pb.enabled,
            "auto_execute": pb.auto_execute
        })
    return playbooks


@app.get("/playbooks/{playbook_id}", tags=["Playbooks"])
async def get_playbook(playbook_id: str):
    """Get specific playbook details"""
    for pb in engine.playbooks:
        if pb.playbook_id == playbook_id:
            return {
                "playbook_id": pb.playbook_id,
                "name": pb.name,
                "description": pb.description,
                "severity": pb.severity.value,
                "threat_types": pb.threat_types,
                "actions": [
                    {
                        "action_id": action.action_id,
                        "action_type": action.action_type.value,
                        "target": action.target,
                        "description": action.description
                    }
                    for action in pb.actions
                ],
                "enabled": pb.enabled,
                "auto_execute": pb.auto_execute,
                "requires_approval": pb.requires_approval
            }
    
    raise HTTPException(status_code=404, detail="Playbook not found")


@app.post("/threats", response_model=ThreatResponseModel, tags=["Threats"])
async def handle_threat(threat: ThreatEventRequest):
    """
    Handle a threat event and execute response actions
    
    This endpoint receives threat information and automatically executes
    appropriate response playbooks based on severity and threat type.
    """
    try:
        # Create threat event
        event = ThreatEvent(
            event_id=f"api_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.utcnow(),
            source_ip=threat.source_ip,
            target_ip=threat.target_ip,
            target_ports=threat.target_ports or [],
            severity=ThreatSeverity[threat.severity.value],
            threat_type=threat.threat_type,
            description=threat.description or f"API triggered {threat.threat_type}",
            cve_ids=threat.cve_ids or [],
            confidence_score=threat.confidence_score or 1.0
        )
        
        # Match playbooks
        matched = engine.match_playbooks(event)
        
        # Execute response
        results = await engine.handle_threat(event)
        
        # Format response
        response = {
            "event_id": event.event_id,
            "status": "completed" if results else "no_match",
            "matched_playbooks": len(matched),
            "actions_executed": len(results),
            "results": [
                {
                    "action_id": r.action_id,
                    "status": r.status.value,
                    "success": r.success,
                    "started_at": r.started_at.isoformat() if r.started_at else None,
                    "completed_at": r.completed_at.isoformat() if r.completed_at else None,
                    "error_message": r.error_message
                }
                for r in results
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error handling threat: {str(e)}")


@app.post("/threats/batch", tags=["Threats"])
async def handle_threats_batch(threats: List[ThreatEventRequest]):
    """
    Handle multiple threats in batch
    
    Processes multiple threat events concurrently and returns all results.
    """
    try:
        # Create threat events
        events = []
        for threat in threats:
            event = ThreatEvent(
                event_id=f"api_{uuid.uuid4().hex[:8]}",
                timestamp=datetime.utcnow(),
                source_ip=threat.source_ip,
                target_ip=threat.target_ip,
                target_ports=threat.target_ports or [],
                severity=ThreatSeverity[threat.severity.value],
                threat_type=threat.threat_type,
                description=threat.description or f"Batch API {threat.threat_type}",
                cve_ids=threat.cve_ids or [],
                confidence_score=threat.confidence_score or 1.0
            )
            events.append(event)
        
        # Execute all concurrently
        tasks = [engine.handle_threat(event) for event in events]
        all_results = await asyncio.gather(*tasks)
        
        # Format responses
        responses = []
        for event, results in zip(events, all_results):
            matched = engine.match_playbooks(event)
            responses.append({
                "event_id": event.event_id,
                "status": "completed" if results else "no_match",
                "matched_playbooks": len(matched),
                "actions_executed": len(results),
                "results": [
                    {
                        "action_id": r.action_id,
                        "status": r.status.value,
                        "success": r.success
                    }
                    for r in results
                ]
            })
        
        return {
            "total_threats": len(threats),
            "processed": len(responses),
            "responses": responses,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in batch processing: {str(e)}")


@app.get("/stats", tags=["Statistics"])
async def get_statistics():
    """Get API statistics"""
    return {
        "playbooks": {
            "total": len(engine.playbooks),
            "enabled": sum(1 for pb in engine.playbooks if pb.enabled),
            "disabled": sum(1 for pb in engine.playbooks if not pb.enabled)
        },
        "severity_distribution": {
            "LOW": sum(1 for pb in engine.playbooks if pb.severity == ThreatSeverity.LOW),
            "MEDIUM": sum(1 for pb in engine.playbooks if pb.severity == ThreatSeverity.MEDIUM),
            "HIGH": sum(1 for pb in engine.playbooks if pb.severity == ThreatSeverity.HIGH),
            "CRITICAL": sum(1 for pb in engine.playbooks if pb.severity == ThreatSeverity.CRITICAL)
        },
        "uptime_seconds": (datetime.utcnow() - start_time).total_seconds()
    }


# ==================== ERROR HANDLERS ====================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Not found", "detail": str(exc)}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
