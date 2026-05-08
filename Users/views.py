# Users/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, DetailView
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
import json
from django.views import View
from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from utils.qrgen import generate_vcard_qr_code

from .forms import (
    RegisterForm, EmailLoginForm, SeekerProfileForm,
    SkillForm, CertificationForm, ToolProficiencyForm,
    SpecializationForm, ContactTalentForm
)
from .models import (
    User, SeekerProfile, SeekerSkill,
    Certification, ToolProficiency, Specialization,
    Skill, Review, DmFromResume, Company, WorkExperience
)

User = get_user_model()

# ============= AUTHENTICATION VIEWS =============

def auth_view(request):
    # Initialize both forms at the beginning
    register_form = RegisterForm()
    login_form = EmailLoginForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'register':
            register_form = RegisterForm(request.POST)
            login_form = EmailLoginForm()  # Keep login form empty

            if register_form.is_valid():
                user = register_form.save()
                messages.success(request, 'Account created successfully! Please log in.')
                return redirect('authenticate')
            else:
                # Add form errors to messages
                for field, errors in register_form.errors.items():
                    for error in errors:
                        if field == '__all__':
                            messages.error(request, error)
                        else:
                            messages.error(request, f'{field}: {error}')

        elif form_type == 'login':
            login_form = EmailLoginForm(request, data=request.POST)
            register_form = RegisterForm()  # Keep register form empty

            if login_form.is_valid():
                email = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(request, username=email, password=password)

                if user is not None:
                    if user.is_active:
                        login(request, user)
                        messages.success(request, f'Welcome back, {user.full_name}!')
                        return redirect('home')
                    else:
                        messages.error(request, 'Your account is not active. Please check your email.')
                else:
                    messages.error(request, 'Invalid email or password.')
            else:
                # Add form errors to messages
                for field, errors in login_form.errors.items():
                    for error in errors:
                        if field == '__all__':
                            messages.error(request, error)
                        else:
                            messages.error(request, f'{field}: {error}')

    # Always render with both forms
    return render(request, 'Users/auth.html', {
        'register_form': register_form,
        'login_form': login_form
    })

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been verified successfully!')
        return redirect('home')
    else:
        messages.error(request, 'Activation link is invalid or expired.')
        return redirect('authenticate')


class UserLogoutView(LogoutView):
    """User logout view"""
    next_page = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)

class UserProfileView(LoginRequiredMixin, DetailView):
    template_name = 'users/myProfile.html'
    model = SeekerProfile
    context_object_name = 'seeker'

    def get_object(self, queryset=None):
        # Return the SeekerProfile, not the User
        profile, created = SeekerProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object  # This is now a SeekerProfile object
        user = self.request.user

        # Get all related data (using profile directly)
        skills = SeekerSkill.objects.filter(profile=profile)
        certifications = Certification.objects.filter(profile=profile)
        tools = ToolProficiency.objects.filter(profile=profile)
        specializations = Specialization.objects.filter(profile=profile)
        experience = WorkExperience.objects.filter(profile=profile)
        ratings = Review.objects.filter(profile=profile)  # Fixed: remove username lookup

        # Calculate average ratings (you likely want to aggregate, not overwrite)
        rating_data = {
            'tm': 0,
            'tw': 0,
            'com': 0,
            'ct': 0,
            'lead': 0,
            'star': 0
        }

        if ratings.exists():
            rating_data['tm'] = ratings.aggregate(Avg('time_management'))['time_management__avg'] or 0
            rating_data['tw'] = ratings.aggregate(Avg('teamwork'))['teamwork__avg'] or 0
            rating_data['com'] = ratings.aggregate(Avg('Communication'))['Communication__avg'] or 0
            rating_data['ct'] = ratings.aggregate(Avg('critical_thinking'))['critical_thinking__avg'] or 0
            rating_data['lead'] = ratings.aggregate(Avg('leadership'))['leadership__avg'] or 0
            rating_data['star'] = ratings.aggregate(Avg('ratings'))['ratings__avg'] or 0

        context.update(rating_data)

        # Rest of your code remains the same...
        available_skills = Skill.objects.exclude(
            id__in=skills.values_list('skill_id', flat=True)
        )[:10]

        # Generate QR code (now profile is SeekerProfile)
        try:
            qr_code_data = generate_vcard_qr_code(profile)  # Pass profile, not self.object
            print(f"QR code data length: {len(qr_code_data) if qr_code_data else 'None'}")
        except Exception as e:
            print(f"Error in view generating QR: {e}")
            qr_code_data = None

        context.update({
            'profile': profile,
            'skills': skills,
            'certifications': certifications,
            'tools': tools,
            'specializations': specializations,
            'qr_code_data': qr_code_data,
            'available_skills': available_skills,
            'experiences': experience,
            'ratings': ratings
        })

        return context


