from decimal import Decimal

from django.db import migrations, models


OLD_FAQ_QUESTIONS = [
    "What happens after I sign up?",
    "Do I own the code and assets?",
    "Can I switch plans later?",
    "What technologies do you work with?",
]

PLANS = [
    dict(
        slug="starter", name="Starter", display_order=1,
        tagline="A fast, professional website for a business launching or refreshing its online presence.",
        project_price="45000", maintenance_monthly="3500",
        maintenance_note="Hosting care, backups, security updates and 1 hr of content changes each month.",
        delivery_time="1-2 weeks", is_featured=False, eyebrow_text="", custom_price_label="",
        cta_text="Start a Website →",
        features=[
            ("Custom-designed website (up to 8 pages)", True),
            ("Mobile-responsive, fast-loading build", True),
            ("On-page SEO setup + Google Search Console", True),
            ("Contact form, WhatsApp button & Google Maps", True),
            ("Domain, hosting & SSL setup", True),
            ("2 revision rounds", True),
            ("Custom web application / logins", False),
            ("Mobile app", False),
        ],
    ),
    dict(
        slug="business", name="Business", display_order=2,
        tagline="Custom web platforms, online stores and booking systems that take payments and run your operations.",
        project_price="150000", maintenance_monthly="10000",
        maintenance_note="Hosting, monitoring, backups, security patches, bug fixes and 4 hrs of improvements each month.",
        delivery_time="4-8 weeks", is_featured=True, eyebrow_text="", custom_price_label="",
        cta_text="Build My Platform →",
        features=[
            ("Custom web application or e-commerce store", True),
            ("M-Pesa (Daraja), card & bank payment integration", True),
            ("Admin dashboard to manage your business", True),
            ("User accounts, roles & email/SMS notifications", True),
            ("Third-party API integrations", True),
            ("Advanced SEO + analytics setup", True),
            ("Source code & IP handed over to you", True),
            ("Unlimited revisions during build", True),
        ],
    ),
    dict(
        slug="premium", name="Premium", display_order=3,
        tagline="Mobile apps and multi-system products for companies that need serious engineering.",
        project_price="450000", maintenance_monthly="25000",
        maintenance_note="Priority support, uptime monitoring, app-store updates, performance tuning and 10 hrs of development each month.",
        delivery_time="8-16 weeks", is_featured=False, eyebrow_text="", custom_price_label="",
        cta_text="Plan My App →",
        features=[
            ("iOS + Android app (React Native)", True),
            ("Scalable Django API & database design", True),
            ("Web admin panel + customer web app", True),
            ("Payments, push notifications & real-time features", True),
            ("Security review & load testing", True),
            ("App Store & Google Play publishing", True),
            ("Dedicated project manager", True),
            ("Post-launch support period (30 days)", True),
        ],
    ),
    dict(
        slug="custom", name="Enterprise", display_order=4,
        tagline="Large-scale platforms, systems integration and ongoing engineering partnerships.",
        project_price=None, maintenance_monthly=None,
        maintenance_note="Custom SLA with 24/7 support available.",
        delivery_time="Scoped per project", is_featured=False, eyebrow_text="Enterprise",
        custom_price_label="Let's Talk",
        cta_text="Request a Quote →",
        features=[
            ("Dedicated engineering team", True),
            ("Complex multi-system & legacy integrations", True),
            ("Technology consulting & architecture review", True),
            ("Custom SLA with 24/7 support", True),
            ("Weekly sprint demos & reporting", True),
            ("Security audit & compliance guidance", True),
        ],
    ),
]

