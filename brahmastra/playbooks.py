"""
Default Response Playbooks
Pre-configured threat response strategies
Save as: ~/chakravyuh/brahmastra/brahmastra/playbooks.py
"""

import uuid
from brahmastra.models import (
    ResponsePlaybook, ResponseAction, ActionType, ThreatSeverity
)


def default_playbooks():
    """Create default playbooks with actions for testing"""
    
    # LOW Severity: Port Scan Response
    actions_low = [
        ResponseAction(
            action_id=str(uuid.uuid4()),
            action_type=ActionType.LOG,
            target="local",
            parameters={"message": "Low severity threat logged"},
            description="Log low severity threat"
        ),
    ]
    
    # MEDIUM Severity: Suspicious Activity Response
    actions_medium = [
        ResponseAction(
            action_id=str(uuid.uuid4()),
            action_type=ActionType.ALERT,
            target="security-team@example.com",
            parameters={"email_subject": "Medium severity alert"},
            description="Send medium severity alert email"
        ),
        ResponseAction(
            action_id=str(uuid.uuid4()),
            action_type=ActionType.LOG,
            target="local",
            parameters={"message": "Medium severity threat logged"},
            description="Log medium severity threat"
        ),
    ]
    
    # HIGH Severity: Intrusion Response
    actions_high = [
        ResponseAction(
            action_id=str(uuid.uuid4()),
            action_type=ActionType.ALERT,
            target="security-team@example.com",
            parameters={"email_subject": "High severity alert"},
            description="Send high severity alert email"
        ),
        ResponseAction(
            action_id="act_block_ip_intrusion",  # Explicit ID for test matching
            action_type=ActionType.BLOCK_IP,
            target="192.168.1.0/24",
            parameters={"duration": "1 hour"},
            description="Block IP range for 1 hour"
        ),
    ]
    
    # CRITICAL Severity: Exploit Response
    actions_critical = [
        ResponseAction(
            action_id=str(uuid.uuid4()),
            action_type=ActionType.ALERT,
            target="security-team@example.com",
            parameters={"email_subject": "CRITICAL severity alert"},
            description="Send CRITICAL severity alert email"
        ),
        ResponseAction(
            action_id=str(uuid.uuid4()),
            action_type=ActionType.BLOCK_IP,
            target="0.0.0.0/0",
            parameters={"duration": "permanent"},
            description="Permanently block all traffic"
        ),
        ResponseAction(
            action_id=str(uuid.uuid4()),
            action_type=ActionType.ISOLATE_SERVICE,
            target="web_server",
            parameters={"method": "firewall"},
            description="Isolate web server"
        ),
    ]
    
    playbook_low = ResponsePlaybook(
        playbook_id=str(uuid.uuid4()),
        name="Low Severity Default Playbook",
        description="Handles low severity threats by logging",
        severity=ThreatSeverity.LOW,
        threat_types=["port_scan", "recon"],
        actions=actions_low,
        enabled=True,
        auto_execute=True,
        requires_approval=False
    )
    
    playbook_medium = ResponsePlaybook(
        playbook_id=str(uuid.uuid4()),
        name="Medium Severity Default Playbook",
        description="Handles medium severity threats with alerts and logging",
        severity=ThreatSeverity.MEDIUM,
        threat_types=["port_scan", "suspicious_activity", "anomaly"],
        actions=actions_medium,
        enabled=True,
        auto_execute=True,
        requires_approval=False
    )
    
    playbook_high = ResponsePlaybook(
        playbook_id=str(uuid.uuid4()),
        name="High Severity Default Playbook",
        description="Handles high severity threats with alert and IP block",
        severity=ThreatSeverity.HIGH,
        threat_types=["intrusion", "exploit_attempt"],
        actions=actions_high,
        enabled=True,
        auto_execute=True,
        requires_approval=False
    )
    
    playbook_critical = ResponsePlaybook(
        playbook_id=str(uuid.uuid4()),
        name="Critical Severity Default Playbook",
        description="Handles critical threats with comprehensive response",
        severity=ThreatSeverity.CRITICAL,
        threat_types=["exploit_attempt", "zero_day"],
        actions=actions_critical,
        enabled=True,
        auto_execute=False,
        requires_approval=True
    )
    
    return [playbook_low, playbook_medium, playbook_high, playbook_critical]
