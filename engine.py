import asyncio
from datetime import datetime
from typing import List, Dict, Optional
from brahmastra.models import (
    ThreatEvent, ResponsePlaybook, ResponseAction,
    ResponseResult, ResponseStatus
)

class BrahmastraEngine:
    def __init__(self):
        self.playbooks: Dict[str, ResponsePlaybook] = {}

    def register_playbook(self, playbook: ResponsePlaybook) -> None:
        self.playbooks[playbook.playbook_id] = playbook

    def match_playbooks(self, event: ThreatEvent) -> List[ResponsePlaybook]:
        matched = []
        for playbook in self.playbooks.values():
            if not playbook.enabled:
                continue
            if playbook.severity != event.severity:
                continue
            if event.threat_type not in playbook.threat_types:
                continue
            matched.append(playbook)
        return matched

   async def handle_threat(self, event: ThreatEvent) -> List[ResponseResult]:
    matched_playbooks = self.match_playbooks(event)
    all_results = []
    for pb in matched_playbooks:
        results = await self.execute_playbook(pb)
        print(f"DEBUG (handle_threat): playbook {pb.name} produced results {results}")
        all_results.extend(results)
    print(f"DEBUG (handle_threat): returning {all_results}")
    return all_results


    async def execute_playbook(self, playbook: ResponsePlaybook) -> List[ResponseResult]:
    	if not playbook.actions:
        	print(f"DEBUG: No actions for playbook {playbook.name}, returning []")
       		 return []
    print(f"DEBUG: actions = {playbook.actions}")
    action_tasks = [self.execute_action(action) for action in playbook.actions]
    results = await asyncio.gather(*action_tasks)
    print(f"DEBUG: results = {results}")  # <---- add this
    return list(results)


    async def execute_action(self, action: ResponseAction) -> ResponseResult:
        # Always return a ResponseResult object (never string)
        result = ResponseResult(
            action_id=action.action_id,
            status=ResponseStatus.IN_PROGRESS,
            started_at=datetime.utcnow()
        )
        try:
            await asyncio.sleep(0.1)
            result.status = ResponseStatus.COMPLETED
            result.success = True
            result.completed_at = datetime.utcnow()
        except Exception as e:
            result.status = ResponseStatus.FAILED
            result.success = False
            result.error_message = str(e)
            result.completed_at = datetime.utcnow()
        return result
