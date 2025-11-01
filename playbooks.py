import uuid
from brahmastra.models import (
    ResponsePlaybook, ResponseAction,
    ThreatSeverity, ActionType
)


def default_playbooks():
    """Create default playbooks with actions for testing"""
    
    actions_low = [
        ResponseAction(
            action_id=str(uuid.uuid4()),
            action_type=ActionType.LOG,
            target="local",
            parameters={"message": "Low severity threat logged"},
            description="Log low severity threat"
        ),
    ]

    actions_high = [
        ResponseAction(
            action_id=str(uuid.uuid4()),
            action_type=ActionType.ALERT,
            target="security-team@example.com",
            parameters={"email_subject": "High severity alert"},
            description="Send high severity alert email"
        ),
        ResponseAction(
            action_id=str(uuid.uuid4()),
            action_type=ActionType.BLOCK_IP,
            target="192.168.1.0/24",
            parameters={"duration": "1 hour"},
            description="Block IP range for 1 hour"
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
        requires_approval=False,
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
        requires_approval=True,
    )

    return [playbook_low, playbook_high]
