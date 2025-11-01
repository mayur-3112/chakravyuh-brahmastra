"""
COMPLETE Unit tests for models.py
Tests all data structures and enums
Save this as: ~/chakravyuh/brahmastra/tests/test_models.py
"""
import unittest
from datetime import datetime
from brahmastra.models import (
    ThreatSeverity, ResponseStatus, ActionType,
    ThreatEvent, ResponseAction, ResponsePlaybook, ResponseResult
)

class TestEnums(unittest.TestCase):
    """Test all enum classes"""
    
    def test_threat_severity_values(self):
        """Test ThreatSeverity enum has all expected values"""
        self.assertEqual(ThreatSeverity.LOW.value, "low")
        self.assertEqual(ThreatSeverity.MEDIUM.value, "medium")
        self.assertEqual(ThreatSeverity.HIGH.value, "high")
        self.assertEqual(ThreatSeverity.CRITICAL.value, "critical")
    
    def test_response_status_values(self):
        """Test ResponseStatus enum"""
        self.assertEqual(ResponseStatus.PENDING.value, "pending")
        self.assertEqual(ResponseStatus.IN_PROGRESS.value, "in_progress")
        self.assertEqual(ResponseStatus.COMPLETED.value, "completed")
        self.assertEqual(ResponseStatus.FAILED.value, "failed")
        self.assertEqual(ResponseStatus.SKIPPED.value, "skipped")
    
    def test_action_type_values(self):
        """Test ActionType enum has security actions"""
        self.assertEqual(ActionType.ALERT.value, "alert")
        self.assertEqual(ActionType.BLOCK_IP.value, "block_ip")
        self.assertEqual(ActionType.LOG.value, "log")
        self.assertEqual(ActionType.BLOCK_PORT.value, "block_port")
        self.assertEqual(ActionType.ISOLATE_SERVICE.value, "isolate_service")
        self.assertEqual(ActionType.RATE_LIMIT.value, "rate_limit")

class TestThreatEvent(unittest.TestCase):
    """Test ThreatEvent dataclass"""
    
    def test_threat_event_creation(self):
        """Test creating a basic ThreatEvent"""
        event = ThreatEvent(
            event_id="test_001",
            timestamp=datetime.utcnow(),
            source_ip="192.168.1.100",
            target_ip="10.0.0.5",
            target_ports=[22, 80],
            severity=ThreatSeverity.HIGH,
            threat_type="intrusion",
            description="Test intrusion"
        )
        
        self.assertEqual(event.event_id, "test_001")
        self.assertEqual(event.severity, ThreatSeverity.HIGH)
        self.assertEqual(event.threat_type, "intrusion")
        self.assertEqual(len(event.target_ports), 2)
        self.assertIn(22, event.target_ports)
        self.assertIn(80, event.target_ports)
    
    def test_threat_event_optional_fields(self):
        """Test optional fields have correct defaults"""
        event = ThreatEvent(
            event_id="test_002",
            timestamp=datetime.utcnow(),
            source_ip="192.168.1.100",
            target_ip="10.0.0.5",
            target_ports=[],
            severity=ThreatSeverity.LOW,
            threat_type="port_scan",
            description="Test"
        )
        
        self.assertIsNone(event.scan_id)
        self.assertEqual(event.cve_ids, [])
        self.assertEqual(event.confidence_score, 0.0)
        self.assertEqual(event.metadata, {})
    
    def test_threat_event_with_cve_ids(self):
        """Test ThreatEvent with CVE IDs"""
        event = ThreatEvent(
            event_id="test_003",
            timestamp=datetime.utcnow(),
            source_ip="192.168.1.100",
            target_ip="10.0.0.5",
            target_ports=[443],
            severity=ThreatSeverity.CRITICAL,
            threat_type="exploit_attempt",
            description="CVE exploit",
            cve_ids=["CVE-2021-44228", "CVE-2022-12345"]
        )
        
        self.assertEqual(len(event.cve_ids), 2)
        self.assertIn("CVE-2021-44228", event.cve_ids)

