# """
# core/models.py

# Singleton-style models for site-wide settings and the homepage.
# """

# from django.db import models
# from django.core.exceptions import ValidationError


# class SingletonModel(models.Model):
#     """
#     Abstract base that enforces a single database row.
#     Useful for site-wide settings / hero content that should only
#     ever have one record.
#     """

#     class Meta:
#         abstract = True

#     def save(self, *args, **kwargs):
#         self.pk = 1
#         super().save(*args, **kwargs)

#     def delete(self, *args, **kwargs):
#         pass  # Prevent deletion of the singleton

#     @classmethod
#     def load(cls):
#         obj, _ = cls.objects.get_or_create(pk=1)
#         return obj


# # ─── Site Settings (singleton) ────────────────────────────────────────────────

# class SiteSettings(SingletonModel):
#     """Global settings rendered across every page."""

#     site_name        = models.CharField(max_length=100, default='Urban Theory')
#     tagline          = models.CharField(max_length=200, default='Innovation and movement converge to overcome the boundaries of communication.')
#     founded_year     = models.PositiveSmallIntegerField(default=2018)
#     base_city        = models.CharField(max_length=80, default='Milan')

#     # Contact
#     email_general    = models.EmailField(default='info@urbantheory.com')
#     email_booking    = models.EmailField(default='booking@urbantheory.com')
#     phone            = models.CharField(max_length=30, default='+39 012 345 6789')
#     address_line1    = models.CharField(max_length=100, default='Via Milano 42')
#     address_line2    = models.CharField(max_length=100, default='20121 Milan, Italy')

#     # Social links
#     instagram_url    = models.URLField(blank=True)
#     tiktok_url       = models.URLField(blank=True)
#     youtube_url      = models.URLField(blank=True)
#     facebook_url     = models.URLField(blank=True)

#     # Footer
#     footer_about     = models.TextField(
#         default='Urban Theory is a dance collective pushing the boundaries of '
#                 'movement, art, and visual storytelling. Based in Milan, performing worldwide.'
#     )
#     powered_by       = models.CharField(max_length=100, default='blackcodelabs')

#     class Meta:
#         verbose_name        = 'Site Settings'
#         verbose_name_plural = 'Site Settings'

#     def __str__(self):
#         return 'Site Settings'


# # ─── Hero Section (singleton) ─────────────────────────────────────────────────

# class HeroContent(SingletonModel):
#     """Controls the hero / landing section."""

#     eyebrow   = models.CharField(
#         max_length=100, default='Milan · Est. 2018',
#         help_text='Small text above the logo, e.g. "Milan · Est. 2018"',
#     )
#     headline  = models.CharField(max_length=100, default='Urban Theory')
#     subtext   = models.TextField(
#         default='Innovation and movement converge to overcome the boundaries of communication.',
#         help_text='Paragraph under the headline.',
#     )
#     cta_primary_label = models.CharField(max_length=50, default='Explore')
#     cta_primary_url   = models.CharField(max_length=200, default='#what-we-do')
#     cta_outline_label = models.CharField(max_length=50, default='Work With Us')
#     cta_outline_url   = models.CharField(max_length=200, default='#contact')

#     class Meta:
#         verbose_name        = 'Hero Content'
#         verbose_name_plural = 'Hero Content'

#     def __str__(self):
#         return 'Hero Content'


# # ─── Social / Community Stats ─────────────────────────────────────────────────

# class SocialStat(models.Model):
#     """
#     Each row is one stat shown in the marquee strip and/or community section.
#     e.g. "2.5M Followers", "21M Likes".
#     """

#     label       = models.CharField(max_length=80, help_text='e.g. "Followers"')
#     value       = models.CharField(max_length=20, help_text='Display value, e.g. "2.5M"')
#     raw_value   = models.BigIntegerField(
#         null=True, blank=True,
#         help_text='Numeric value used for the animated counter (optional).',
#     )
#     show_in_marquee   = models.BooleanField(default=True)
#     show_in_community = models.BooleanField(default=False,
#         help_text='If True, this stat drives the big animated counter.',
#     )
#     order       = models.PositiveSmallIntegerField(default=0)

#     class Meta:
#         ordering            = ['order']
#         verbose_name        = 'Social Stat'
#         verbose_name_plural = 'Social Stats'

#     def __str__(self):
#         return f'{self.value} {self.label}'


