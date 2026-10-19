import json
from datetime import timedelta
from functools import wraps

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncDate, TruncMonth
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import NoReverseMatch, reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.http import require_POST

from . import doctypes
from .models import GeneratedDocument
from .schema import clean_document
from .services import duplicate_document, save_document

RANGES = {"30": 30, "90": 90, "180": 180, "365": 365}


def staff_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if not request.user.is_staff:
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return never_cache(wrapper)


def _admin_link(name):
    try:
        return reverse(f"admin:{name}_changelist")
    except NoReverseMatch:
        return None


def _nav(request, active):
    site = [(label, _admin_link(model)) for label, model in [
        ("Inquiries", "Home_contactinquiry"), ("Blog posts", "Blogs_post"), ("Portfolio", "Home_portfolioproject"),
        ("Services", "Home_techservices"), ("Solutions", "Home_solution"), ("Pricing plans", "Home_pricingplan")]]
    return {"active": active, "site_links": [(l, u) for l, u in site if u],
            "doc_types": [(t.key, t.label) for t in doctypes.all_types()], "admin_url": _admin_link("auth_user")}


def _ctx(request, active, **extra):
    return {"nav": _nav(request, active), **extra}


def _type_or_404(key):
    t = doctypes.get(key)
    if not t:
        raise Http404("Unknown document type")
    return t


# ----------------------------------------------------------------- dashboard
@staff_required
def dashboard(request):
    from Home.models import ContactInquiry, PortfolioProject, Solution, TechServices
    days = RANGES.get(request.GET.get("range", "90"), 90)
    today = timezone.localdate()
    since = today - timedelta(days=days - 1)
    since_dt = timezone.make_aware(timezone.datetime.combine(since, timezone.datetime.min.time()))

    docs = GeneratedDocument.objects.defer("pdf")
    in_range = docs.filter(created_at__gte=since_dt)
    types = doctypes.all_types()

    # --- stacked bars: documents per month, by type
    months, cursor = [], today.replace(day=1)
    n_months = max(3, min(12, days // 30))
    for _ in range(n_months):
        months.append(cursor)
        cursor = (cursor - timedelta(days=1)).replace(day=1)
    months.reverse()
    counts = {}
    for row in docs.filter(created_at__date__gte=months[0]).annotate(m=TruncMonth("created_at")).values("m", "doc_type").annotate(c=Count("id")):
        counts[(row["m"].date() if hasattr(row["m"], "date") else row["m"], row["doc_type"])] = row["c"]
    by_month = {
        "labels": [m.strftime("%b %Y") for m in months],
        "series": [{"key": t.key, "label": t.label, "data": [counts.get((m, t.key), 0) for m in months]} for t in types],
    }

    # --- value by status
    value_rows = {r["status"]: r["v"] or 0 for r in in_range.values("status").annotate(v=Sum("amount"))}
    status_labels = dict(GeneratedDocument.STATUS_CHOICES)
    by_status = {"labels": [status_labels[k] for k in status_labels], "data": [float(value_rows.get(k, 0)) for k in status_labels]}

    # --- inquiries per day
    inq_counts = {r["d"]: r["c"] for r in ContactInquiry.objects.filter(created_at__gte=since_dt)
                  .annotate(d=TruncDate("created_at")).values("d").annotate(c=Count("id"))}
    day_list = [since + timedelta(days=i) for i in range(days)]
    inquiries = {"labels": [d.strftime("%d %b") for d in day_list], "data": [inq_counts.get(d, 0) for d in day_list]}

    total_value = in_range.aggregate(v=Sum("amount"))["v"] or 0
    won_value = in_range.filter(status="accepted").aggregate(v=Sum("amount"))["v"] or 0
    open_value = in_range.filter(status__in=["draft", "sent"]).aggregate(v=Sum("amount"))["v"] or 0
    inq_total = sum(inquiries["data"])
    try:
        from Blogs.models import Post
        posts = Post.objects.filter(status="published").count()
    except Exception:
        posts = None

    stats = {
        "docs": in_range.count(), "docs_all": docs.count(), "value": total_value, "won": won_value, "open": open_value,
        "inquiries": inq_total, "new_inquiries": ContactInquiry.objects.filter(status="new").count(),
        "projects": PortfolioProject.objects.filter(is_active=True).count(),
        "solutions": Solution.objects.filter(is_active=True).count(), "services": TechServices.objects.count(), "posts": posts,
    }
    return render(request, "studio/dashboard.html", _ctx(
        request, "overview", range=str(days), ranges=list(RANGES), stats=stats,
        recent_docs=docs[:8], recent_inquiries=ContactInquiry.objects.order_by("-created_at")[:6],
        charts={"by_month": by_month, "by_status": by_status, "inquiries": inquiries, "range": days}))


# ----------------------------------------------------------------- documents list
@staff_required
def document_list(request):
    qs = GeneratedDocument.objects.defer("pdf")
    q = request.GET.get("q", "").strip()
    typ = request.GET.get("type", "")
    status = request.GET.get("status", "")
    if q:
        qs = qs.filter(Q(client_name__icontains=q) | Q(reference__icontains=q) | Q(title__icontains=q))
    if typ in doctypes.REGISTRY:
        qs = qs.filter(doc_type=typ)
    if status in dict(GeneratedDocument.STATUS_CHOICES):
        qs = qs.filter(status=status)
    page = Paginator(qs, 20).get_page(request.GET.get("page"))
    labels = {t.key: t.label for t in doctypes.all_types()}
    for d in page:
        d.type_label = labels.get(d.doc_type, d.doc_type)
    keep = "&".join(f"{k}={v}" for k, v in (("q", q), ("type", typ), ("status", status)) if v)
    return render(request, "studio/document_list.html", _ctx(
        request, f"docs-{typ}" if typ else "docs", page=page, q=q, typ=typ, status=status, keep=keep,
        statuses=GeneratedDocument.STATUS_CHOICES, types=[(t.key, t.label) for t in doctypes.all_types()]))


# ----------------------------------------------------------------- create / edit
@staff_required
def document_form(request, pk=None):
    doc = get_object_or_404(GeneratedDocument.objects.defer("pdf"), pk=pk) if pk else None
    key = doc.doc_type if doc else request.GET.get("type") or doctypes.all_types()[0].key
    t = _type_or_404(key)
    initial = doc.data if doc else t.defaults()
    config = {
        "type": t.key, "id": doc.pk if doc else None, "sections": t.sections, "initial": initial,
        "sample": t.sample(), "saveUrl": reverse("studio:document_save"),
        "listUrl": reverse("studio:document_list"),
    }
    return render(request, "studio/document_form.html", _ctx(
        request, f"new-{t.key}" if not doc else f"docs-{t.key}", doc=doc, doctype=t, config=config,
        types=[(x.key, x.label, x.description) for x in doctypes.all_types()]))


@staff_required
@require_POST
def document_save(request):
    try:
        body = json.loads(request.body.decode())
        t = doctypes.get(body.get("type"))
        if not t or not isinstance(body.get("data"), dict):
            raise ValueError
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "Bad request"}, status=400)
    data, errors = clean_document(t.sections, body["data"])
    if errors:
        return JsonResponse({"ok": False, "errors": errors}, status=422)
    doc = None
    if body.get("id"):
        doc = get_object_or_404(GeneratedDocument, pk=body["id"], doc_type=t.key)
    try:
        saved = save_document(t, data, request.user, doc=doc)
    except Exception as exc:  # a render problem must never lose the user's work silently
        return JsonResponse({"ok": False, "error": f"Could not generate the PDF: {exc}"}, status=500)
    return JsonResponse({"ok": True, "url": reverse("studio:document_detail", args=[saved.pk]), "reference": saved.reference})


