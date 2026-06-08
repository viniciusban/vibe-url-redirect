import json
import logging

logger = logging.getLogger("steerer")


def log_action(
    action: str,
    error_code: int = 0,
    reason: str | None = None,
    alias: str | None = None,
) -> None:
    data: dict[str, str | int] = {"action": action, "error_code": error_code}
    if alias is not None:
        data["alias"] = alias
    if reason is not None:
        data["reason"] = reason
    logger.info(json.dumps(data))