class TestResponseAction(unittest.TestCase):
    """Test ResponseAction dataclass"""
    
    def test_response_action_creation(self):
        """Test creating a ResponseAction"""
        action = ResponseAction(
            action_id="act_001",
            action_type=ActionType.BLOCK_IP,
            target="192.168.1.100",
            parameters={"duration": "1h"},
            description="Block malicious IP"
        )
        
        self.assertEqual(action.action_id, "act_001")
        self.assertEqual(action.action_type, ActionType.BLOCK_IP)
        self.assertEqual(action.target, "192.168.1.100")
        self.assertEqual(action.parameters["duration"], "1h")
        self.assertEqual(action.priority, 5)  # default
        self.assertEqual(action.timeout, 30)  # default
    
    def test_response_action_with_priority(self):
        """Test ResponseAction with custom priority"""
        action = ResponseAction(
            action_id="act_002",
            action_type=ActionType.ALERT,
            target="security@company.com",
            parameters={"subject": "Critical Alert"},
            priority=1,  # High priority
            timeout=60,
            description="Send critical alert"
        )
        
        self.assertEqual(action.priority, 1)
        self.assertEqual(action.timeout, 60)
    
    def test_response_action_retry_settings(self):
        """Test ResponseAction retry settings"""
        action = ResponseAction(
            action_id="act_003",
            action_type=ActionType.BLOCK_IP,
            target="10.0.0.5",
            parameters={},
            max_retries=5
        )
        
        self.assertEqual(action.retry_count, 0)
        self.assertEqual(action.max_retries, 5)

class TestResponsePlaybook(unittest.TestCase):
    """Test ResponsePlaybook dataclass"""
    
    def test_playbook_creation(self):
        """Test creating a playbook with actions"""
        action = ResponseAction(
            action_id="act_001",
            action_type=ActionType.LOG,
            target="local",
            parameters={}
        )
        
        playbook = ResponsePlaybook(
            playbook_id="pb_001",
            name="Test Playbook",
            description="Test",
            severity=ThreatSeverity.LOW,
            threat_types=["port_scan"],
            actions=[action]
        )
        
        self.assertEqual(playbook.playbook_id, "pb_001")
        self.assertEqual(playbook.name, "Test Playbook")
        self.assertEqual(len(playbook.actions), 1)
        self.assertTrue(playbook.enabled)
        self.assertFalse(playbook.auto_execute)
        self.assertTrue(playbook.requires_approval)
    
    def test_playbook_multiple_actions(self):
        """Test playbook with multiple actions"""
        action1 = ResponseAction(
            action_id="act_001",
            action_type=ActionType.ALERT,
            target="admin@company.com",
            parameters={}
        )
        
        action2 = ResponseAction(
            action_id="act_002",
            action_type=ActionType.BLOCK_IP,
            target="192.168.1.100",
            parameters={}
        )
        
        playbook = ResponsePlaybook(
            playbook_id="pb_002",
            name="Multi-Action Playbook",
            description="Multiple actions",
            severity=ThreatSeverity.HIGH,
            threat_types=["intrusion", "exploit"],
            actions=[action1, action2]
        )
        
        self.assertEqual(len(playbook.actions), 2)
        self.assertEqual(playbook.actions[0].action_type, ActionType.ALERT)
        self.assertEqual(playbook.actions[1].action_type, ActionType.BLOCK_IP)
    
    def test_playbook_disabled(self):
        """Test disabled playbook"""
        playbook = ResponsePlaybook(
            playbook_id="pb_003",
            name="Disabled Playbook",
            description="Disabled",
            severity=ThreatSeverity.MEDIUM,
            threat_types=["recon"],
            actions=[],
            enabled=False
        )
        
        self.assertFalse(playbook.enabled)

class TestResponseResult(unittest.TestCase):
    """Test ResponseResult dataclass"""
    
    def test_response_result_creation(self):
        """Test creating ResponseResult"""
        start_time = datetime.utcnow()
        
        result = ResponseResult(
            action_id="act_001",
            status=ResponseStatus.IN_PROGRESS,
            started_at=start_time
        )
        
        self.assertEqual(result.action_id, "act_001")
        self.assertEqual(result.status, ResponseStatus.IN_PROGRESS)
        self.assertEqual(result.started_at, start_time)
        self.assertFalse(result.success)
        self.assertIsNone(result.completed_at)
    
    def test_response_result_completed(self):
        """Test completed ResponseResult"""
        start_time = datetime.utcnow()
        end_time = datetime.utcnow()
        
        result = ResponseResult(
            action_id="act_002",
            status=ResponseStatus.COMPLETED,
            started_at=start_time,
            completed_at=end_time,
            success=True
        )
        
        self.assertEqual(result.status, ResponseStatus.COMPLETED)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.completed_at)
    
    def test_response_result_failed(self):
        """Test failed ResponseResult"""
        result = ResponseResult(
            action_id="act_003",
            status=ResponseStatus.FAILED,
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
            success=False,
            error_message="Connection timeout"
        )
        
        self.assertEqual(result.status, ResponseStatus.FAILED)
        self.assertFalse(result.success)
        self.assertEqual(result.error_message, "Connection timeout")

if __name__ == '__main__':
    unittest.main()
