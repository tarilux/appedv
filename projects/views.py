from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ProjectForm
from .models import Project, ProjectHistory, build_project_history
from .services import export_dashboard_ppt, export_project_pdf, export_projects_excel


class AdminLoginView(LoginView):
    template_name = "auth/login.html"


@login_required
def dashboard(request):
    active_projects = Project.objects.filter(archive=False)
    stats = {
        "total_actifs": active_projects.count(),
        "execution": active_projects.filter(etat=Project.Etat.EXECUTION).count(),
        "clotures": active_projects.filter(etat=Project.Etat.CLOTURE).count(),
        "archives": Project.objects.filter(archive=True).count(),
        "budget_total": active_projects.aggregate(total=Sum("budget_previsionnel"))["total"] or 0,
        "budget_engage": active_projects.aggregate(total=Sum("montant_contrat"))["total"] or 0,
    }

    state_distribution = list(active_projects.values("etat").annotate(total=Count("id")).order_by("etat"))
    recent_projects = active_projects.order_by("-updated_at")[:8]
    budget_evolution = list(active_projects.order_by("date_debut").values("date_debut", "budget_previsionnel"))

    context = {
        "stats": stats,
        "state_distribution": state_distribution,
        "budget_evolution": budget_evolution,
        "recent_projects": recent_projects,
        "today": timezone.localdate(),
        "page_title": "Dashboard",
    }
    return render(request, "projects/dashboard.html", context)


@login_required
def project_list(request):
    query = request.GET.get("q", "")
    archive_filter = request.GET.get("archive", "0")
    projects = Project.objects.filter(archive=archive_filter == "1")
    if query:
        projects = projects.filter(Q(intitule__icontains=query) | Q(reference__icontains=query))

    paginator = Paginator(projects.order_by("-updated_at"), 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        payload = [
            {
                "id": p.id,
                "reference": p.reference,
                "intitule": p.intitule,
                "etat": p.etat,
                "budget": str(p.budget_previsionnel),
                "avancement": p.taux_avancement,
            }
            for p in page_obj
        ]
        return JsonResponse({"results": payload})

    return render(
        request,
        "projects/project_list.html",
        {"page_obj": page_obj, "query": query, "archive_filter": archive_filter, "page_title": "Projets"},
    )


@login_required
def project_create(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        project = form.save()
        build_project_history(None, project, request.user)
        messages.success(request, "Projet ajouté avec succès.")
        return redirect("project_detail", pk=project.pk)

    return render(request, "projects/project_form.html", {"form": form, "page_title": "Ajouter projet"})


@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    previous = Project.objects.get(pk=pk)
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        updated = form.save()
        build_project_history(previous, updated, request.user)
        messages.success(request, "Projet modifié avec succès.")
        return redirect("project_detail", pk=pk)

    return render(
        request,
        "projects/project_form.html",
        {"form": form, "project": project, "page_title": f"Modifier {project.reference}"},
    )


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(
        request,
        "projects/project_detail.html",
        {"project": project, "history": project.historiques.all()[:10], "page_title": f"Projet {project.reference}"},
    )


@login_required
def project_archive(request, pk):
    project = get_object_or_404(Project, pk=pk)
    previous = Project.objects.get(pk=pk)
    project.archive = True
    project.save(update_fields=["archive", "updated_at"])
    build_project_history(previous, project, request.user)
    messages.warning(request, f"Projet {project.reference} archivé.")
    return redirect("project_list")


@login_required
def history_list(request):
    history = ProjectHistory.objects.select_related("project", "modifie_par")[:100]
    return render(request, "projects/history_list.html", {"history": history, "page_title": "Historique"})


@login_required
def export_excel(request):
    return export_projects_excel(Project.objects.all().order_by("reference"))


@login_required
def export_pdf(request, pk):
    return export_project_pdf(get_object_or_404(Project, pk=pk))


@login_required
def export_ppt(request):
    return export_dashboard_ppt()


def custom_404(request, exception):
    return render(request, "errors/404.html", status=404)


def custom_500(request):
    return render(request, "errors/500.html", status=500)