class BuildProfile(LoginRequiredMixin, TemplateView):
    template_name = 'users/build_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get or create seeker profile
        profile, created = SeekerProfile.objects.get_or_create(user=user)

        # Calculate profile completion
        completion_percentage = self.calculate_profile_completion(profile)
        profile.profile_completion = completion_percentage
        profile.save()

        # Get all related data
        skills = SeekerSkill.objects.filter(profile=profile)
        certifications = Certification.objects.filter(profile=profile)
        tools = ToolProficiency.objects.filter(profile=profile)
        specializations = Specialization.objects.filter(profile=profile)

        # Get available skills for suggestions
        available_skills = Skill.objects.exclude(
            id__in=skills.values_list('skill_id', flat=True)
        )[:10]

        context.update({
            'profile': profile,
            'skills': skills,
            'certifications': certifications,
            'tools': tools,
            'specializations': specializations,
            'available_skills': available_skills,
            'profile_form': SeekerProfileForm(instance=profile),
            'skill_form': SkillForm(),
            'certification_form': CertificationForm(),
            'tool_form': ToolProficiencyForm(initial={
                'tools': list(tools.values_list('tool_name', flat=True))
            }),
            'specialization_form': SpecializationForm(initial={
                'specializations': list(specializations.values_list('name', flat=True))
            }),
        })

        return context

    def calculate_profile_completion(self, profile):
        total_points = 0
        earned_points = 0

        # Basic info (25 points)
        total_points += 25
        if profile.primary_trade and profile.years_experience and profile.pfp:
            earned_points += 25
        elif profile.primary_trade and profile.years_experience:
            earned_points += 20  # Partial points if profile picture is missing

        # Skills (25 points)
        total_points += 25
        if SeekerSkill.objects.filter(profile=profile).exists():
            earned_points += 25

        # Certifications (20 points)
        total_points += 20
        if Certification.objects.filter(profile=profile).exists():
            earned_points += 20

        # Work experience (20 points)
        total_points += 20
        # This would be added when work experience model is implemented
        # if WorkExperience.objects.filter(profile=profile).exists():
        #     earned_points += 20

        # Tools and specializations (10 points)
        total_points += 10
        if (ToolProficiency.objects.filter(profile=profile).exists() or
            Specialization.objects.filter(profile=profile).exists()):
            earned_points += 10

        return int((earned_points / total_points) * 100) if total_points > 0 else 0

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(SeekerProfile, user=request.user)
        section = request.POST.get('section')

        if section == 'basic_info':
            form = SeekerProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Basic information updated successfully!')
            else:
                messages.error(request, 'Please correct the errors below.')

        elif section == 'skills':
            # Handle the main form submission (including experience levels)
            try:
                # Handle profile picture upload
                if 'pfp' in request.FILES:
                    profile.pfp = request.FILES['pfp']

                # Update primary trade
                primary_trade = request.POST.get('primary_trade')
                if primary_trade:
                    profile.primary_trade = primary_trade

                # Update years of experience
                years_experience = request.POST.get('years_experience')
                if years_experience:
                    profile.years_experience = years_experience

                # Update location if provided
                location = request.POST.get('location')
                if location:
                    profile.location = location

                # Update availability
                profile.availability = 'availability' in request.POST

                # Save profile changes
                profile.save()

                # Handle tools
                selected_tools = request.POST.getlist('tools', [])
                with transaction.atomic():
                    # Remove existing tools
                    ToolProficiency.objects.filter(profile=profile).delete()
                    # Add new tools
                    for tool in selected_tools:
                        ToolProficiency.objects.create(
                            profile=profile,
                            tool_name=tool,
                            proficiency_level='intermediate'
                        )

                # Handle specializations
                selected_specializations = request.POST.getlist('specializations', [])
                with transaction.atomic():
                    # Remove existing specializations
                    Specialization.objects.filter(profile=profile).delete()
                    # Add new specializations
                    for specialization in selected_specializations:
                        Specialization.objects.create(
                            profile=profile,
                            name=specialization
                        )

                messages.success(request, 'Profile updated successfully!')

            except Exception as e:
                messages.error(request, f'Error updating profile: {str(e)}')

        elif section == 'certifications':
            # Handle certification creation
            form = CertificationForm(request.POST, request.FILES)
            if form.is_valid():
                certification = form.save(commit=False)
                certification.profile = profile
                certification.save()
                messages.success(request, 'Certification added successfully!')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')

        return redirect('build_profile')

