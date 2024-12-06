import json
from datetime import datetime
from typing import Any

from starlette.responses import JSONResponse


def default_json_encoder(obj: Any) -> Any:
    if isinstance(obj, datetime):
        return obj.isoformat()
    return str(obj)


class AmsdalJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(',', ':'),
            default=default_json_encoder,
        ).encode('utf-8')
