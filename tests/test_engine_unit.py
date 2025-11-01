"""
Unit tests for engine.py
Tests BrahmastraEngine methods individually
Save this as: ~/chakravyuh/brahmastra/tests/test_engine_unit.py
"""
import unittest
import asyncio
from datetime import datetime
from brahmastra.engine import BrahmastraEngine
from brahmastra.models import (
    ThreatEvent, ThreatSeverity,
    ResponsePlaybook, ResponseAction, ActionType
)

class TestEngineInitialization(unittest.TestCase):
    """Test engine initialization"""
    
    def test_engine_creation(self):
        """Test creating BrahmastraEngine"""
        engine = BrahmastraEngine()
        self.assertEqual(len(engine.playbooks), 0)
        self.assertIsInstance(engine.executed_actions, dict)

class TestPlaybookRegistration(unittest.TestCase):
    """Test playbook registration"""
    
    def setUp(self):
        self.engine = BrahmastraEngine()
        self.playbook = ResponsePlaybook(
            playbook_id="pb_test",
            name="Test Playbook",
            description="Test",
            severity=ThreatSeverity.LOW,
            threat_types=["test"],
            actions=[]
        )
    
    def test_register_single_playbook(self):
        """Test registering one playbook"""
        self.engine.register_playbook(self.playbook)
        self.assertEqual(len(self.engine.playbooks), 1)
    
    def test_register_multiple_playbooks(self):
        """Test registering multiple playbooks"""
        playbook2 = ResponsePlaybook(
            playbook_id="pb_test2",
            name="Test Playbook 2",
            description="Test 2",
            severity=ThreatSeverity.HIGH,
            threat_types=["test2"],
            actions=[]
        )
        
        self.engine.register_playbook(self.playbook)
        self.engine.register_playbook(playbook2)
        self.assertEqual(len(self.engine.playbooks), 2)

class TestPlaybookMatching(unittest.TestCase):
    """Test playbook matching logic"""
    
    def setUp(self):
        self.engine = BrahmastraEngine()
        
        # Create LOW severity playbook
        self.playbook_low = ResponsePlaybook(
            playbook_id="pb_low",
            name="Low Severity",
            description="Handles low threats",
            severity=ThreatSeverity.LOW,
            threat_types=["port_scan", "recon"],
            actions=[]
        )
        
        # Create HIGH severity playbook
        self.playbook_high = ResponsePlaybook(
            playbook_id="pb_high",
            name="High Severity",
            description="Handles high threats",
            severity=ThreatSeverity.HIGH,
            threat_types=["intrusion", "exploit"],
            actions=[]
        )
        
        self.engine.register_playbook(self.playbook_low)
        self.engine.register_playbook(self.playbook_high)
    
    def test_match_low_severity(self):
        """Test matching LOW severity event"""
        event = ThreatEvent(
            event_id="ev_001",
            timestamp=datetime.utcnow(),
            source_ip="1.1.1.1",
            target_ip="2.2.2.2",
            target_ports=[22],
            severity=ThreatSeverity.LOW,
            threat_type="port_scan",
            description="Test"
        )
        
        matched = self.engine.match_playbooks(event)
        self.assertEqual(len(matched), 1)
        self.assertEqual(matched[0].playbook_id, "pb_low")
    
    def test_match_high_severity(self):
        """Test matching HIGH severity event"""
        event = ThreatEvent(
            event_id="ev_002",
            timestamp=datetime.utcnow(),
            source_ip="1.1.1.1",
            target_ip="2.2.2.2",
            target_ports=[80],
            severity=ThreatSeverity.HIGH,
            threat_type="intrusion",
            description="Test"
        )
        
        matched = self.engine.match_playbooks(event)
        self.assertEqual(len(matched), 1)
        self.assertEqual(matched[0].playbook_id, "pb_high")
    
    def test_no_match_for_unknown_threat(self):
        """Test no match for unknown threat type"""
        event = ThreatEvent(
            event_id="ev_003",
            timestamp=datetime.utcnow(),
            source_ip="1.1.1.1",
            target_ip="2.2.2.2",
            target_ports=[],
            severity=ThreatSeverity.LOW,
            threat_type="unknown_type",
            description="Test"
        )
        
        matched = self.engine.match_playbooks(event)
        self.assertEqual(len(matched), 0)
    
    def test_disabled_playbook_not_matched(self):
        """Test disabled playbooks are not matched"""
        self.playbook_low.enabled = False
        
        event = ThreatEvent(
            event_id="ev_004",
            timestamp=datetime.utcnow(),
            source_ip="1.1.1.1",
            target_ip="2.2.2.2",
            target_ports=[22],
            severity=ThreatSeverity.LOW,
            threat_type="port_scan",
            description="Test"
        )
        
        matched = self.engine.match_playbooks(event)
        self.assertEqual(len(matched), 0)

if __name__ == '__main__':
    unittest.main()

