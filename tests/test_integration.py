"""
Integration tests for Brahmastra Response Engine
Tests complete threat response workflow end-to-end
Save as: ~/chakravyuh/brahmastra/tests/test_integration.py
"""

import unittest
import asyncio
from datetime import datetime
from brahmastra.engine import BrahmastraEngine
from brahmastra.models import (
    ThreatEvent, ThreatSeverity, ActionType,
    ResponsePlaybook, ResponseAction, ResponseStatus
)
from brahmastra.playbooks import default_playbooks


class TestEndToEndWorkflow(unittest.TestCase):
    """Test complete threat response workflow"""
    
    def setUp(self):
        """Set up engine with default playbooks"""
        self.engine = BrahmastraEngine()
        
        # Register default playbooks
        for playbook in default_playbooks():
            self.engine.register_playbook(playbook)
    
    def test_port_scan_response(self):
        """Test complete response to port scan threat"""
        # Create port scan threat event
        event = ThreatEvent(
            event_id="test_port_scan_001",
            timestamp=datetime.utcnow(),
            source_ip="192.168.1.100",
            target_ip="10.0.0.5",
            target_ports=[22, 80, 443, 8080],
            severity=ThreatSeverity.LOW,
            threat_type="port_scan",
            description="Systematic port scan detected",
            confidence_score=0.85
        )
        
        # Execute response
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(
            self.engine.handle_threat(event)
        )
        
        # Verify response executed
        self.assertGreater(len(results), 0)
        
        # Verify all actions completed
        for result in results:
            self.assertEqual(result.status, ResponseStatus.COMPLETED)
            self.assertTrue(result.success)
            self.assertIsNotNone(result.completed_at)
    
    def test_intrusion_response(self):
        """Test complete response to intrusion threat"""
        event = ThreatEvent(
            event_id="test_intrusion_001",
            timestamp=datetime.utcnow(),
            source_ip="203.0.113.45",
            target_ip="10.0.0.10",
            target_ports=[22],
            severity=ThreatSeverity.HIGH,
            threat_type="intrusion",
            description="Unauthorized SSH access attempt",
            confidence_score=0.95
        )
        
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(
            self.engine.handle_threat(event)
        )
        
        # High severity should trigger multiple actions
        self.assertGreater(len(results), 1)
        
        # Verify blocking action executed - check for 'block' in action_id
        action_ids = [r.action_id for r in results]
        has_block_action = any('block' in aid.lower() for aid in action_ids)
        self.assertTrue(has_block_action, f"Expected blocking action in results. Got: {action_ids}")
    
    def test_exploit_response(self):
        """Test response to exploit attempt with CVEs"""
        event = ThreatEvent(
            event_id="test_exploit_001",
            timestamp=datetime.utcnow(),
            source_ip="198.51.100.89",
            target_ip="10.0.0.15",
            target_ports=[443],
            severity=ThreatSeverity.CRITICAL,
            threat_type="exploit_attempt",
            description="Log4Shell exploitation attempt",
            cve_ids=["CVE-2021-44228"],
            confidence_score=0.98
        )
        
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(
            self.engine.handle_threat(event)
        )
        
        # Critical severity should trigger comprehensive response
        self.assertGreaterEqual(len(results), 2)
        
        # All critical actions should succeed
        for result in results:
            self.assertTrue(result.success)


