import asyncio
from datetime import datetime
from brahmastra.models import ThreatEvent, ThreatSeverity
from brahmastra.engine import BrahmastraEngine
from brahmastra.playbooks import default_playbooks


async def main():
    # Initialize engine and register playbooks
    engine = BrahmastraEngine()
    playbooks = default_playbooks()
    for pb in playbooks:
        engine.register_playbook(pb)

    # Create a sample threat event (high severity)
    threat = ThreatEvent(
        event_id="ev123",
        timestamp=datetime.utcnow(),
        source_ip="10.0.0.5",
        target_ip="192.168.1.100",
        target_ports=[22, 80],
        severity=ThreatSeverity.HIGH,
        threat_type="intrusion",
        description="Suspicious intrusion detected"
    )

    # Handle the threat
    result = await engine.handle_threat(threat)

    # Print result summary
    print(f"Message: {result['message']}")
    print("Action results:")
    for res in result["results"]:
        print(f"  Action {res.action_id}: {res.status.value}, Success: {res.success}")


if __name__ == "__main__":
    asyncio.run(main())
