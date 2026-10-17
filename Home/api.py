"""Token-protected JSON API for managing Services and Solutions.

Auth:   Authorization: Bearer <API_TOKEN>   (API_TOKEN comes from the environment;
        if it is not set the API is disabled and every call returns 503)
Base:   /api/v1/

    GET    /api/v1/services/              list
    POST   /api/v1/services/              create, or update if `name` already exists (upsert)
    GET    /api/v1/services/<id>/         read one
    PUT    /api/v1/services/<id>/         replace   (PATCH = partial update)
    DELETE /api/v1/services/<id>/         delete

    GET    /api/v1/solutions/             list (add ?all=1 to include inactive)
    POST   /api/v1/solutions/             create, or update if `slug` exists (upsert)
    GET    /api/v1/solutions/<slug>/      read one
    PUT    /api/v1/solutions/<slug>/      replace   (PATCH = partial update)
    DELETE /api/v1/solutions/<slug>/      delete

Saves go through the ORM, so the existing signals clear the home / solutions caches.
"""
import hmac
import json
import re

from django.conf import settings
from django.http import JsonResponse
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Solution, TechServices

ICON_HTML_RE = re.compile(r'^<i class="[A-Za-z0-9 _-]{1,80}"></i>$')
ICON_CLASS_RE = re.compile(r'^fa-[a-z0-9-]{1,45}$')


class ApiError(Exception):
    def __init__(self, message, status=400, errors=None):
        super().__init__(message)
        self.status = status
        self.errors = errors


def _json(data, status=200):
    return JsonResponse(data, status=status, json_dumps_params={"ensure_ascii": False})


def api_view(view):
    """Auth + JSON error handling + csrf exemption (bearer tokens aren't cookie-based)."""
    @csrf_exempt
    def wrapper(request, *args, **kwargs):
        token = getattr(settings, "API_TOKEN", "")
        if not token:
            return _json({"error": "API disabled: API_TOKEN is not configured"}, 503)
        header = request.headers.get("Authorization", "")
        supplied = header[7:].strip() if header.lower().startswith("bearer ") else ""
        if not supplied or not hmac.compare_digest(supplied.encode(), token.encode()):
            resp = _json({"error": "Invalid or missing bearer token"}, 401)
            resp["WWW-Authenticate"] = "Bearer"
            return resp
        try:
            return view(request, *args, **kwargs)
        except ApiError as exc:
            body = {"error": str(exc)}
            if exc.errors:
                body["fields"] = exc.errors
            return _json(body, exc.status)
    wrapper.__name__ = view.__name__
    return wrapper


def _body(request):
    try:
        data = json.loads(request.body.decode() or "{}")
    except (ValueError, UnicodeDecodeError):
        raise ApiError("Request body must be valid JSON")
    if not isinstance(data, dict):
        raise ApiError("Request body must be a JSON object")
    return data


def _clean(data, spec, partial):
    """spec: {field: (required, max_len, validator|None, error_text)}"""
    out, errors = {}, {}
    unknown = set(data) - set(spec)
    if unknown:
        raise ApiError("Unknown field(s): " + ", ".join(sorted(unknown)))
    for field, (required, max_len, validator, err) in spec.items():
        if field not in data:
            if required and not partial:
                errors[field] = "This field is required"
            continue
        value = data[field]
        if not isinstance(value, str):
            errors[field] = "Must be a string"
            continue
        value = value.strip()
        if required and not value:
            errors[field] = "This field cannot be empty"
        elif max_len and len(value) > max_len:
            errors[field] = f"Max {max_len} characters"
        elif validator and value and not validator.match(value):
            errors[field] = err
        else:
            out[field] = value
    if errors:
        raise ApiError("Validation failed", 422, errors)
    return out


def _int(data, out, field, errors):
    if field in data:
        if isinstance(data[field], bool) or not isinstance(data[field], int):
            errors[field] = "Must be an integer"
        else:
            out[field] = data[field]


def _bool(data, out, field, errors):
    if field in data:
        if not isinstance(data[field], bool):
            errors[field] = "Must be true or false"
        else:
            out[field] = data[field]


# ---------------------------------------------------------------- services
SERVICE_SPEC = {
    "name": (True, 100, None, ""),
    "description": (True, 2000, None, ""),
    "icon": (True, 200, ICON_HTML_RE, 'Must look like <i class="fas fa-video"></i>'),
}


def _service_out(s):
    return {"id": s.id, "name": s.name, "description": s.description, "icon": s.icon,
            "created_at": s.created_at.isoformat(), "updated_at": s.updated_at.isoformat()}


