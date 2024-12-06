"""Main logger implementation with ULID support."""
import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, Optional
import json
from pathlib import Path
from rich.console import Console
from rich.text import Text
from .config import LogConfig
from .core import LogEvent, EventAggregator, LogMetrics, LogSanitizer
from .storage import LogStorage
from .ulid import ULID

class AdvancedLogger:
    LEVELS = ["DEBUG", "INFO", "WARN", "ERROR", "FATAL"]
    COLORS = {
        "DEBUG": "cyan",
        "INFO": "green", 
        "WARN": "yellow",
        "ERROR": "red",
        "FATAL": "bold red",
    }
    DISPLAY_FORMATS = ["SHORT", "FULL", "DETAILED"]

    def __init__(self, service_name: str, config_path: Optional[str] = None, display_format: str = "SHORT"):
        self._cleanup_task = None
        self.console = Console()
        self.config = LogConfig(config_path)
        self.service_name = service_name
        self.display_format = display_format.upper()
        if self.display_format not in self.DISPLAY_FORMATS:
            self.display_format = "SHORT"
        
        self.storage = LogStorage(
            Path(self.config.config["log_dir"]),
            self.config.config["rotation_size"],
            self.config.config["retention_days"]
        )
        
        self.aggregator = EventAggregator(
            self.config.config["similarity_threshold"]
        )
        
        self.metrics = LogMetrics() if self.config.config["metrics_enabled"] else None
        self.sanitizer = LogSanitizer(self.config.config["sensitive_fields"])
            
        self.log_level = self.config.config["default_level"]
        self._cleanup_task = asyncio.create_task(self._periodic_cleanup())

    def _display_console(self, level: str, user_id: str, action: str, description: str, event: LogEvent = None):
        try:
            if self.display_format == "FULL":
                self.console.print(json.dumps(event.__dict__, default=str))
                return

            # Format court ou détaillé
            timestamp = datetime.now()
            if event and event.id:
                # Utilisation de from_str et datetime de notre classe ULID
                ulid_obj = ULID.from_str(event.id)
                timestamp = ulid_obj.datetime()

            if self.display_format == "DETAILED":
                text = Text.assemble(
                    (f"[{level}] ", self.COLORS.get(level, "white")),
                    (f"Date: {timestamp.strftime('%Y-%m-%d %H:%M:%S')} | ", "bold white"),
                    ("User: ", "bold"),
                    (user_id, "italic"),
                    (" | Action: ", "bold"),
                    (action, "bold cyan"),
                    (" | Description: ", "bold"),
                    (description, self.COLORS.get(level, "white")),
                    (" | ID: ", "bold"),
                    (str(event.id) if event else "", "dim white")
                )
            else:  # SHORT
                text = Text.assemble(
                    (f"[{level}] ", self.COLORS.get(level, "white")),
                    ("User: ", "bold"),
                    (user_id, "italic"),
                    (" | Action: ", "bold"),
                    (action, "bold cyan"),
                    (" | Description: ", "bold"),
                    (description, self.COLORS.get(level, "white"))
                )
            
            self.console.print(text)
        except Exception as e:
            print(f"Display error: {str(e)}")

    async def log(self, level: str, user_id: str, action: str, description: str, 
                component: str, metadata: Optional[Dict] = None) -> None:
        try:
            if not self._should_log(level) or level not in self.LEVELS:
                return

            start_time = time.time()
            metadata = self.sanitizer.sanitize(metadata or {})
            
            log_id = str(ULID.generate())
            
            event = LogEvent(
                who={
                    "user_id": user_id,
                    "service": self.service_name
                },
                what={
                    "action": action,
                    "level": level
                },
                where={
                    "component": component,
                    "endpoint": metadata.get("endpoint", "unknown")
                },
                why={
                    "description": description,
                    "context": metadata.get("context", {})
                },
                duration=time.time() - start_time,
                id=log_id,
                metadata=metadata
            )

            self._display_console(level, user_id, action, description, event)

            if self.metrics:
                await self.metrics.record_event(event)

            await self.storage.write_log(event.__dict__)

        except Exception as e:
            self.console.print(f"[FATAL] Logging error: {str(e)}", style="bold red")
            raise

    def _should_log(self, level: str) -> bool:
        try:
            return self.LEVELS.index(level) >= self.LEVELS.index(self.log_level)
        except ValueError:
            return False

    async def _periodic_cleanup(self):
        while True:
            try:
                await asyncio.sleep(24 * 3600)
                await self.storage.cleanup_old_logs()
            except Exception as e:
                self.console.print(f"[FATAL] Cleanup error: {str(e)}", style="bold red")

    def set_level(self, level: str):
        if level in self.LEVELS:
            self.log_level = level
            self._display_console("INFO", "system", "config", f"Log level changed to {level}")

    async def close(self):
        try:
            if self._cleanup_task:
                self._cleanup_task.cancel()
                try:
                    await self._cleanup_task
                except asyncio.CancelledError:
                    pass
                
            if self.metrics:
                await self.metrics.save()
        except Exception as e:
            self.console.print(f"[FATAL] Close error: {str(e)}", style="bold red")

    async def cleanup(self):
        try:
            await self.storage.cleanup_old_logs()
            await self.close()
        except Exception as e:
            self.console.print(f"[FATAL] Cleanup error: {str(e)}", style="bold red")

    def __del__(self):
        if self._cleanup_task and not self._cleanup_task.done():
            asyncio.create_task(self.close())

    async def export_logs(self, format_type: str = "json", target_file: Optional[str] = None):
        try:
            if not target_file:
                target_file = f"logs_export_{datetime.now().strftime('%Y%m%d%H%M%S')}.{format_type}"
                
            logs = list(self.storage.search_logs())
            
            if format_type == "json":
                with open(target_file, 'w') as f:
                    json.dump(logs, f, indent=2, default=str)
            else:
                raise ValueError(f"Unsupported format: {format_type}")
                
            return target_file
        except Exception as e:
            self.console.print(f"[FATAL] Export error: {str(e)}", style="bold red")
            raise

    async def get_statistics(self, timeframe_hours: int = 24) -> Dict:
        try:
            stats = {
                "total_logs": 0,
                "logs_by_level": {},
                "error_rate": 0
            }
            
            logs = await self.storage.search_logs(
                start_time=datetime.now() - timedelta(hours=timeframe_hours)
            )
            
            total = 0
            errors = 0
            level_counts = {}
            
            for log in logs:
                total += 1
                level = log["what"]["level"]
                level_counts[level] = level_counts.get(level, 0) + 1
                if level == "ERROR":
                    errors += 1
            
            stats["total_logs"] = total
            stats["logs_by_level"] = level_counts
            stats["error_rate"] = (errors / total * 100) if total > 0 else 0
            
            return stats
        except Exception as e:
            self.console.print(f"[FATAL] Stats error: {str(e)}", style="bold red")
            return {"error": str(e)}

from .api import LogAPI