"""Core components for the logging system."""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any
from collections import defaultdict
import hashlib
import asyncio

@dataclass
class LogEvent:
    who: Dict[str, Any]
    what: Dict[str, Any]
    where: Dict[str, Any]
    why: Dict[str, Any]
    duration: float
    id: str
    metadata: Dict[str, Any]

class EventAggregator:
    def __init__(self, similarity_threshold: float = 0.85):
        self.event_groups = defaultdict(list)
        self.similarity_threshold = similarity_threshold
        self.lock = asyncio.Lock()

    def _compute_hash(self, event: LogEvent) -> str:
        key_parts = [
            str(event.what.get("action")),
            str(event.where.get("component")),
            str(event.why.get("description"))
        ]
        return hashlib.sha256("".join(key_parts).encode()).hexdigest()

    async def add_event(self, event: LogEvent) -> bool:
        event_hash = self._compute_hash(event)
        
        async with self.lock:
            if self._is_duplicate(event, event_hash):
                self.event_groups[event_hash].append(event)
                return False
            
            self.event_groups[event_hash] = [event]
            return True

    def _is_duplicate(self, event: LogEvent, event_hash: str) -> bool:
        if event_hash not in self.event_groups:
            return False
            
        recent_events = self.event_groups[event_hash][-10:]
        
        for recent in recent_events:
            time_diff = (event.when - recent.when).total_seconds()
            if time_diff < 60:  # Within 1 minute
                return True
        return False

class LogMetrics:
    def __init__(self):
        self.start_time = datetime.now()
        self.metrics = {
            "logs_by_level": defaultdict(int),
            "logs_by_component": defaultdict(int),
            "error_rates": defaultdict(float),
            "execution_times": defaultdict(list),
            "request_counts": defaultdict(int)
        }
        self.lock = asyncio.Lock()

    async def record_event(self, event: LogEvent):
        async with self.lock:
            level = event.what.get("level")
            component = event.where.get("component")
            action = event.what.get("action")
            
            self.metrics["logs_by_level"][level] += 1
            self.metrics["logs_by_component"][component] += 1
            self.metrics["request_counts"][action] += 1
            self.metrics["execution_times"][action].append(event.duration)

            if level == "ERROR":
                total = self.metrics["logs_by_component"][component]
                errors = self.metrics["logs_by_level"]["ERROR"]
                self.metrics["error_rates"][component] = (errors / total) * 100

    def get_metrics(self) -> Dict:
        return {
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            **self.metrics
        }

    async def save(self):
        # Pour une future implémentation de persistance des métriques
        pass

class LogSanitizer:
    def __init__(self, sensitive_fields: list):
        self.sensitive_fields = sensitive_fields

    def sanitize(self, data: Dict) -> Dict:
        if not isinstance(data, dict):
            return data

        sanitized = data.copy()
        for key, value in sanitized.items():
            if any(field in key.lower() for field in self.sensitive_fields):
                sanitized[key] = "***REDACTED***"
            elif isinstance(value, dict):
                sanitized[key] = self.sanitize(value)
            elif isinstance(value, list):
                sanitized[key] = [self.sanitize(item) if isinstance(item, dict) else item 
                                for item in value]
        return sanitized
