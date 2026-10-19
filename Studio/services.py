"""Creating / regenerating documents (shared by the save view, duplicate and the admin)."""
from datetime import date

from django.db import IntegrityError, transaction

from . import doctypes
from .branding import brand
from .models import GeneratedDocument


def _doc_date(data):
    try:
        return date.fromisoformat(data.get("date") or "")
    except ValueError:
        return date.today()


def next_reference(doc_type, data):
    """BCL-WM-2610-01: company, type code, YYMM of the document date, running number for that month."""
    d = _doc_date(data)
    prefix = f"BCL-{doc_type.code}-{d:%y%m}-"
    used = set(GeneratedDocument.objects.filter(reference__startswith=prefix).values_list("reference", flat=True))
    n = 1
    while f"{prefix}{n:02d}" in used:
        n += 1
    return f"{prefix}{n:02d}"


def _fields(doc_type, data, reference, revision_pdf):
    return dict(
        title=doc_type.title(data)[:200],
        client_name=doc_type.client(data)[:200],
        amount=doc_type.amount(data),
        currency=doc_type.currency(data),
        data=data,
        pdf=revision_pdf,
    )


def save_document(doc_type, data, user, doc=None, status=None):
    """Validate-free: `data` must already be cleaned. Renders the PDF, then stores data + PDF together.

    Rendering happens before anything is written, so a failed render never leaves a half-saved row.
    """
    for attempt in range(5):
        try:
            with transaction.atomic():
                reference = doc.reference if doc else next_reference(doc_type, data)
                pdf = doc_type.render(data, {"brand": brand(), "reference": reference, "currency": doc_type.currency(data)})
                fields = _fields(doc_type, data, reference, pdf)
                if doc:
                    for k, v in fields.items():
                        setattr(doc, k, v)
                    doc.revision += 1
                    if status:
                        doc.status = status
                    doc.save()
                else:
                    doc = GeneratedDocument.objects.create(doc_type=doc_type.key, reference=reference,
                                                           created_by=user, status=status or "draft", **fields)
                return doc
        except IntegrityError:  # two people took the same reference at once; try the next number
            if doc:
                raise
    raise RuntimeError("Could not allocate a unique reference")


def duplicate_document(doc, user):
    t = doctypes.get(doc.doc_type)
    data = dict(doc.data)
    data["date"] = date.today().isoformat()
    return save_document(t, data, user)