FAQS = [
    ("How is pricing structured?",
     "Every project has a one-time price covering design, development, testing and launch. "
     "The prices shown are starting points; after a free discovery call you get a fixed written quote. "
     "Monthly fees are only for optional maintenance after launch."),
    ("How do payments work?",
     "Typically 50% upfront to start, and 50% on delivery. Larger projects are split into milestones. "
     "We accept M-Pesa, bank transfer and card, and issue invoices for every payment."),
    ("What does the monthly maintenance cover?",
     "Hosting care, backups, security updates, uptime monitoring, bug fixes and a set number of hours "
     "for small improvements. It's optional, and you can cancel any time with 30 days' notice."),
    ("Do I own the code and assets?",
     "Yes, 100%. On final payment all source code, designs and intellectual property transfer to you, "
     "and we sign an IP transfer agreement on every project."),
    ("Are hosting, domain and third-party costs included?",
     "Domain, hosting and paid third-party services (SMS, payment gateway fees, app-store accounts) are billed "
     "at cost, with no markup. We'll list them in your quote so there are no surprises."),
    ("How long does a project take?",
     "A business website takes 1-2 weeks, a custom web platform 4-8 weeks and a mobile app 8-16 weeks. "
     "You get a dated timeline in your quote and weekly progress updates."),
    ("What technologies do you work with?",
     "Mainly Django and Python for backends and APIs, React and React Native for web and mobile, and PostgreSQL, "
     "with deep experience integrating M-Pesa Daraja. We choose the right tool for the job."),
]


def forwards(apps, schema_editor):
    PricingPlan = apps.get_model("Home", "PricingPlan")
    PricingFeature = apps.get_model("Home", "PricingFeature")
    PricingFAQ = apps.get_model("Home", "PricingFAQ")

    for spec in PLANS:
        spec = dict(spec)
        features = spec.pop("features")
        for k in ("project_price", "maintenance_monthly"):
            if spec[k] is not None:
                spec[k] = Decimal(spec[k])
        slug = spec.pop("slug")
        plan, _ = PricingPlan.objects.update_or_create(slug=slug, defaults=dict(currency_symbol="KES", **spec))
        plan.features.all().delete()
        for i, (text, included) in enumerate(features):
            PricingFeature.objects.create(plan=plan, text=text, is_included=included, display_order=i)

    PricingFAQ.objects.filter(question__in=OLD_FAQ_QUESTIONS).delete()
    existing = set(PricingFAQ.objects.values_list("question", flat=True))
    for i, (q, a) in enumerate(FAQS):
        if q not in existing:
            PricingFAQ.objects.create(question=q, answer=a, display_order=i)

    # Historical models don't fire the cache-clearing signals, so drop the
    # cached pricing context here or the old plans stay served until it expires.
    from django.core.cache import cache
    cache.delete("pricing_page_context")


class Migration(migrations.Migration):

    dependencies = [
        ("Home", "0007_alter_portfolioproject_cover_image"),
    ]

    operations = [
        migrations.RemoveField(model_name="pricingplan", name="annual_price"),
        migrations.RenameField(model_name="pricingplan", old_name="monthly_price", new_name="project_price"),
        migrations.AlterField(
            model_name="pricingplan", name="project_price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=12, null=True,
                help_text="One-time project price ('starting from'). Leave blank for a 'Let's Talk' / custom-quote plan"),
        ),
        migrations.AddField(
            model_name="pricingplan", name="maintenance_monthly",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True,
                help_text="Optional monthly maintenance / care plan price. Blank hides the maintenance line."),
        ),
        migrations.AddField(
            model_name="pricingplan", name="maintenance_note",
            field=models.CharField(
                blank=True, default="", max_length=200,
                help_text="What the monthly maintenance covers, e.g. 'Hosting, backups, security updates, 2 hrs of changes'"),
        ),
        migrations.AddField(
            model_name="pricingplan", name="delivery_time",
            field=models.CharField(
                blank=True, default="", max_length=60,
                help_text="Typical delivery time, e.g. '2-3 weeks'"),
        ),
        migrations.AlterField(
            model_name="pricingplan", name="currency_symbol",
            field=models.CharField(default="KES", max_length=4),
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
