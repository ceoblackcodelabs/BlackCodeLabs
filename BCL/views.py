from django.views.generic import ListView
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.shortcuts import redirect
from .models import ContactSettings, ContactMessage, AboutSection, Merch

class landing(ListView):
    template_name = 'BCL/index.html'
    model = ContactMessage
    context_object_name = "testimonials"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add contact settings to template
        context['settings'] = ContactSettings.get_settings()
        about_section = AboutSection.objects.first()
        context['about_section_img'] = about_section.image if about_section else None
        context['about_section_video'] = about_section.video if about_section else None

        # merch
        context['merch_items'] = Merch.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            # Send auto-reply email if enabled
            # settings = ContactSettings.get_settings()
            # if settings.auto_reply_enabled:
            #     send_mail(
            #         subject=settings.auto_reply_subject,
            #         message=settings.auto_reply_message,
            #         from_email=settings.email_general,
            #         recipient_list=[contact_message.email],
            #         fail_silently=True,
            #     )
            messages.success(request, "Your message has been sent successfully!")
            return redirect(reverse_lazy('landing'))
        else:
            messages.error(request, "There was an error with your submission. Please check the form and try again.")
            return self.get(request, *args, **kwargs)


    def send_admin_notification(self, message):
        pass