import json

from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def health(request):
    try:
        connection.ensure_connection()
        db_status = "ok"
    except Exception:
        db_status = "error"

    status = 200 if db_status == "ok" else 503
    return JsonResponse({"status": "ok" if status == 200 else "error", "db": db_status}, status=status)


@csrf_exempt
@require_POST
def login(request):
    try:
        data = json.loads(request.body)
        username = data.get("username", "mock_user")
    except Exception:
        username = "mock_user"

    return JsonResponse(
        {
            "access": "mock-access-token",
            "refresh": "mock-refresh-token",
            "user": {"id": 1, "username": username},
        }
    )


@csrf_exempt
@require_POST
def refresh(request):
    return JsonResponse(
        {
            "access": "mock-access-token-refreshed",
        }
    )
