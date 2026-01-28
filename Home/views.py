from django.views.generic import TemplateView, ListView
from .models import (
    TechServices, TeamMember, DataCounter,
    ClientReview
)

class HomePageView(ListView):
    template_name = "Home/index.html"
    model = TechServices
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tech_services'] = TechServices.objects.all()
        context['team_members'] = TeamMember.objects.all()
        data_counter = DataCounter.objects.filter(is_active=True).first()
        if not data_counter:
            # Create a default counter if none exists
            data_counter = DataCounter.objects.create(
                projects_delivered=1247,
                systems_automated=892,
                happy_clients=765,
                returning_clients=423,
                is_active=True
            )
        context['data_counters'] = data_counter
        context["client_reviews"] = ClientReview.objects.all()[:6]
        return context
    
class AboutPageView(TemplateView):
    template_name = "Home/about.html"

class ContactPageView(TemplateView):
    template_name = "Home/contact.html"
    
class TechPageView(TemplateView):
    template_name = "Home/tech.html"
    
class SolutionsPageView(TemplateView):
    template_name = "Home/solutions.html"
    
class CoursesPageView(TemplateView):
    template_name = "Home/courses.html"
    
class CareersPageView(TemplateView):
    template_name = "Home/careers.html"
    
class BlogPageView(TemplateView):
    template_name = "Home/blog.html"
    
class GamesPageView(TemplateView):
    template_name = "Home/games.html"
    
class ContactsPageView(TemplateView):
    template_name = "Home/contacts.html"

class DemoPageView(TemplateView):
    template_name = "Home/demo.html"