@api_view
@require_http_methods(["GET", "POST"])
def services_collection(request):
    if request.method == "GET":
        return _json({"results": [_service_out(s) for s in TechServices.objects.all()]})
    fields = _clean(_body(request), SERVICE_SPEC, partial=False)
    existing = TechServices.objects.filter(name__iexact=fields["name"]).first()
    if existing:
        for k, v in fields.items():
            setattr(existing, k, v)
        existing.save()
        return _json(_service_out(existing), 200)
    return _json(_service_out(TechServices.objects.create(**fields)), 201)


@api_view
@require_http_methods(["GET", "PUT", "PATCH", "DELETE"])
def service_item(request, pk):
    try:
        obj = TechServices.objects.get(pk=pk)
    except TechServices.DoesNotExist:
        raise ApiError("Service not found", 404)
    if request.method == "GET":
        return _json(_service_out(obj))
    if request.method == "DELETE":
        obj.delete()
        return _json({"deleted": pk})
    fields = _clean(_body(request), SERVICE_SPEC, partial=request.method == "PATCH")
    if "name" in fields and TechServices.objects.filter(name__iexact=fields["name"]).exclude(pk=pk).exists():
        raise ApiError("Validation failed", 422, {"name": "Another service already has this name"})
    for k, v in fields.items():
        setattr(obj, k, v)
    obj.save()
    return _json(_service_out(obj))


# --------------------------------------------------------------- solutions
SOLUTION_SPEC = {
    "slug": (False, 50, re.compile(r"^[-a-z0-9_]+$"), "Lowercase letters, numbers, - and _ only"),
    "title": (True, 100, None, ""),
    "short_description": (True, 200, None, ""),
    "detailed_description": (True, 5000, None, ""),
    "icon_class": (True, 50, ICON_CLASS_RE, "Must look like fa-video"),
    "features": (True, 3000, None, ""),
    "cta_text": (False, 50, None, ""),
    "cta_link": (False, 200, None, ""),
}


def _solution_out(s):
    return {"slug": s.slug, "title": s.title, "short_description": s.short_description,
            "detailed_description": s.detailed_description, "icon_class": s.icon_class,
            "features": s.get_features_list(), "cta_text": s.cta_text, "cta_link": s.cta_link,
            "z_index": s.z_index, "display_order": s.display_order, "is_active": s.is_active,
            "url": s.get_absolute_url(),
            "created_at": s.created_at.isoformat(), "updated_at": s.updated_at.isoformat()}


SOLUTION_EXTRAS = ("z_index", "display_order", "is_active")


def _solution_fields(data, partial):
    features = data.get("features")
    if isinstance(features, list):  # accept a JSON list; stored newline-separated
        if not all(isinstance(f, str) for f in features):
            raise ApiError("Validation failed", 422, {"features": "Must be a list of strings"})
        data = dict(data, features="\n".join(f.strip() for f in features if f.strip()))
    unknown = set(data) - set(SOLUTION_SPEC) - set(SOLUTION_EXTRAS)
    if unknown:
        raise ApiError("Unknown field(s): " + ", ".join(sorted(unknown)))
    fields = _clean({k: v for k, v in data.items() if k in SOLUTION_SPEC}, SOLUTION_SPEC, partial)
    errors, extra = {}, {}
    _int(data, extra, "z_index", errors)
    _int(data, extra, "display_order", errors)
    _bool(data, extra, "is_active", errors)
    if errors:
        raise ApiError("Validation failed", 422, errors)
    fields.update(extra)
    return fields


@api_view
@require_http_methods(["GET", "POST"])
def solutions_collection(request):
    if request.method == "GET":
        qs = Solution.objects.all() if request.GET.get("all") else Solution.objects.filter(is_active=True)
        return _json({"results": [_solution_out(s) for s in qs]})
    fields = _solution_fields(_body(request), partial=False)
    slug = fields.pop("slug", "") or slugify(fields["title"])[:50]
    obj, created = Solution.objects.get_or_create(slug=slug, defaults=fields)
    if not created:
        for k, v in fields.items():
            setattr(obj, k, v)
        obj.save()
    return _json(_solution_out(obj), 201 if created else 200)


@api_view
@require_http_methods(["GET", "PUT", "PATCH", "DELETE"])
def solution_item(request, slug):
    try:
        obj = Solution.objects.get(pk=slug)
    except Solution.DoesNotExist:
        raise ApiError("Solution not found", 404)
    if request.method == "GET":
        return _json(_solution_out(obj))
    if request.method == "DELETE":
        obj.delete()
        return _json({"deleted": slug})
    fields = _solution_fields(_body(request), partial=request.method == "PATCH")
    if "slug" in fields and fields["slug"] != slug:
        raise ApiError("Validation failed", 422, {"slug": "Slug cannot be changed"})
    fields.pop("slug", None)
    for k, v in fields.items():
        setattr(obj, k, v)
    obj.save()
    return _json(_solution_out(obj))