class TestPlaybookMatching(unittest.TestCase):
    """Test playbook matching logic"""
    
    def setUp(self):
        self.engine = BrahmastraEngine()
        
        # Register playbooks
        for playbook in default_playbooks():
            self.engine.register_playbook(playbook)
    
    def test_severity_matching(self):
        """Test playbook matches by severity"""
        low_event = ThreatEvent(
            event_id="test_low",
            timestamp=datetime.utcnow(),
            source_ip="1.1.1.1",
            target_ip="2.2.2.2",
            target_ports=[80],
            severity=ThreatSeverity.LOW,
            threat_type="port_scan",
            description="Test"
        )
        
        matched = self.engine.match_playbooks(low_event)
        
        # Should match at least one playbook
        self.assertGreater(len(matched), 0)
        
        # All matched playbooks should handle LOW severity
        for playbook in matched:
            self.assertEqual(playbook.severity, ThreatSeverity.LOW)
    
    def test_threat_type_matching(self):
        """Test playbook matches by threat type"""
        intrusion_event = ThreatEvent(
            event_id="test_intrusion",
            timestamp=datetime.utcnow(),
            source_ip="1.1.1.1",
            target_ip="2.2.2.2",
            target_ports=[22],
            severity=ThreatSeverity.HIGH,
            threat_type="intrusion",
            description="Test"
        )
        
        matched = self.engine.match_playbooks(intrusion_event)
        
        self.assertGreater(len(matched), 0)
        
        # All matched playbooks should handle intrusion
        for playbook in matched:
            self.assertIn("intrusion", playbook.threat_types)
    
    def test_no_match_for_disabled_playbook(self):
        """Test disabled playbooks are not matched"""
        # Create and register disabled playbook
        disabled_playbook = ResponsePlaybook(
            playbook_id="pb_disabled",
            name="Disabled Test",
            description="Should not match",
            severity=ThreatSeverity.LOW,
            threat_types=["port_scan"],
            actions=[],
            enabled=False
        )
        
        self.engine.register_playbook(disabled_playbook)
        
        event = ThreatEvent(
            event_id="test_event",
            timestamp=datetime.utcnow(),
            source_ip="1.1.1.1",
            target_ip="2.2.2.2",
            target_ports=[80],
            severity=ThreatSeverity.LOW,
            threat_type="port_scan",
            description="Test"
        )
        
        matched = self.engine.match_playbooks(event)
        
        # Disabled playbook should not be in matched results
        matched_ids = [p.playbook_id for p in matched]
        self.assertNotIn("pb_disabled", matched_ids)


class TestConcurrentThreats(unittest.TestCase):
    """Test handling multiple threats concurrently"""
    
    def setUp(self):
        self.engine = BrahmastraEngine()
        for playbook in default_playbooks():
            self.engine.register_playbook(playbook)
    
    def test_multiple_threats_parallel(self):
        """Test handling multiple threats in parallel"""
        events = [
            ThreatEvent(
                event_id=f"test_concurrent_{i}",
                timestamp=datetime.utcnow(),
                source_ip=f"192.168.1.{i}",
                target_ip="10.0.0.5",
                target_ports=[22, 80],
                severity=ThreatSeverity.MEDIUM,  # Changed to MEDIUM (now exists)
                threat_type="port_scan",
                description=f"Concurrent threat {i}"
            )
            for i in range(5)
        ]
        
        async def handle_all():
            tasks = [self.engine.handle_threat(event) for event in events]
            return await asyncio.gather(*tasks)
        
        loop = asyncio.get_event_loop()
        all_results = loop.run_until_complete(handle_all())
        
        # All threats should be handled
        self.assertEqual(len(all_results), 5)
        
        # Each should have results
        for results in all_results:
            self.assertGreater(len(results), 0)


class TestErrorHandling(unittest.TestCase):
    """Test error handling in response execution"""
    
    def setUp(self):
        self.engine = BrahmastraEngine()
    
    def test_invalid_threat_type(self):
        """Test handling of threat with no matching playbook"""
        event = ThreatEvent(
            event_id="test_invalid",
            timestamp=datetime.utcnow(),
            source_ip="1.1.1.1",
            target_ip="2.2.2.2",
            target_ports=[],
            severity=ThreatSeverity.LOW,
            threat_type="unknown_threat_type",
            description="Test unknown threat"
        )
        
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(
            self.engine.handle_threat(event)
        )
        
        # Should return empty list for no matches
        self.assertEqual(len(results), 0)
    
    def test_empty_actions_playbook(self):
        """Test playbook with no actions"""
        empty_playbook = ResponsePlaybook(
            playbook_id="pb_empty",
            name="Empty Playbook",
            description="No actions",
            severity=ThreatSeverity.LOW,
            threat_types=["test_empty"],
            actions=[]
        )
        
        self.engine.register_playbook(empty_playbook)
        
        event = ThreatEvent(
            event_id="test_empty",
            timestamp=datetime.utcnow(),
            source_ip="1.1.1.1",
            target_ip="2.2.2.2",
            target_ports=[],
            severity=ThreatSeverity.LOW,
            threat_type="test_empty",
            description="Test"
        )
        
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(
            self.engine.handle_threat(event)
        )
        
        # Empty playbook should return no results
        self.assertEqual(len(results), 0)


if __name__ == '__main__':
    unittest.main()
