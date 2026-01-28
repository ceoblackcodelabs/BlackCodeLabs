from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = "Home/index.html"
    
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