"""
Brahmastra Response Engine
Core orchestration logic for automated threat response
Save as: ~/chakravyuh/brahmastra/brahmastra/engine.py
"""

import asyncio
import uuid
from datetime import datetime
from typing import List, Dict, Optional

from brahmastra.models import (
    ThreatEvent, ResponseAction, ResponseResult, 
    ResponsePlaybook, ResponseStatus, ActionType
)


class BrahmastraEngine:
    def __init__(self):
        self.playbooks: List[ResponsePlaybook] = []
        self.executed_actions: Dict[str, ResponseResult] = {}
    
    def register_playbook(self, playbook: ResponsePlaybook):
        self.playbooks.append(playbook)
    
    def match_playbooks(self, event: ThreatEvent) -> List[ResponsePlaybook]:
        matched = []
        for pb in self.playbooks:
            if pb.enabled and pb.severity.value == event.severity.value and event.threat_type in pb.threat_types:
                matched.append(pb)
        return matched
    
    async def execute_action(self, action: ResponseAction) -> ResponseResult:
        result = ResponseResult(
            action_id=action.action_id,
            status=ResponseStatus.IN_PROGRESS,
            started_at=datetime.utcnow()
        )
        try:
            await asyncio.sleep(1)
            result.status = ResponseStatus.COMPLETED
            result.success = True
            result.completed_at = datetime.utcnow()
        except Exception as e:
            result.status = ResponseStatus.FAILED
            result.success = False
            result.error_message = str(e)
            result.completed_at = datetime.utcnow()
        return result
    
    async def execute_playbook(self, playbook: ResponsePlaybook) -> List[ResponseResult]:
        action_tasks = [self.execute_action(action) for action in playbook.actions]
        results = await asyncio.gather(*action_tasks)
        return results
    
    async def handle_threat(self, event: ThreatEvent) -> List[ResponseResult]:
        """
        Main handler for threat events
        Returns: List[ResponseResult] - NOT a dictionary
        """
        matched_playbooks = self.match_playbooks(event)
        if not matched_playbooks:
            return []
        
        all_results = []
        for pb in matched_playbooks:
            results = await self.execute_playbook(pb)
            all_results.extend(results)
        
        return all_results  # ✅ Returns list directly, NO dictionary wrapper
    
    def new_response_action(self, action_type: ActionType, target: str, parameters: Optional[Dict] = None, description: str = "") -> ResponseResult:
        return ResponseResult(
            action_id=str(uuid.uuid4()),
            action_type=action_type,
            target=target,
            parameters=parameters or {},
            description=description
        )