# Add these views for handling AJAX requests
class AddSkillView(LoginRequiredMixin, View):
    def post(self, request):
        skill_name = request.POST.get('skill_name')
        skill_id = request.POST.get('skill_id')

        if skill_id:
            # Add existing skill by ID
            try:
                skill = Skill.objects.get(id=skill_id)
                profile = get_object_or_404(SeekerProfile, user=request.user)
                seeker_skill, created = SeekerSkill.objects.get_or_create(
                    profile=profile,
                    skill=skill,
                    defaults={
                        'proficiency': 'intermediate',
                        'years_experience': 1
                    }
                )
                return JsonResponse({'success': True, 'skill_id': skill.id})
            except Skill.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Skill not found'})

        elif skill_name:
            # Create new skill
            skill, created = Skill.objects.get_or_create(
                name=skill_name,
                defaults={'category': 'general'}
            )
            profile = get_object_or_404(SeekerProfile, user=request.user)
            seeker_skill, created = SeekerSkill.objects.get_or_create(
                profile=profile,
                skill=skill,
                defaults={
                    'proficiency': 'intermediate',
                    'years_experience': 1
                }
            )
            return JsonResponse({'success': True, 'skill_id': skill.id})

        return JsonResponse({'success': False, 'error': 'No skill name or ID provided'})

class RemoveSkillView(LoginRequiredMixin, View):
    def post(self, request, skill_id):
        profile = get_object_or_404(SeekerProfile, user=request.user)
        try:
            SeekerSkill.objects.filter(profile=profile, skill_id=skill_id).delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

class DeleteCertificationView(LoginRequiredMixin, View):
    def post(self, request, cert_id):
        try:
            certification = get_object_or_404(Certification, id=cert_id, profile__user=request.user)
            certification.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

# Add a view to handle profile picture removal
class RemoveProfilePictureView(LoginRequiredMixin, View):
    def post(self, request):
        profile = get_object_or_404(SeekerProfile, user=request.user)
        try:
            # Set to default profile picture
            profile.pfp = "SeekerPfp/default.jpg"
            profile.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

class MyResume(TemplateView):
    template_name = 'Seekers/resume.html'

class ResumeBuilder(TemplateView):
    template_name = 'Seekers/resume_builder.html'

class TalentDetailView(LoginRequiredMixin, DetailView):
    model = SeekerProfile
    context_object_name = "seeker"
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        certs = Certification.objects.filter(profile__user__username = self.object.user.username)
        skills = SeekerSkill.objects.filter(profile__user__username = self.object.user.username)
        experiences = WorkExperience.objects.filter(profile__user__username = self.object.user.username)
        ratings = Review.objects.filter(profile__user__username = self.object.user.username)
        for r in ratings:
            context.update({"tm": r.time_management})
            context.update({"tw": r.teamwork})
            context.update({"com": r.Communication})
            context.update({"ct": r.critical_thinking})
            context.update({"lead": r.leadership})
            context.update({"star": r.ratings})
        print(ratings)

        # Generate QR code
        try:
            qr_code_data = generate_vcard_qr_code(self.object)
            print(f"QR code data length: {len(qr_code_data) if qr_code_data else 'None'}")  # Debug
        except Exception as e:
            print(f"Error in view generating QR: {e}")  # Debug
            qr_code_data = None

        context.update({"certs": certs})
        context.update({"skills": skills})
        context.update({"experiences": experiences})
        context.update({"dmTalentForm": ContactTalentForm()})
        context.update({"qr_code_data": qr_code_data})
        context.update({"ratings": ratings})

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ContactTalentForm(request.POST)

        if form.is_valid():
            try:
                # Get the company associated with the logged-in user
                company = Company.objects.get(owner=request.user)
                talent = SeekerProfile.objects.get(pk=self.object.pk)

                dm_instance = form.save(commit=False)
                dm_instance.company = company
                dm_instance.talent = talent
                dm_instance.save()

                messages.success(request, 'Your message has been sent to the Talent.')
                return redirect('talent_resume', pk=self.object.pk)

            except Company.DoesNotExist:
                messages.error(request, 'You need to have a company profile to contact Talent.')
                return redirect('talent_resume', pk=self.object.pk)
        else:
            context = self.get_context_data()
            context['dmTalentForm'] = form
            return self.render_to_response(context)