import json

from flask import Response


def problem(status, title, type=None, detail=None, instance=None, **kwargs) -> Response:
    body = kwargs
    body["status"] = status
    body["title"] = title

    if type:
        body["type"] = type
    if detail:
        body["detail"] = detail
    if instance:
        body["instance"] = instance

    headers = {}

    return Response(
        # body,
        json.dumps(body, indent=2) + "\n",
        status,
        headers,
        mimetype="application/problem+json",
    )
