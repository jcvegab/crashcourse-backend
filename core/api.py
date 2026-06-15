from django.db import connection
from ninja import NinjaAPI, Schema

api = NinjaAPI(title="CrashCourse API", version="0.1.0")


class HealthOut(Schema):
    status: str
    db: str


class LoginIn(Schema):
    username: str = "mock_user"
    password: str = ""


class UserOut(Schema):
    id: int
    username: str


class LoginOut(Schema):
    access: str
    refresh: str
    user: UserOut


class RefreshOut(Schema):
    access: str


@api.get("", url_name="api-root")
def api_root(request):
    return {"message": "CrashCourse API", "version": api.version}


@api.get("/health/", response=HealthOut, url_name="health")
def health(request):
    try:
        connection.ensure_connection()
        db_status = "ok"
    except Exception:
        db_status = "error"

    return {"status": "ok" if db_status == "ok" else "error", "db": db_status}


@api.post("/auth/login/", response=LoginOut, url_name="auth-login")
def login(request, data: LoginIn):
    return {
        "access": "mock-access-token",
        "refresh": "mock-refresh-token",
        "user": {"id": 1, "username": data.username},
    }


@api.post("/auth/refresh/", response=RefreshOut, url_name="auth-refresh")
def refresh(request):
    return {
        "access": "mock-access-token-refreshed",
    }
