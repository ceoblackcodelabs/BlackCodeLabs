"""Upsert the Services and Solutions in scripts/content/offerings.json.

    python manage.py seed_offerings --dry-run     # validate + show what would change
    python manage.py seed_offerings               # apply
    python manage.py seed_offerings --file other.json

Idempotent: services are matched by name (case-insensitive), solutions by slug.
Uses the same validation as the content API (Home/api.py). Saves go through the ORM,
so the signals clear the home-page cache.
"""
import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from Home import api
from Home.models import Solution, TechServices


class Command(BaseCommand):
    help = "Create or update the CCTV / access control / design / IT services and solutions."

    def add_arguments(self, parser):
        parser.add_argument("--file", default=str(Path(settings.BASE_DIR) / "scripts" / "content" / "offerings.json"))
        parser.add_argument("--dry-run", action="store_true", help="Validate and report without saving")

    def handle(self, *args, **opts):
        path = Path(opts["file"])
        try:
            data = json.loads(path.read_text())
        except (OSError, ValueError) as exc:
            raise CommandError(f"Cannot read {path}: {exc}")

        # Validate everything first so a typo can't leave a half-applied update.
        services, solutions = [], []
        try:
            for item in data.get("services", []):
                services.append(api._clean(item, api.SERVICE_SPEC, partial=False))
            for item in data.get("solutions", []):
                solutions.append(api._solution_fields(item, partial=False))
        except api.ApiError as exc:
            raise CommandError(f"Invalid content: {exc} {exc.errors or ''}")

        dry = opts["dry_run"]
        counts = {"created": 0, "updated": 0}
        with transaction.atomic():
            for f in services:
                obj = TechServices.objects.filter(name__iexact=f["name"]).first()
                self._report("service", f["name"], obj is None, counts)
                if not dry:
                    if obj:
                        for k, v in f.items():
                            setattr(obj, k, v)
                        obj.save()
                    else:
                        TechServices.objects.create(**f)

            for f in solutions:
                f = dict(f)
                slug = f.pop("slug", "") or slugify(f["title"])[:50]
                exists = Solution.objects.filter(pk=slug).exists()
                self._report("solution", slug, not exists, counts)
                if not dry:
                    obj, created = Solution.objects.get_or_create(slug=slug, defaults=f)
                    if not created:
                        for k, v in f.items():
                            setattr(obj, k, v)
                        obj.save()

        verb = "Would apply" if dry else "Done"
        self.stdout.write(self.style.SUCCESS(f"{verb}: {counts['created']} new, {counts['updated']} existing updated."))

    def _report(self, kind, label, is_new, counts):
        counts["created" if is_new else "updated"] += 1
        self.stdout.write(f"  {'create' if is_new else 'update'}  {kind:<9} {label}")
