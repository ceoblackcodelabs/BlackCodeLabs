from django.conf import settings


def brand():
    """Company details printed on every document. Override any of them in .env / settings."""
    g = lambda k, d: getattr(settings, k, d)
    return {
        "name": g("DOC_COMPANY_NAME", "Black Code Labs"),
        "tagline": g("DOC_TAGLINE", "Web Development  |  Automation  |  Cybersecurity"),
        "phone": g("DOC_PHONE", "0799 804 185"),
        "email": g("DOC_EMAIL", "info@blackcodelab.com"),
        "website": g("DOC_WEBSITE", "blackcodelab.com"),
        "city": g("DOC_CITY", "Nairobi, Kenya"),
        "signatory": g("DOC_SIGNATORY", "Odhiambo Churchill"),
    }
