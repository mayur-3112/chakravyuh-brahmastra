"""
Scanning endpoints for Brahmastra API
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

from surya.scanner import SuryaScanner, quick_scan
from surya.models import ScanResult
from common.logger import logger
from common.validators import sanitize_target, validate_port_range
from common.exceptions import ScanError


router = APIRouter()

# In-memory storage (for prototype - replace with Redis/DB in production)
active_scans = {}
completed_scans = {}


class ScanRequest(BaseModel):
    """Request model for initiating a scan"""
    target: str = Field(..., description="IP address, hostname, or CIDR range")
    ports: Optional[str] = Field("1-1000", description="Port range (e.g., '1-1000', '80,443,8080')")
    scan_type: Optional[str] = Field("tcp_connect", description="Scan type (tcp_connect, syn, service_detection)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "target": "192.168.1.1",
                "ports": "1-1000",
                "scan_type": "tcp_connect"
            }
        }


class ScanStatusResponse(BaseModel):
    """Response model for scan status"""
    scan_id: str
    status: str  # queued, running, completed, failed
    target: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None


async def perform_scan(scan_id: str, target: str, ports: str, scan_type: str):
    """Background task to perform scan"""
    try:
        active_scans[scan_id]["status"] = "running"
        active_scans[scan_id]["started_at"] = datetime.now()
        
        logger.info("scan_started", scan_id=scan_id, target=target)
        
        # Perform scan
        scanner = SuryaScanner()
        result = await scanner.scan_target(target, ports, scan_type)
        
        # Store result
        completed_scans[scan_id] = result
        active_scans[scan_id]["status"] = "completed"
        active_scans[scan_id]["completed_at"] = datetime.now()
        
        logger.info("scan_completed", scan_id=scan_id, hosts_found=len(result.hosts))
        
    except Exception as e:
        logger.error("scan_failed", scan_id=scan_id, error=str(e))
        active_scans[scan_id]["status"] = "failed"
        active_scans[scan_id]["error"] = str(e)
        active_scans[scan_id]["completed_at"] = datetime.now()


@router.post("/start", response_model=ScanStatusResponse)
async def start_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    """
    Initiate a new network scan
    
    Returns scan_id for tracking progress
    """
    try:
        # Validate inputs
        target = sanitize_target(request.target)
        if not validate_port_range(request.ports):
            raise HTTPException(status_code=400, detail=f"Invalid port range: {request.ports}")
        
        # Generate scan ID
        scan_id = f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Initialize scan tracking
        active_scans[scan_id] = {
            "scan_id": scan_id,
            "status": "queued",
            "target": target,
            "ports": request.ports,
            "scan_type": request.scan_type,
            "started_at": None,
            "completed_at": None,
            "error": None
        }
        
        # Queue scan as background task
        background_tasks.add_task(
            perform_scan, 
            scan_id, 
            target, 
            request.ports, 
            request.scan_type
        )
        
        logger.info("scan_queued", scan_id=scan_id, target=target)
        
        return ScanStatusResponse(**active_scans[scan_id])
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("scan_request_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to initiate scan")


@router.get("/status/{scan_id}", response_model=ScanStatusResponse)
async def get_scan_status(scan_id: str):
    """
    Get status of a specific scan
    """
    if scan_id not in active_scans:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    return ScanStatusResponse(**active_scans[scan_id])


@router.get("/result/{scan_id}", response_model=ScanResult)
async def get_scan_result(scan_id: str):
    """
    Get results of a completed scan
    """
    if scan_id not in completed_scans:
        if scan_id in active_scans:
            status = active_scans[scan_id]["status"]
            if status == "running" or status == "queued":
                raise HTTPException(status_code=202, detail=f"Scan still {status}")
            elif status == "failed":
                error = active_scans[scan_id].get("error", "Unknown error")
                raise HTTPException(status_code=500, detail=f"Scan failed: {error}")
        raise HTTPException(status_code=404, detail="Scan not found")
    
    return completed_scans[scan_id]


@router.get("/list", response_model=List[ScanStatusResponse])
async def list_scans(status: Optional[str] = None):
    """
    List all scans, optionally filtered by status
    """
    scans = list(active_scans.values())
    
    if status:
        scans = [s for s in scans if s["status"] == status]
    
    return [ScanStatusResponse(**s) for s in scans]


@router.delete("/delete/{scan_id}")
async def delete_scan(scan_id: str):
    """
    Delete a scan and its results
    """
    if scan_id not in active_scans:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    # Remove from storage
    del active_scans[scan_id]
    if scan_id in completed_scans:
        del completed_scans[scan_id]
    
    logger.info("scan_deleted", scan_id=scan_id)
    
    return {"message": "Scan deleted successfully", "scan_id": scan_id}
