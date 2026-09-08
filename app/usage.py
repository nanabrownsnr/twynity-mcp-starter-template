from datetime import UTC, datetime
from logging import getLogger

import httpx

from app.config import settings

logger = getLogger(__name__)

async def save_usage_report(method: str, endpoint: str, auth_header: str | None) -> None:
    """Fire-and-forget usage report. Skips calls with no Authorization header."""
    if auth_header is None:
        return
    try:
        data = {
            "service": settings.SERVICE_ID,
            "method": method,
            "endpoint": endpoint,
            "timestamp": datetime.now(UTC).timestamp(),
        }
        headers = {"Authorization": auth_header}
        async with httpx.AsyncClient() as client:
            await client.post(settings.USAGE_REPORT_ENDPOINT, json=data, headers=headers)
    except Exception as e:
        logger.error(f"Usage report failed: {e}")