import json
import logging

logger = logging.getLogger("steerer")


def log_action(
    action: str, alias: str, error_code: int, reason: str | None = None
) -> None:
    data: dict[str, str | int] = {
        "action": action,
        "alias": alias,
        "error_code": error_code,
    }
    if reason is not None:
        data["reason"] = reason
    logger.info(json.dumps(data))
