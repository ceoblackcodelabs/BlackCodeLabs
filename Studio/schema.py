"""Tiny declarative form schema used by every document type.

A document type is described as sections of fields. The same description drives
(1) the form the browser builds, and (2) the server-side validation, so a form can
never submit something the PDF renderer doesn't expect.

Field kinds: text, textarea, date, number, money, select, list.
A list holds rows of `item` = {"kind": "text"|"textarea"} or {"kind": "group", "fields": [...]}.
"""
import re
from datetime import date
from decimal import Decimal, InvalidOperation

_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def _f(kind, name, label, **kw):
    return {"kind": kind, "name": name, "label": label, **kw}


def text(name, label, **kw):
    return _f("text", name, label, **kw)


def textarea(name, label, **kw):
    return _f("textarea", name, label, **kw)


def date_(name, label, **kw):
    return _f("date", name, label, **kw)


def number(name, label, **kw):
    return _f("number", name, label, **kw)


def money(name, label, **kw):
    return _f("money", name, label, **kw)


def select(name, label, choices, **kw):
    return _f("select", name, label, choices=list(choices), **kw)


def lines(name, label, item_kind="text", **kw):
    """A list of single text rows (bullets, paragraphs)."""
    return _f("list", name, label, item={"kind": item_kind}, **kw)


def rows(name, label, fields, **kw):
    """A list of grouped rows, each row holding the given sub-fields."""
    return _f("list", name, label, item={"kind": "group", "fields": fields}, **kw)


def section(title, fields, hint=""):
    return {"title": title, "hint": hint, "fields": fields}


def all_fields(sections):
    for s in sections:
        yield from s["fields"]


# ------------------------------------------------------------------ validation
class Errors(dict):
    def add(self, path, message):
        self.setdefault(path, message)


def _clean_str(value, spec, path, errors, kind):
    if value is None:
        value = ""
    if not isinstance(value, str):
        errors.add(path, "Must be text")
        return ""
    value = _CONTROL.sub("", value).strip()
    limit = spec.get("max_len") or (4000 if kind == "textarea" else 300)
    if len(value) > limit:
        errors.add(path, f"Max {limit} characters")
    if kind == "text":
        value = " ".join(value.split())
    return value


def clean_value(spec, value, path, errors):
    kind = spec["kind"]
    if kind in ("text", "textarea"):
        return _clean_str(value, spec, path, errors, kind)
    if kind == "select":
        value = _clean_str(value, spec, path, errors, "text")
        if value and value not in spec["choices"]:
            errors.add(path, "Pick one of the options")
        return value
    if kind == "date":
        value = _clean_str(value, spec, path, errors, "text")
        if value:
            try:
                date.fromisoformat(value)
            except ValueError:
                errors.add(path, "Enter a valid date")
        return value
    if kind in ("number", "money"):
        raw = _clean_str(value if not isinstance(value, (int, float)) else str(value), spec, path, errors, "text")
        raw = raw.replace(",", "")
        if not raw:
            return ""
        try:
            d = Decimal(raw)
            if not d.is_finite() or abs(d) > Decimal("1000000000000"):
                raise InvalidOperation
        except InvalidOperation:
            errors.add(path, "Enter a number")
            return ""
        if spec.get("min") is not None and d < Decimal(str(spec["min"])):
            errors.add(path, f"Must be at least {spec['min']}")
        if spec.get("max") is not None and d > Decimal(str(spec["max"])):
            errors.add(path, f"Must be at most {spec['max']}")
        return format(d.normalize(), "f") if d == d.to_integral() else str(d.quantize(Decimal("0.01")))
    if kind == "list":
        return _clean_list(spec, value, path, errors)
    errors.add(path, "Unsupported field")
    return None


def _is_blank(v):
    if isinstance(v, dict):
        return all(_is_blank(x) for x in v.values())
    if isinstance(v, list):
        return all(_is_blank(x) for x in v)
    return v in ("", None)


def _clean_list(spec, value, path, errors):
    if value is None:
        value = []
    if not isinstance(value, list):
        errors.add(path, "Must be a list")
        return []
    item = spec["item"]
    out = []
    for i, raw in enumerate(value):
        p = f"{path}.{i}"
        if item["kind"] == "group":
            if not isinstance(raw, dict):
                errors.add(p, "Invalid row")
                continue
            row = clean_fields(item["fields"], raw, p, errors, enforce_required=False)
            if _is_blank(row):
                continue  # untouched rows are dropped
            for f in item["fields"]:  # a row that is in use must have its required cells
                if f.get("required") and _is_blank(row.get(f["name"])):
                    errors.add(f"{p}.{f['name']}", "Required")
            out.append(row)
        else:
            v = clean_value(item, raw, p, errors)
            if v not in ("", None):
                out.append(v)
    if spec.get("max_items") and len(out) > spec["max_items"]:
        errors.add(path, f"At most {spec['max_items']} rows")
    if spec.get("min_items") and len(out) < spec["min_items"]:
        errors.add(path, f"Add at least {spec['min_items']}")
    return out


def clean_fields(fields, payload, prefix, errors, enforce_required=True):
    if not isinstance(payload, dict):
        errors.add(prefix or "_", "Invalid data")
        return {}
    out = {}
    for spec in fields:
        name = spec["name"]
        path = f"{prefix}.{name}" if prefix else name
        out[name] = clean_value(spec, payload.get(name), path, errors)
        if enforce_required and spec.get("required") and _is_blank(out[name]):
            errors.add(path, "Required")
    return out


def clean_document(sections, payload):
    """Returns (cleaned_data, errors)."""
    errors = Errors()
    cleaned = clean_fields(list(all_fields(sections)), payload, "", errors)
    return cleaned, errors


# ------------------------------------------------------------------ doc types
class DocType:
    """Subclass per document type and register it in Studio.doctypes."""

    key = ""
    label = ""
    code = ""            # reference prefix, e.g. WM -> BCL-WM-2610-01
    description = ""
    amount_label = "Total value"
    sections = []

    def defaults(self):
        return {}

    def sample(self):
        return None

    def amount(self, data):
        return None

    def validate(self, data):
        """Cross-field checks that a single field can't express. Return {field_path: message}."""
        return {}

    def title(self, data):
        return self.label

    def client(self, data):
        return data.get("client_name", "")

    def currency(self, data):
        return data.get("currency") or "KES"

    def render(self, data, meta):  # -> bytes
        raise NotImplementedError

    def form_config(self):
        return {"key": self.key, "label": self.label, "sections": self.sections}
