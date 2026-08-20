from decimal import Decimal

from django.db import migrations


STARTER_FEATURES = [
    ("One active project", True),
    ("Website development (up to 10 pages)", True),
    ("Basic SEO setup", True),
    ("REST API integration (1 API)", True),
    ("Mobile-responsive design", True),
    ("3 revision rounds", True),
    ("Email support (48 hr)", True),
    ("App development", False),
    ("Bug bounty program", False),
    ("Dedicated account manager", False),
]

PREMIUM_FEATURES = [
    ("Up to 3 active projects", True),
    ("Full-stack web application", True),
    ("Advanced SEO + monthly report", True),
    ("Custom API engineering (up to 5)", True),
    ("iOS or Android app development", True),
    ("Bug bounty security audit", True),
    ("Unlimited revisions", True),
    ("Priority support (4 hr)", True),
    ("Dedicated account manager", True),
    ("Monthly strategy call", True),
]

ENTERPRISE_FEATURES = [
    ("Unlimited active projects", True),
    ("Full platform engineering", True),
    ("Enterprise SEO strategy", True),
    ("Unlimited API development", True),
    ("iOS + Android apps", True),
    ("Full bug bounty program", True),
    ("24/7 dedicated support", True),
    ("Dedicated engineering team", True),
    ("Weekly sprint calls", True),
    ("SLA guarantee", True),
]

FAQS = [
    ("What happens after I sign up?",
     "You'll be assigned a project manager within 24 hours who schedules a kickoff call. "
     "Development begins within 48 hours of the kickoff."),
    ("Do I own the code and assets?",
     "Yes — 100%. Upon final payment, all source code, assets, and intellectual property "
     "transfer entirely to you. We sign an IP transfer agreement on every project."),
    ("Can I switch plans later?",
     "Absolutely. Upgrades take effect immediately. Downgrades apply at the start of your "
     "next billing cycle. No penalties."),
    ("What technologies do you work with?",
     "We work across the full stack — React, Next.js, Node.js, Python, Django, React Native, "
     "AWS, PostgreSQL, and much more. We choose the right tool for the job."),
]

PORTFOLIO_PROJECTS = [
    dict(
        title="VoteHub Awards Platform",
        slug="votehub-awards-platform",
        client_name="BCL Production",
        category="web",
        summary="A live voting and competition platform with M-Pesa payments, digital tickets, and tour bookings.",
        description="A full Django platform built for BCL Production to run branded award shows: "
                     "real-time nominee voting, M-Pesa STK push integration, digital ticketing, and "
                     "tour/event bookings, all from one admin-managed backend.",
        technologies="Django, PostgreSQL, M-Pesa Daraja API, JavaScript",
        completed_year=2025,
        is_featured=True,
        display_order=1,
        cover_image_url="https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1200&q=80",
    ),
    dict(
        title="CareerForge ATS",
        slug="careerforge-ats",
        client_name="Internal Product",
        category="web",
        summary="A Django-powered applicant tracking system with automated resume scoring.",
        description="An ATS rebuilt from an earlier React Native concept into a Django web app that "
                     "scores resumes against job descriptions, ranks candidates automatically, and "
                     "gives recruiters a clean review dashboard.",
        technologies="Django, Python, PostgreSQL, NLP scoring",
        completed_year=2025,
        is_featured=True,
        display_order=2,
        cover_image_url="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1200&q=80",
    ),
    dict(
        title="DaySafari Adventures",
        slug="daysafari-adventures",
        client_name="DaySafari",
        category="web",
        summary="A safari and tourism booking site showcasing curated Kenyan travel experiences.",
        description="A Django tourism site for booking safari packages and day trips, with a content "
                     "structure built for local SEO across Kenyan travel search terms.",
        technologies="Django, Bootstrap, JavaScript",
        completed_year=2024,
        is_featured=False,
        display_order=3,
        cover_image_url="https://images.unsplash.com/photo-1516426122078-c23e76319801?w=1200&q=80",
    ),
    dict(
        title="BHealthy E-Commerce",
        slug="bhealthy-ecommerce",
        client_name="BHealthy",
        category="ecommerce",
        summary="A Halal-certified sports nutrition and beauty products storefront.",
        description="An e-commerce build for BHealthy covering product catalogues for sports "
                     "nutrition/supplements and beauty products, styled after modern beauty-retail UX.",
        technologies="Django, PostgreSQL, Stripe/M-Pesa",
        completed_year=2024,
        is_featured=False,
        display_order=4,
        cover_image_url="https://images.unsplash.com/photo-1556228720-195a672e8a03?w=1200&q=80",
    ),
]


def seed(apps, schema_editor):
    PricingPlan = apps.get_model("Home", "PricingPlan")
    PricingFeature = apps.get_model("Home", "PricingFeature")
    PricingFAQ = apps.get_model("Home", "PricingFAQ")
    PortfolioProject = apps.get_model("Home", "PortfolioProject")

    if not PricingPlan.objects.exists():
        starter = PricingPlan.objects.create(
            name="Starter", slug="starter",
            tagline="For entrepreneurs and small teams launching their first digital product.",
            monthly_price=Decimal("499.00"), annual_price=Decimal("399.00"),
            cta_text="Get Started \u2192", cta_url_name="contact",
            display_order=1,
        )
        for i, (text, included) in enumerate(STARTER_FEATURES):
            PricingFeature.objects.create(plan=starter, text=text, is_included=included, display_order=i)

        premium = PricingPlan.objects.create(
            name="Premium", slug="premium",
            tagline="For growing companies that need serious engineering and rapid delivery.",
            monthly_price=Decimal("1499.00"), annual_price=Decimal("1199.00"),
            is_featured=True, featured_badge_text="Most Popular",
            cta_text="Upgrade to Premium \u2192", cta_url_name="contact",
            display_order=2,
        )
        for i, (text, included) in enumerate(PREMIUM_FEATURES):
            PricingFeature.objects.create(plan=premium, text=text, is_included=included, display_order=i)

        enterprise = PricingPlan.objects.create(
            name="Custom", slug="custom",
            tagline="Fully tailored solutions for enterprises building complex, large-scale platforms.",
            eyebrow_text="Enterprise", custom_price_label="Let's Talk",
            cta_text="Request a Quote \u2192", cta_url_name="contact",
            display_order=3,
        )
        for i, (text, included) in enumerate(ENTERPRISE_FEATURES):
            PricingFeature.objects.create(plan=enterprise, text=text, is_included=included, display_order=i)

    if not PricingFAQ.objects.exists():
        for i, (q, a) in enumerate(FAQS):
            PricingFAQ.objects.create(question=q, answer=a, display_order=i)

    if not PortfolioProject.objects.exists():
        for data in PORTFOLIO_PROJECTS:
            PortfolioProject.objects.create(**data)


def unseed(apps, schema_editor):
    PricingPlan = apps.get_model("Home", "PricingPlan")
    PricingFAQ = apps.get_model("Home", "PricingFAQ")
    PortfolioProject = apps.get_model("Home", "PortfolioProject")
    PricingPlan.objects.filter(slug__in=["starter", "premium", "custom"]).delete()
    PricingFAQ.objects.all().delete()
    PortfolioProject.objects.filter(
        title__in=[p["title"] for p in PORTFOLIO_PROJECTS]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("Home", "0002_portfolioproject_pricingfaq_pricingplan_and_more"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