# ----------------------------------------------------------------- detail / pdf / actions
@staff_required
def document_detail(request, pk):
    doc = get_object_or_404(GeneratedDocument.objects.defer("pdf"), pk=pk)
    t = doctypes.get(doc.doc_type)
    return render(request, "studio/document_detail.html", _ctx(
        request, f"docs-{doc.doc_type}", doc=doc, doctype=t, statuses=GeneratedDocument.STATUS_CHOICES))


@staff_required
@xframe_options_sameorigin
def document_pdf(request, pk):
    doc = get_object_or_404(GeneratedDocument, pk=pk)
    resp = HttpResponse(bytes(doc.pdf), content_type="application/pdf")
    disposition = "attachment" if request.GET.get("download") else "inline"
    resp["Content-Disposition"] = f'{disposition}; filename="{doc.filename}"'
    resp["X-Content-Type-Options"] = "nosniff"
    return resp


@staff_required
@require_POST
def document_status(request, pk):
    doc = get_object_or_404(GeneratedDocument.objects.defer("pdf"), pk=pk)
    status = request.POST.get("status")
    if status in dict(GeneratedDocument.STATUS_CHOICES):
        doc.status = status
        doc.save(update_fields=["status", "updated_at"])
        messages.success(request, f"{doc.reference} marked {doc.get_status_display().lower()}.")
    nxt = request.POST.get("next", "")
    if nxt and url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        return redirect(nxt)
    return redirect("studio:document_detail", pk)


@staff_required
@require_POST
def document_duplicate(request, pk):
    doc = get_object_or_404(GeneratedDocument.objects.defer("pdf"), pk=pk)
    copy = duplicate_document(doc, request.user)
    messages.success(request, f"Created {copy.reference} as a copy of {doc.reference}.")
    return redirect("studio:document_detail", copy.pk)


@staff_required
@require_POST
def document_delete(request, pk):
    doc = get_object_or_404(GeneratedDocument.objects.defer("pdf"), pk=pk)
    ref = doc.reference
    doc.delete()
    messages.success(request, f"Deleted {ref}.")
    return redirect("studio:document_list")
