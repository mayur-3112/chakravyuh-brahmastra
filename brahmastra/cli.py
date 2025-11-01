"""
Brahmastra CLI - Command Line Interface for Threat Response Engine
Save as: ~/chakravyuh/brahmastra/brahmastra/cli.py
"""

import asyncio
import argparse
import json
import sys
from datetime import datetime
from typing import List
from brahmastra.engine import BrahmastraEngine
from brahmastra.models import ThreatEvent, ThreatSeverity, ResponseResult
from brahmastra.playbooks import default_playbooks


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class BrahmastraCLI:
    """Command-line interface for Brahmastra"""
    
    def __init__(self):
        self.engine = BrahmastraEngine()
        self._load_playbooks()
    
    def _load_playbooks(self):
        """Load default playbooks into engine"""
        for playbook in default_playbooks():
            self.engine.register_playbook(playbook)
        print(f"{Colors.OKGREEN}✓ Loaded {len(self.engine.playbooks)} playbooks{Colors.ENDC}")
    
    def print_banner(self):
        """Print Brahmastra ASCII banner"""
        banner = f"""{Colors.OKBLUE}{Colors.BOLD}
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║   ██████╗ ██████╗  █████╗ ██╗  ██╗███╗   ███╗ █████╗ ║
║   ██╔══██╗██╔══██╗██╔══██╗██║  ██║████╗ ████║██╔══██╗║
║   ██████╔╝██████╔╝███████║███████║██╔████╔██║███████║║
║   ██╔══██╗██╔══██╗██╔══██║██╔══██║██║╚██╔╝██║██╔══██║║
║   ██████╔╝██║  ██║██║  ██║██║  ██║██║ ╚═╝ ██║██║  ██║║
║   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝║
║                                                       ║
║        Automated Threat Response Engine              ║
║              Project Chakravyuh                      ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
{Colors.ENDC}"""
        print(banner)
    
    def list_playbooks(self):
        """List all registered playbooks"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}📋 Registered Playbooks:{Colors.ENDC}\n")
        
        for idx, playbook in enumerate(self.engine.playbooks, 1):
            severity_color = self._get_severity_color(playbook.severity)
            enabled_status = f"{Colors.OKGREEN}✓ ENABLED{Colors.ENDC}" if playbook.enabled else f"{Colors.FAIL}✗ DISABLED{Colors.ENDC}"
            
            print(f"{Colors.BOLD}{idx}. {playbook.name}{Colors.ENDC}")
            print(f"   Severity: {severity_color}{playbook.severity.value}{Colors.ENDC}")
            print(f"   Threat Types: {', '.join(playbook.threat_types)}")
            print(f"   Actions: {len(playbook.actions)} configured")
            print(f"   Status: {enabled_status}")
            print(f"   Auto-execute: {playbook.auto_execute}")
            print()
    
    def _get_severity_color(self, severity: ThreatSeverity) -> str:
        """Get color code for severity level"""
        colors = {
            ThreatSeverity.LOW: Colors.OKBLUE,
            ThreatSeverity.MEDIUM: Colors.WARNING,
            ThreatSeverity.HIGH: Colors.FAIL,
            ThreatSeverity.CRITICAL: f"{Colors.FAIL}{Colors.BOLD}"
        }
        return colors.get(severity, Colors.ENDC)
    
    async def handle_threat(self, args):
        """Handle a threat event"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}🎯 Processing Threat Event{Colors.ENDC}\n")
        
        # Create threat event
        event = ThreatEvent(
            event_id=f"cli_{int(datetime.now().timestamp())}",
            timestamp=datetime.utcnow(),
            source_ip=args.source_ip,
            target_ip=args.target_ip,
            target_ports=args.ports if args.ports else [],
            severity=ThreatSeverity[args.severity.upper()],
            threat_type=args.threat_type,
            description=args.description or f"CLI triggered {args.threat_type}",
            confidence_score=args.confidence if args.confidence else 1.0
        )
        
        # Display event details
        self._print_event_details(event)
        
        # Execute response
        print(f"\n{Colors.OKCYAN}⚡ Executing response actions...{Colors.ENDC}\n")
        
        results = await self.engine.handle_threat(event)
        
        # Display results
        self._print_results(results)
        
        # Export if requested
        if args.export:
            self._export_results(results, args.export, event)
        
        return results
    
    def _print_event_details(self, event: ThreatEvent):
        """Print threat event details"""
        severity_color = self._get_severity_color(event.severity)
        
        print(f"{Colors.BOLD}Event Details:{Colors.ENDC}")
        print(f"  ID: {event.event_id}")
        print(f"  Type: {event.threat_type}")
        print(f"  Severity: {severity_color}{event.severity.value}{Colors.ENDC}")
        print(f"  Source IP: {event.source_ip}")
        print(f"  Target IP: {event.target_ip}")
        if event.target_ports:
            print(f"  Target Ports: {', '.join(map(str, event.target_ports))}")
        print(f"  Confidence: {event.confidence_score:.2%}")
    
    def _print_results(self, results: List[ResponseResult]):
        """Print execution results"""
        if not results:
            print(f"{Colors.WARNING}⚠ No matching playbooks found for this threat{Colors.ENDC}")
            return
        
        print(f"{Colors.BOLD}Execution Results:{Colors.ENDC}\n")
        
        for idx, result in enumerate(results, 1):
            status_icon = "✓" if result.success else "✗"
            status_color = Colors.OKGREEN if result.success else Colors.FAIL
            
            print(f"{status_color}{status_icon}{Colors.ENDC} Action {idx}/{len(results)}")
            print(f"  Action ID: {result.action_id}")
            print(f"  Status: {status_color}{result.status.value}{Colors.ENDC}")
            print(f"  Success: {result.success}")
            
            if result.completed_at and result.started_at:
                duration = (result.completed_at - result.started_at).total_seconds()
                print(f"  Duration: {duration:.2f}s")
            
            if result.error_message:
                print(f"  Error: {Colors.FAIL}{result.error_message}{Colors.ENDC}")
            
            print()
        
        # Summary
        success_count = sum(1 for r in results if r.success)
        print(f"{Colors.BOLD}Summary:{Colors.ENDC}")
        print(f"  Total Actions: {len(results)}")
        print(f"  Successful: {Colors.OKGREEN}{success_count}{Colors.ENDC}")
        print(f"  Failed: {Colors.FAIL}{len(results) - success_count}{Colors.ENDC}")
    
    def _export_results(self, results: List[ResponseResult], export_format: str, event: ThreatEvent):
        """Export results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if export_format == 'json':
            filename = f"brahmastra_results_{timestamp}.json"
            data = {
                "event": {
                    "event_id": event.event_id,
                    "threat_type": event.threat_type,
                    "severity": event.severity.value,
                    "source_ip": event.source_ip,
                    "target_ip": event.target_ip,
                    "timestamp": event.timestamp.isoformat()
                },
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
                ]
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"\n{Colors.OKGREEN}✓ Results exported to {filename}{Colors.ENDC}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Brahmastra - Automated Threat Response Engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Handle a port scan
  brahmastra respond --threat-type port_scan --severity low --source-ip 192.168.1.100 --target-ip 10.0.0.5

  # Handle an intrusion with multiple ports
  brahmastra respond --threat-type intrusion --severity high --source-ip 203.0.113.45 --target-ip 10.0.0.10 --ports 22 80 443

  # List all playbooks
  brahmastra list

  # Export results to JSON
  brahmastra respond --threat-type exploit_attempt --severity critical --source-ip 198.51.100.89 --target-ip 10.0.0.15 --export json
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all registered playbooks')
    
    # Respond command
    respond_parser = subparsers.add_parser('respond', help='Handle a threat event')
    respond_parser.add_argument('--threat-type', required=True, help='Type of threat (e.g., port_scan, intrusion, exploit_attempt)')
    respond_parser.add_argument('--severity', required=True, choices=['low', 'medium', 'high', 'critical'], help='Threat severity level')
    respond_parser.add_argument('--source-ip', required=True, help='Source IP address')
    respond_parser.add_argument('--target-ip', required=True, help='Target IP address')
    respond_parser.add_argument('--ports', type=int, nargs='+', help='Target ports (space-separated)')
    respond_parser.add_argument('--description', help='Threat description')
    respond_parser.add_argument('--confidence', type=float, help='Confidence score (0.0-1.0)')
    respond_parser.add_argument('--export', choices=['json', 'csv'], help='Export results to file')
    
    args = parser.parse_args()
    
    # Initialize CLI
    cli = BrahmastraCLI()
    cli.print_banner()
    
    if args.command == 'list':
        cli.list_playbooks()
    elif args.command == 'respond':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(cli.handle_threat(args))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
