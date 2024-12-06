"""API interface for logging system."""
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
import uvicorn
from .logger import AdvancedLogger
from .models import LogEntry, SearchQuery, HealthResponse

class LogAPI:
    def __init__(self, logger):
        self.app = FastAPI(
            title="Advanced Logger API",
            description="API for advanced logging system",
            version="1.0.0"
        )
        self.logger = logger
        self.start_time = datetime.now()
        self._setup_routes()

    def _setup_routes(self):
        @self.app.get("/health", response_model=HealthResponse)
        async def health_check():
            metrics = await self.logger.get_statistics(1)  # dernière heure
            uptime = (datetime.now() - self.start_time).total_seconds()
            
            return {
                "status": "healthy",
                "version": "1.0.0",
                "uptime": uptime,
                "metrics": {
                    "error_rate": metrics.get("error_rates", {}).get("total", 0),
                    "logs_last_hour": metrics.get("total_logs", 0),
                    "current_level": self.logger.log_level
                }
            }

        @self.app.post("/log", status_code=status.HTTP_201_CREATED)
        async def create_log(entry: LogEntry):
            try:
                await self.logger.log(
                    entry.level,
                    entry.user_id,
                    entry.action,
                    entry.description,
                    entry.component,
                    entry.metadata
                )
                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content={"status": "success", "message": "Log created"}
                )
            except Exception as e:
                print(f"Server error in create_log: {str(e)}")  # Debug print
                return JSONResponse(
                    status_code=status.HTTP_200_OK,  # On renvoie 200 au lieu de 500
                    content={
                        "status": "error",
                        "message": str(e)
                    }
                )

        @self.app.get("/logs")
        async def search_logs(
            query: Optional[str] = None,
            level: Optional[str] = None,
            start_time: Optional[datetime] = None,
            end_time: Optional[datetime] = None,
            limit: int = Query(default=100, le=1000)
        ):
            logs = self.logger.storage.search_logs(
                query=query,
                level=level,
                start_time=start_time,
                end_time=end_time
            )
            return {"logs": list(logs)[:limit]}

        @self.app.get("/metrics")
        async def get_metrics(
            hours: int = Query(default=24, ge=1, le=168)
        ):
            try:
                stats = await self.logger.get_statistics(hours)
                return stats
            except Exception as e:
                return {
                    "error": str(e),
                    "total_logs": 0,
                    "logs_by_level": {},
                    "error_rate": 0
                }


        @self.app.get("/level")
        def get_level():
            return {
                "current_level": self.logger.log_level,
                "available_levels": self.logger.LEVELS
            }

        @self.app.post("/level/{new_level}")
        def set_level(new_level: str):
            if new_level not in self.logger.LEVELS:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid log level. Must be one of: {', '.join(self.logger.LEVELS)}"
                )
            self.logger.set_level(new_level)
            return {"status": "success", "new_level": new_level}

        @self.app.get("/config")
        def get_config():
            return {
                "log_dir": str(self.logger.storage.log_dir),
                "rotation_size": self.logger.storage.rotation_size,
                "retention_days": self.logger.storage.retention_days,
                "default_level": self.logger.log_level,
                "service_name": self.logger.service_name
            }

        @self.app.post("/export")
        async def export_logs(
            format_type: str = "json",
            start_time: Optional[datetime] = None,
            end_time: Optional[datetime] = None
        ):
            try:
                file_path = await self.logger.export_logs(
                    format_type=format_type
                )
                return {"status": "success", "file": str(file_path)}
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.app.delete("/logs")
        async def cleanup_logs(
            days: int = Query(default=30, ge=1),
            confirm: bool = Query(default=False)
        ):
            if not confirm:
                raise HTTPException(
                    status_code=400,
                    detail="Confirmation required for log cleanup"
                )
            await self.logger.cleanup()
            return {"status": "success", "message": f"Logs older than {days} days cleaned up"}

    def run(self, host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
        uvicorn.run(self.app, host=host, port=port, reload=reload)
