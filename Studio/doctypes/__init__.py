"""Registry of document types. To add one: subclass DocType, then add it to _TYPES."""
from .billing import Invoice, Quotation
from .contract import ServiceAgreement
from .proposal import WebsiteManagementProposal

_TYPES = [WebsiteManagementProposal(), ServiceAgreement(), Quotation(), Invoice()]
REGISTRY = {t.key: t for t in _TYPES}


def all_types():
    return list(_TYPES)


def get(key):
    return REGISTRY.get(key)


def choices():
    return [(t.key, t.label) for t in _TYPES]
