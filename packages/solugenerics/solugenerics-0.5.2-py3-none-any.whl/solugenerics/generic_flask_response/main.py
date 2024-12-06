import json
from flask import Response


class GenericFlaskResponse:
    @classmethod
    def success(cls, data):
        return cls._create_response("success", data=data)

    @classmethod
    def error(cls, message):
        return cls._create_response("error", message=message)

    @staticmethod
    def _create_response(type, **kwargs):
        response = {"type": type}
        if type == "success":
            response["data"] = kwargs.get("data")
        elif type == "error":
            response["message"] = kwargs.get("message")
        return Response(
            json.dumps(response),
            status=200 if type == "success" else 500,
            mimetype="application/json",
        )
