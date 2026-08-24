from django.db import migrations

URLS = {
    "votehub-awards-platform": "https://example.com/votehub-demo",
    "careerforge-ats": "https://example.com/careerforge-demo",
}


def seed_urls(apps, schema_editor):
    PortfolioProject = apps.get_model("Home", "PortfolioProject")
    for slug, url in URLS.items():
        PortfolioProject.objects.filter(slug=slug, project_url="").update(project_url=url)


def unseed_urls(apps, schema_editor):
    PortfolioProject = apps.get_model("Home", "PortfolioProject")
    PortfolioProject.objects.filter(slug__in=URLS.keys()).update(project_url="")


class Migration(migrations.Migration):

    dependencies = [
        ("Home", "0004_portfolioproject_home_portfo_is_acti_b01049_idx_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_urls, unseed_urls),
    ]
