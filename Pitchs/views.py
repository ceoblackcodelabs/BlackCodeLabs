from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Project
from .forms import ProjectRequestForm

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/index.html'
    context_object_name = 'projects'
    
    def get_queryset(self):
        return Project.objects.filter(is_available=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProjectRequestForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = ProjectRequestForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(
                request, 
                'Your project request has been submitted successfully! We\'ll contact you within 24 hours.'
            )
            return redirect('project_list')
        
        # If form is invalid, re-render the page with errors
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

class ProjectRequestCreateView(CreateView):
    model = Project
    form_class = ProjectRequestForm
    template_name = 'projects/index.html'
    success_url = reverse_lazy('project_list')
    
    def form_valid(self, form):
        messages.success(
            self.request,
            'Your project request has been submitted successfully! We\'ll contact you within 24 hours.'
        )
        return super().form_valid(form)