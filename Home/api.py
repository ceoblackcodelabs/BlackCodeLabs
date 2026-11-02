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

    GET    /api/v1/posts/                 list blog posts (add ?all=1 to include drafts)
    POST   /api/v1/posts/                 create, or update if `slug` exists (upsert)
    GET    /api/v1/posts/<slug>/          read one
    PUT    /api/v1/posts/<slug>/          replace   (PATCH = partial update)
    DELETE /api/v1/posts/<slug>/          delete

    GET    /api/v1/portfolio/             list portfolio projects (add ?all=1 to include hidden)
    POST   /api/v1/portfolio/             create, or update if `slug` exists (upsert)
    GET    /api/v1/portfolio/<slug>/      read one
    PUT    /api/v1/portfolio/<slug>/      replace   (PATCH = partial update)
    DELETE /api/v1/portfolio/<slug>/      delete

Posts and portfolio projects accept an optional base64 image (see POST_IMAGE_FIELD / PORTFOLIO_IMAGE_FIELD).
Saves go through the ORM, so the existing signals clear the relevant caches.
"""
import base64
import binascii
import hmac
import io
import json
import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
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


# ------------------------------------------------------------------ shared: images + HTML safety
MAX_IMAGE_BYTES = 8 * 1024 * 1024
IMAGE_FORMATS = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp"}
URL_RE = re.compile(r"^https?://[^\s]{1,490}$")
_BAD_HTML = re.compile(r"<\s*(script|iframe|object|embed|style|link|meta|form|base)\b|\bon\w+\s*=|javascript\s*:", re.I)


def _safe_html(value, field):
    """A guard, not a sanitiser: refuses markup that can run code if the content is ever rendered unescaped."""
    if _BAD_HTML.search(value):
        raise ApiError("Validation failed", 422, {field: "Script, iframe, form or inline event handlers are not allowed"})
    return value


def _image_file(b64, field, name):
    """Decode a base64 (or data: URI) image, verify it really is a JPEG/PNG/WebP, return a ContentFile."""
    from PIL import Image, UnidentifiedImageError
    if not isinstance(b64, str):
        raise ApiError("Validation failed", 422, {field: "Must be a base64 string"})
    if b64.startswith("data:"):
        b64 = b64.split(",", 1)[-1]
    try:
        raw = base64.b64decode(b64, validate=True)
    except (binascii.Error, ValueError):
        raise ApiError("Validation failed", 422, {field: "Not valid base64"})
    if not raw or len(raw) > MAX_IMAGE_BYTES:
        raise ApiError("Validation failed", 422, {field: f"Image must be between 1 byte and {MAX_IMAGE_BYTES // 1024 // 1024} MB"})
    try:
        img = Image.open(io.BytesIO(raw))
        fmt = img.format
        img.verify()
        if img.width * img.height > 40_000_000:
            raise ValueError
    except (UnidentifiedImageError, ValueError, OSError, Image.DecompressionBombError):
        raise ApiError("Validation failed", 422, {field: "Not a valid image"})
    if fmt not in IMAGE_FORMATS:
        raise ApiError("Validation failed", 422, {field: "Use a JPEG, PNG or WebP image"})
    return ContentFile(raw, name=f"{name}.{IMAGE_FORMATS[fmt]}")


def _int_field(data, field, errors, lo, hi):
    if field not in data:
        return None
    v = data[field]
    if isinstance(v, bool) or not isinstance(v, int) or not lo <= v <= hi:
        errors[field] = f"Must be a whole number from {lo} to {hi}"
        return None
    return v


def _flag(data, field, errors):
    if field not in data:
        return None
    if not isinstance(data[field], bool):
        errors[field] = "Must be true or false"
        return None
    return data[field]


def _split(data, text_spec, extra_keys, partial, preprocess=None):
    """Validate the text fields with _clean, reject unknown keys, return (text_fields, raw_data)."""
    if preprocess:
        data = preprocess(data)
    unknown = set(data) - set(text_spec) - set(extra_keys)
    if unknown:
        raise ApiError("Unknown field(s): " + ", ".join(sorted(unknown)))
    return _clean({k: v for k, v in data.items() if k in text_spec}, text_spec, partial), data


def _upsert(model, slug, defaults, apply):
    obj = model.objects.filter(slug=slug).first()
    created = obj is None
    if created:
        obj = model(slug=slug)
    apply(obj, defaults)
    obj.save()
    return obj, created


# ------------------------------------------------------------------ blog posts
POST_SPEC = {
    "slug": (False, 240, re.compile(r"^[-a-z0-9_]+$"), "Lowercase letters, numbers, - and _ only"),
    "title": (True, 220, None, ""),
    "excerpt": (True, 320, None, ""),
    "body": (True, 100000, None, ""),
    "category": (False, 60, None, ""),
    "author": (False, 150, None, ""),
    "image_url": (False, 500, URL_RE, "Must be an http(s) URL"),
    "status": (False, 10, re.compile(r"^(draft|published)$"), "Must be draft or published"),
    "published_at": (False, 40, None, ""),
}
POST_EXTRAS = ("featured", "read_minutes", "image_base64")


def _post_out(p):
    return {"slug": p.slug, "title": p.title, "excerpt": p.excerpt, "body": p.body, "status": p.status,
            "category": p.category.name if p.category else None, "author": p.author.get_username(),
            "featured": p.featured, "read_minutes": p.read_minutes, "image_url": p.image_url,
            "image": p.image.url if p.image else None, "published_at": p.published_at.isoformat(),
            "url": p.get_absolute_url(), "created_at": p.created_at.isoformat()}


def _post_fields(data, partial):
    fields, raw = _split(data, POST_SPEC, POST_EXTRAS, partial)
    errors, extra = {}, {}
    for name, val in (("featured", _flag(raw, "featured", errors)), ("read_minutes", _int_field(raw, "read_minutes", errors, 1, 180))):
        if name in raw and val is not None:
            extra[name] = val
    if "body" in fields:
        _safe_html(fields["body"], "body")
    if fields.get("published_at"):
        dt = parse_datetime(fields["published_at"])
        if not dt:
            errors["published_at"] = "Use an ISO date-time, e.g. 2026-11-02T09:00:00+03:00"
        else:
            from django.utils import timezone
            fields["published_at"] = dt if timezone.is_aware(dt) else timezone.make_aware(dt)
    elif "published_at" in fields:
        del fields["published_at"]
    if errors:
        raise ApiError("Validation failed", 422, errors)
    fields.update(extra)
    return fields, raw.get("image_base64")


def _resolve_author(name):
    User = get_user_model()
    user = User.objects.filter(**{User.USERNAME_FIELD: name}).first() if name else User.objects.filter(is_superuser=True).order_by("pk").first()
    if not user:
        raise ApiError("Validation failed", 422, {"author": "No such user" if name else "No superuser exists to publish as; pass `author`"})
    return user


def _apply_post(post, fields, image_b64=None, creating=False):
    from Blogs.models import Category
    cat = fields.pop("category", None)
    author = fields.pop("author", None)
    for k, v in fields.items():
        setattr(post, k, v)
    if cat:
        post.category = Category.objects.get_or_create(name=cat)[0]
    if creating or author:
        post.author = _resolve_author(author)
    if image_b64:
        if post.image:
            post.image.delete(save=False)
        f = _image_file(image_b64, "image_base64", post.slug)
        post.image.save(f.name, f, save=False)


@api_view
@require_http_methods(["GET", "POST"])
def posts_collection(request):
    from Blogs.models import Post
    if request.method == "GET":
        qs = Post.objects.select_related("category", "author")
        if not request.GET.get("all"):
            qs = qs.filter(status="published")
        return _json({"results": [_post_out(p) for p in qs]})
    fields, img = _post_fields(_body(request), partial=False)
    slug = fields.pop("slug", "") or slugify(fields["title"])[:200]
    if not slug:
        raise ApiError("Validation failed", 422, {"slug": "Could not make a slug from the title; pass `slug`"})
    existing = Post.objects.filter(slug=slug).first()
    post = existing or Post(slug=slug)
    _apply_post(post, fields, img, creating=existing is None)
    post.save()
    return _json(_post_out(post), 200 if existing else 201)


@api_view
@require_http_methods(["GET", "PUT", "PATCH", "DELETE"])
def post_item(request, slug):
    from Blogs.models import Post
    post = Post.objects.select_related("category", "author").filter(slug=slug).first()
    if not post:
        raise ApiError("Post not found", 404)
    if request.method == "GET":
        return _json(_post_out(post))
    if request.method == "DELETE":
        if post.image:
            post.image.delete(save=False)
        post.delete()
        return _json({"deleted": slug})
    fields, img = _post_fields(_body(request), partial=request.method == "PATCH")
    if fields.pop("slug", slug) != slug:
        raise ApiError("Validation failed", 422, {"slug": "Slug cannot be changed"})
    _apply_post(post, fields, img)
    post.save()
    return _json(_post_out(post))


# ------------------------------------------------------------------ portfolio
PORTFOLIO_CATEGORIES = ["web", "mobile", "api", "ai", "ecommerce", "branding", "other"]
PORTFOLIO_SPEC = {
    "slug": (False, 170, re.compile(r"^[-a-z0-9_]+$"), "Lowercase letters, numbers, - and _ only"),
    "title": (True, 150, None, ""),
    "summary": (True, 280, None, ""),
    "description": (False, 20000, None, ""),
    "client_name": (False, 150, None, ""),
    "category": (False, 20, re.compile("^(" + "|".join(PORTFOLIO_CATEGORIES) + ")$"), "Use one of: " + ", ".join(PORTFOLIO_CATEGORIES)),
    "technologies": (False, 300, None, ""),
    "cover_image_url": (False, 500, URL_RE, "Must be an http(s) URL"),
    "project_url": (False, 500, URL_RE, "Must be an http(s) URL"),
}
PORTFOLIO_EXTRAS = ("completed_year", "is_featured", "display_order", "is_active", "cover_image_base64")


def _portfolio_out(p):
    return {"slug": p.slug, "title": p.title, "summary": p.summary, "description": p.description,
            "client_name": p.client_name, "category": p.category, "technologies": p.tech_list(),
            "cover_image_url": p.cover_image_url, "cover_image": p.cover_image.url if p.cover_image else None,
            "project_url": p.project_url, "completed_year": p.completed_year, "is_featured": p.is_featured,
            "display_order": p.display_order, "is_active": p.is_active, "url": p.get_absolute_url(),
            "created_at": p.created_at.isoformat()}


def _portfolio_fields(data, partial):
    def prep(d):
        d = dict(d)
        if isinstance(d.get("technologies"), list):
            if not all(isinstance(t, str) for t in d["technologies"]):
                raise ApiError("Validation failed", 422, {"technologies": "Must be a list of strings"})
            d["technologies"] = ", ".join(t.strip() for t in d["technologies"] if t.strip())
        return d
    fields, raw = _split(data, PORTFOLIO_SPEC, PORTFOLIO_EXTRAS, partial, preprocess=prep)
    errors = {}
    for name, val in (("completed_year", _int_field(raw, "completed_year", errors, 1990, 2100)),
                      ("display_order", _int_field(raw, "display_order", errors, 0, 100000)),
                      ("is_featured", _flag(raw, "is_featured", errors)), ("is_active", _flag(raw, "is_active", errors))):
        if name in raw and val is not None:
            fields[name] = val
    if "description" in fields:
        _safe_html(fields["description"], "description")
    if errors:
        raise ApiError("Validation failed", 422, errors)
    return fields, raw.get("cover_image_base64")


def _apply_portfolio(obj, fields, image_b64=None):
    for k, v in fields.items():
        setattr(obj, k, v)
    if image_b64:
        if obj.cover_image:
            obj.cover_image.delete(save=False)
        f = _image_file(image_b64, "cover_image_base64", obj.slug)
        obj.cover_image.save(f.name, f, save=False)


@api_view
@require_http_methods(["GET", "POST"])
def portfolio_collection(request):
    from .models import PortfolioProject
    if request.method == "GET":
        qs = PortfolioProject.objects.all() if request.GET.get("all") else PortfolioProject.objects.filter(is_active=True)
        return _json({"results": [_portfolio_out(p) for p in qs]})
    fields, img = _portfolio_fields(_body(request), partial=False)
    slug = fields.pop("slug", "") or slugify(fields["title"])[:160]
    if not slug:
        raise ApiError("Validation failed", 422, {"slug": "Could not make a slug from the title; pass `slug`"})
    existing = PortfolioProject.objects.filter(slug=slug).first()
    obj = existing or PortfolioProject(slug=slug)
    _apply_portfolio(obj, fields, img)
    obj.save()
    return _json(_portfolio_out(obj), 200 if existing else 201)


@api_view
@require_http_methods(["GET", "PUT", "PATCH", "DELETE"])
def portfolio_item(request, slug):
    from .models import PortfolioProject
    obj = PortfolioProject.objects.filter(slug=slug).first()
    if not obj:
        raise ApiError("Project not found", 404)
    if request.method == "GET":
        return _json(_portfolio_out(obj))
    if request.method == "DELETE":
        if obj.cover_image:
            obj.cover_image.delete(save=False)
        obj.delete()
        return _json({"deleted": slug})
    fields, img = _portfolio_fields(_body(request), partial=request.method == "PATCH")
    if fields.pop("slug", slug) != slug:
        raise ApiError("Validation failed", 422, {"slug": "Slug cannot be changed"})
    _apply_portfolio(obj, fields, img)
    obj.save()
    return _json(_portfolio_out(obj))
