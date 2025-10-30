"""
Surya - The All-Seeing Reconnaissance Module
Network scanning and service discovery engine
Optimized for Kali Linux environment
"""

import asyncio
import nmap
from typing import Dict, List, Optional
from datetime import datetime
from common.logger import logger
from common.validators import sanitize_target, validate_port_range
from common.exceptions import ScanError
from surya.models import ScanResult, HostInfo, PortInfo
from config.settings import settings


class SuryaScanner:
    """
    Advanced network reconnaissance scanner
    Wraps Nmap with async capabilities and structured output
    """
    
    def __init__(self):
        self.nm = nmap.PortScanner()
        self.scan_id = None
        
    async def scan_target(
        self,
        target: str,
        ports: str = None,
        scan_type: str = "tcp_connect",
        timeout: int = None
    ) -> ScanResult:
        """
        Perform asynchronous network scan
        
        Args:
            target: IP address, hostname, or CIDR range
            ports: Port range (e.g., '1-1000', '80,443,8080')
            scan_type: Type of scan (tcp_connect, syn, udp, service_detection)
            timeout: Scan timeout in seconds
            
        Returns:
            ScanResult object with structured data
        """
        # Validate inputs
        target = sanitize_target(target)
        ports = ports or settings.DEFAULT_PORT_RANGE
        if not validate_port_range(ports):
            raise ScanError(f"Invalid port range: {ports}")
        
        timeout = timeout or settings.SCAN_TIMEOUT
        scan_id = f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        logger.info(
            "scan_initiated",
            scan_id=scan_id,
            target=target,
            ports=ports,
            scan_type=scan_type
        )
        
        try:
            # Build nmap arguments based on scan type
            nmap_args = self._build_nmap_args(scan_type)
            
            # Run scan in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self.nm.scan,
                target,
                ports,
                nmap_args
            )
            
            # Parse results
            result = self._parse_scan_results(scan_id, target)
            
            logger.info(
                "scan_completed",
                scan_id=scan_id,
                hosts_found=len(result.hosts),
                total_ports=sum(len(h.ports) for h in result.hosts)
            )
            
            return result
            
        except Exception as e:
            logger.error("scan_failed", scan_id=scan_id, error=str(e))
            raise ScanError(f"Scan failed: {str(e)}")
    
    def _build_nmap_args(self, scan_type: str) -> str:
        """Build Nmap arguments based on scan type"""
        scan_profiles = {
            "tcp_connect": "-sT -T4",
            "syn": "-sS -T4",  # Requires root
            "udp": "-sU -T4",  # Requires root
            "service_detection": "-sV -T4",
            "os_detection": "-O -T4",  # Requires root
            "aggressive": "-A -T4",  # Requires root
            "stealth": "-sS -T2 -f",  # Requires root
        }
        
        args = scan_profiles.get(scan_type, "-sT -T4")
        
        # Add version detection for better service identification
        if "sV" not in args and scan_type != "tcp_connect":
            args += " -sV"
        
        return args
    
    def _parse_scan_results(self, scan_id: str, target: str) -> ScanResult:
        """Parse Nmap results into structured format"""
        hosts = []
        
        for host in self.nm.all_hosts():
            if self.nm[host].state() != "up":
                continue
                
            # Parse ports
            ports = []
            for proto in self.nm[host].all_protocols():
                port_list = self.nm[host][proto].keys()
                for port in port_list:
                    port_info = self.nm[host][proto][port]
                    ports.append(PortInfo(
                        port=port,
                        protocol=proto,
                        state=port_info.get('state', 'unknown'),
                        service=port_info.get('name', ''),
                        version=port_info.get('version', ''),
                        product=port_info.get('product', ''),
                        extra_info=port_info.get('extrainfo', '')
                    ))
            
            # Get hostname
            hostname = self.nm[host].hostname() if self.nm[host].hostname() else ""
            
            # Get OS info if available
            os_info = ""
            if 'osmatch' in self.nm[host]:
                os_matches = self.nm[host]['osmatch']
                if os_matches:
                    os_info = os_matches[0].get('name', '')
            
            hosts.append(HostInfo(
                ip=host,
                hostname=hostname,
                state=self.nm[host].state(),
                ports=ports,
                os_info=os_info
            ))
        
        return ScanResult(
            scan_id=scan_id,
            target=target,
            timestamp=datetime.now(),
            hosts=hosts,
            command=self.nm.command_line()
        )


# Convenience function for quick scans
async def quick_scan(target: str, ports: str = "1-1000") -> ScanResult:
    """Quick TCP connect scan"""
    scanner = SuryaScanner()
    return await scanner.scan_target(target, ports, scan_type="tcp_connect")
