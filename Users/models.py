from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ACCOUNT_TYPE_CHOICES = [
        ('Seeker', 'Seeker / Job Seeker'),
        ('Employer', 'Employer / Recruiter'),
        ('Developer', 'Developer / Admin'),
    ]

    # Keep username but make email required and unique
    email = models.EmailField(unique=True, verbose_name='Email Address')
    contact = models.CharField(max_length=13, default="+2547")
    # Add custom fields
    full_name = models.CharField(max_length=255, verbose_name='Full Name')
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        verbose_name='Account Type',
        blank=True,
        null=True
    )
    agree_terms = models.BooleanField(default=False, verbose_name='Agreed to Terms')

    # Set the ordering field for admin
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    def __str__(self):
        return self.email

class SeekerProfile(models.Model):
    TRADE_CHOICES = [
        ('electrician', 'Electrician'),
        ('welder', 'Welder'),
        ('plumber', 'Plumber'),
        ('carpenter', 'Carpenter'),
        ('hvac', 'HVAC Technician'),
        ('operator', 'Heavy Equipment Operator'),
        ('mechanic', 'Mechanic'),
        ('other', 'Other'),
    ]

    EXPERIENCE_LEVELS = [
        ('0-2', 'Entry Level (0-2 years)'),
        ('3-5', 'Mid Level (3-5 years)'),
        ('5-10', 'Senior Level (5-10 years)'),
        ('10+', 'Expert Level (10+ years)'),
    ]

    STATUS_CHOICE = [
        ('seeking', 'Seeking'),
        ('employed', 'Employed'),
        ('freelancing', 'Freelancing'),
        ('idle', 'Idle')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seeker_profile')
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    pfp = models.ImageField(upload_to="SeekerPfp", default="SeekerPfp/default.jpg")
    primary_trade = models.CharField(max_length=20, choices=TRADE_CHOICES)
    years_experience = models.CharField(max_length=5, choices=EXPERIENCE_LEVELS)
    location = models.CharField(max_length=255, blank=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    availability = models.CharField(max_length=20, default='seeking', choices=STATUS_CHOICE)
    profile_completion = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.get_primary_trade_display()}"

    @property
    def user_description(self):
        """Generate a dynamic, natural-sounding summary paragraph for the profile."""
        trade = self.get_primary_trade_display()
        experience = self.get_years_experience_display().replace("(", "").replace(")", "")
        location = self.location or "various regions"

        # Grab top 3 verified certifications
        certs = self.certifications.filter(status='verified')[:2]
        cert_list = ", ".join([c.name for c in certs])

        # Grab top 3 skills
        skills = self.skills.all()[:3]
        skill_list = ", ".join([s.skill.name for s in skills])

        # Include last or current job if available
        last_job = self.work_experience.order_by('-start_date').first()
        job_part = ""
        if last_job:
            company = last_job.company
            position = last_job.position
            if last_job.current:
                job_part = f" Currently employed at {company} as a {position}."
            else:
                job_part = f" Previously worked at {company} as a {position}."

        # Start building description
        description = f"{self.user.full_name or 'This professional'} is a {trade.lower()} with {experience.lower()} of experience in {location}."

        if cert_list:
            description += f" Certified in {cert_list}."

        description += job_part

        # Add availability info
        if self.availability == "seeking":
            description += " Currently open to new opportunities."
        elif self.availability == "freelancing":
            description += " Available for freelance or contract projects."
        elif self.availability == "employed":
            description += " Actively employed but open to career growth."
        else:
            description += " Exploring new avenues for professional development."

        return description


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class SeekerSkill(models.Model):
    PROFIENCY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    profile = models.ForeignKey(SeekerProfile, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency = models.CharField(max_length=15, choices=PROFIENCY_LEVELS, default='intermediate')
    years_experience = models.IntegerField(default=1)

    class Meta:
        unique_together = ['profile', 'skill']

class Certification(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    profile = models.ForeignKey(SeekerProfile, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    document = models.FileField(upload_to='certifications/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.profile.user.full_name}"

class ToolProficiency(models.Model):
    profile = models.ForeignKey(SeekerProfile, on_delete=models.CASCADE, related_name='tools')
    tool_name = models.CharField(max_length=100)
    proficiency_level = models.CharField(max_length=15, choices=SeekerSkill.PROFIENCY_LEVELS, default='intermediate')

    class Meta:
        unique_together = ['profile', 'tool_name']

class Specialization(models.Model):
    profile = models.ForeignKey(SeekerProfile, on_delete=models.CASCADE, related_name='specializations')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ['profile', 'name']

class Review(models.Model):
    STARS = [
        ('ONE_STAR', 'ONE_STAR'),
        ('TWO_STAR', 'TWO_STAR'),
        ('THREE_STAR', 'THREE_STAR'),
        ('FOUR_STAR', 'FOUR_STAR'),
        ('FIVE_STAR', 'FIVE_STAR'),
    ]
    profile = models.ForeignKey(SeekerProfile, on_delete=models.CASCADE, related_name='review', null=True, blank=True)
    ratings = models.CharField(max_length=20, default="THREE_STAR", choices=STARS)
    teamwork = models.FloatField(default=0.0)
    time_management = models.FloatField(default=0.0)
    critical_thinking = models.FloatField(default=0.0)
    leadership = models.FloatField(default=0.0)
    Communication = models.FloatField(default=0.0)

    def __str__(self):
        return self.profile.user.full_name

class WorkExperience(models.Model):
    profile = models.ForeignKey(SeekerProfile, on_delete=models.CASCADE, related_name='work_experience')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="workExperience", null=True, blank=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name="thecompany", null=True, blank=True)
    role = models.CharField(max_length=100, default="")
    position = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    my_description = models.CharField(max_length=300, default="")
    employer_description = models.CharField(max_length=300, default="")
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.position} at {self.company}"

# premium feature
PROJECT_TYPE = [
    {'online', 'Online'},
    {'offline', 'Offline'},
    {'hybrid', 'Hybrid'},
    {'contract', 'Contract'},
]

class CompanyReview(models.Model):
    company_name = models.ForeignKey('Company', on_delete=models.CASCADE, null=True)
    review_text = models.TextField(default="")
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.company_name.name

class Company(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default="")
    industry = models.CharField(max_length=200, default="")
    location = models.CharField(max_length=200, default="")
    review = models.ForeignKey(CompanyReview, on_delete=models.CASCADE, null=True, blank=True)
    website = models.URLField(max_length=200, default="", null=True, blank=True)
    description = models.TextField(default="", blank=True)
    email = models.EmailField(max_length=255, blank=True, default="")
    phone = models.CharField(max_length=20, blank=True, default="")

    def __str__(self):
        return self.name

Availanility_CHOICES = [
    ('FT', 'Full-Time'),
    ('PT', 'Part-Time'),
    ('CT', 'Contract'),
    ('IN', 'Internship'),
]

requirements_CHOICES = [
    ('HS', 'High School Diploma'),
    ('AD', 'Associate Degree'),
    ('BD', 'Bachelor\'s Degree'),
    ('MD', 'Master\'s Degree'),
    ('PHD', 'Doctorate'),
]

class DmFromResume(models.Model):
    name = models.CharField(max_length=255, default="")
    email = models.EmailField(max_length=255, default="")
    talent = models.ForeignKey(SeekerProfile, on_delete=models.CASCADE, related_name="received_messages", null=True, blank=True)
    subject = models.CharField(max_length=100, default="Checking Availabilty To Hire")
    location = models.TextField(default="")
    contact = models.CharField(max_length=20, default="")
    link = models.URLField(max_length=200, default="", null=True, blank=True)
    project_type = models.CharField(max_length=50, default='hybrid', choices=PROJECT_TYPE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    description = models.TextField(default="")