# # ─── "Perspective Matters" Section ────────────────────────────────────────────

# class PerspectiveSection(SingletonModel):
#     """The large typographic 'PERSPECTIVE MATTERS' section."""

#     line1   = models.CharField(max_length=100, default='PERSPECTIVE')
#     line2   = models.CharField(max_length=100, default='MATTERS')
#     subtext = models.TextField(
#         default='Where movement becomes message. Where bodies become billboards. Where culture shifts.',
#         blank=True,
#     )

#     class Meta:
#         verbose_name        = 'Perspective Section'
#         verbose_name_plural = 'Perspective Section'

#     def __str__(self):
#         return f'{self.line1} / {self.line2}'


# # ─── Service (What We Do) ─────────────────────────────────────────────────────

# class Service(models.Model):
#     """One card in the 'What We Do' grid."""

#     title       = models.CharField(max_length=100)
#     description = models.TextField()
#     image       = models.ImageField(
#         upload_to='services/',
#         null=True, blank=True,
#         help_text='Upload a high-quality image (min 800 × 640 px recommended).',
#     )
#     order       = models.PositiveSmallIntegerField(default=0, help_text='Display order (ascending).')
#     is_active   = models.BooleanField(default=True)

#     class Meta:
#         ordering            = ['order']
#         verbose_name        = 'Service'
#         verbose_name_plural = 'Services'

#     def __str__(self):
#         return self.title

#     @property
#     def number_display(self):
#         """Return zero-padded display number, e.g. 01, 02."""
#         return f'{self.order:02d}'

# """
# merchandise/models.py
# """

# from django.db import models
# from django.utils.text import slugify


# class MerchCategory(models.Model):
#     """Optional grouping: Tops, Accessories, Outerwear, etc."""

#     name  = models.CharField(max_length=80, unique=True)
#     slug  = models.SlugField(max_length=80, unique=True, blank=True)
#     order = models.PositiveSmallIntegerField(default=0)

#     class Meta:
#         ordering            = ['order', 'name']
#         verbose_name        = 'Merch Category'
#         verbose_name_plural = 'Merch Categories'

#     def __str__(self):
#         return self.name

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.name)
#         super().save(*args, **kwargs)


# class MerchItem(models.Model):
#     """A single merchandise product."""

#     STATUS_COMING_SOON = 'coming_soon'
#     STATUS_AVAILABLE   = 'available'
#     STATUS_SOLD_OUT    = 'sold_out'

#     STATUS_CHOICES = [
#         (STATUS_COMING_SOON, 'Coming Soon'),
#         (STATUS_AVAILABLE,   'Available'),
#         (STATUS_SOLD_OUT,    'Sold Out'),
#     ]

#     name        = models.CharField(max_length=150)
#     slug        = models.SlugField(max_length=150, unique=True, blank=True)
#     category    = models.ForeignKey(
#         MerchCategory,
#         null=True, blank=True,
#         on_delete=models.SET_NULL,
#         related_name='items',
#     )
#     description = models.TextField(blank=True)
#     price       = models.DecimalField(
#         max_digits=8, decimal_places=2,
#         help_text='Price in euros.',
#     )
#     image       = models.ImageField(
#         upload_to='merchandise/',
#         null=True, blank=True,
#         help_text='Product image (min 600 × 700 px recommended).',
#     )
#     badge       = models.CharField(
#         max_length=30, blank=True,
#         help_text='Optional label shown on the card, e.g. "New" or "Limited".',
#     )
#     status      = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default=STATUS_COMING_SOON,
#     )
#     is_published = models.BooleanField(
#         default=True,
#         help_text='Unpublished items are hidden from the website.',
#     )
#     order       = models.PositiveSmallIntegerField(default=0)
#     created_at  = models.DateTimeField(auto_now_add=True)
#     updated_at  = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering            = ['order', 'name']
#         verbose_name        = 'Merch Item'
#         verbose_name_plural = 'Merch Items'

#     def __str__(self):
#         return self.name

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.name)
#         super().save(*args, **kwargs)

#     @property
#     def price_display(self):
#         """Returns '€89' with no decimals if the price is a whole number."""
#         if self.price == int(self.price):
#             return f'€{int(self.price)}'
#         return f'€{self.price:.2f}'

#     @property
#     def is_available(self):
#         return self.status == self.STATUS_AVAILABLE