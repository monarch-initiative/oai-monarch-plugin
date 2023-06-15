from fastapi import Request
from loguru import logger

class LoggingMiddleware:
    async def __call__(self, request: Request, call_next):
        logger.info({
            "event": "request",
            "endpoint": str(request.url.path),
            "origin": request.headers.get("origin", ""), 
            "openai-conversation-id": request.headers.get("openai-conversation-id", ""),
            "openai-ephemeral-user-id": request.headers.get("openai-ephemeral-user-id", ""),
            "query_params": dict(request.query_params),
            "path_params": dict(request.path_params),
        })
        
        response = await call_next(request)
        return response
