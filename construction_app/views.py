from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, ListView
from django.views.generic.edit import UpdateView, DeleteView

from .models import Project, Material, DailyLog
from .forms import DailyLogForm, MaterialUsageFormSet, ProjectForm, MaterialForm


class Dashboard(TemplateView):
    template_name = "construction_app/dashboard.html"


class ProjectListView(ListView):
    model = Project
    template_name = "construction_app/project_list.html"
    context_object_name = "projects"  # název proměnné v šabloně


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "construction_app/project_form.html"
    success_url = reverse_lazy("projects")


class ProjectUpdateView(UpdateView):
    model = Project
    fields = ["name", "location", "start_date", "end_date", "status"]
    template_name = "construction_app/project_form.html"
    success_url = reverse_lazy("projects")


class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy("projects")

    def get(self, *args, **kwargs):
        # přímě přesměrování bez vykreslování šablony
        return self.post(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.success_url)


class MaterialListView(ListView):
    model = Material
    template_name = "construction_app/material_list.html"
    context_object_name = "materials"


class MaterialCreateView(CreateView):
    model = Material
    form_class = MaterialForm
    template_name = "construction_app/material_form.html"
    success_url = reverse_lazy("materials")


class MaterialUpdateView(UpdateView):
    model = Material
    fields = ["name", "quantity", "unit", "price"]
    template_name = "construction_app/material_form.html"
    success_url = reverse_lazy("materials")


class MaterialDeleteView(DeleteView):
    model = Material
    success_url = reverse_lazy("materials")

    def get(self, request, *args, **kwargs):
        """Přesměruje GET požadavky na přímé odstranění záznamu"""
        self.object = self.get_object()  # získání objekut, který bude smazán
        self.object.delete()
        return HttpResponseRedirect(self.success_url)

class DailyLogListView(ListView):
    model = DailyLog
    template_name = "construction_app/daily_log_list.html"
    context_object_name = "daily_logs"


class DailyLogCreateView(CreateView):
    model = DailyLog
    form_class = DailyLogForm
    template_name = "construction_app/daily_log_form.html"
    success_url = reverse_lazy("daily_logs")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["material_usage_formset"] = MaterialUsageFormSet(self.request.POST)
        else:
            context["material_usage_formset"] = MaterialUsageFormSet()
        context["daily_log_form"] = context["form"]
        return context

    def form_valid(self, form):
        daily_log = form.save(commit=False)
        context = self.get_context_data()
        material_usage_formset = context["material_usage_formset"]

        if material_usage_formset.is_valid():
            daily_log.save()
            material_usage_formset.instance = daily_log
            material_usage_formset.save()
            return reverse_lazy("daily_logs")

        return render(self.request, self.template_name, {
            "daily_log_form": form,
            "material_usage_formset": material_usage_formset
        })


class DailyLogUpdateView(UpdateView):
#     model = DailyLog
#     form_class = DailyLogForm
#     template_name = "construction_app/daily_log_form.html"
#     success_url = reverse_lazy("daily_logs")
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context["material_usage_formset"] = MaterialUsageFormSet(self.request.POST, instance=self.object)
#         else:
#             context["material_usage_formset"] = MaterialUsageFormSet(instance=self.object)
#         context["daily_log_form"] = context["form"]
#         return context
#
#     def form_valid(self, form):
#         daily_log = form.save(commit=False)
#         context = self.get_context_data()
#         material_usage_formset = context["material_usage_formset"]
#
#         if material_usage_formset.is_valid():
#             daily_log.save()
#             material_usage_formset.instance = daily_log
#             material_usage_formset.save()
#             return super().form_valid(form)
#
#         return render(self.request, self.template_name, {
#             "daily_log_form": form,
#             "material_usage_formset": material_usage_formset
#         })
    pass


class DailyLogDeleteView(DeleteView):
    model = DailyLog
    success_url = reverse_lazy("daily_logs")

    def get(self, request, *args, **kwargs):
        """Přesměruje GET požadavky na přímé odstranění záznamu"""
        self.object = self.get_object()  # získání objektu, který bude smazán
        self.object.delete()
        return HttpResponseRedirect(self.success_url)
