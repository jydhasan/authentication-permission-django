from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.contrib import messages


@login_required
def dashboard(request):
    return render(request, "core/dashboard.html")


def is_super_admin(user):
    return user.is_authenticated and user.is_superuser


@login_required
def role_list(request):
    if not is_super_admin(request.user):
        messages.error(request, "Permission নেই")
        return redirect("dashboard")
    groups = Group.objects.all().prefetch_related("permissions")
    return render(request, "core/role_list.html", {"groups": groups})


@login_required
def role_create(request):
    if not is_super_admin(request.user):
        messages.error(request, "Permission নেই")
        return redirect("dashboard")

    all_permissions = Permission.objects.select_related("content_type").order_by(
        "content_type__app_label", "codename"
    )

    if request.method == "POST":
        role_name = request.POST.get("role_name", "").strip()
        selected_perm_ids = request.POST.getlist("permissions")

        if not role_name:
            messages.error(request, "Role name দিন")
            return redirect("role_create")

        if Group.objects.filter(name=role_name).exists():
            messages.error(request, "এই Role আগে থেকেই আছে")
            return redirect("role_create")

        group = Group.objects.create(name=role_name)
        group.permissions.set(Permission.objects.filter(id__in=selected_perm_ids))

        messages.success(request, f"Role '{role_name}' তৈরি হয়েছে")
        return redirect("role_list")

    return render(request, "core/role_form.html", {"all_permissions": all_permissions})


@login_required
def role_edit(request, group_id):
    if not is_super_admin(request.user):
        messages.error(request, "Permission নেই")
        return redirect("dashboard")

    group = Group.objects.get(id=group_id)
    all_permissions = Permission.objects.select_related("content_type").order_by(
        "content_type__app_label", "codename"
    )

    if request.method == "POST":
        new_name = request.POST.get("role_name", "").strip()
        if new_name:
            group.name = new_name
        selected_perm_ids = request.POST.getlist("permissions")
        group.permissions.set(Permission.objects.filter(id__in=selected_perm_ids))
        group.save()
        messages.success(request, "Role আপডেট হয়েছে")
        return redirect("role_list")

    current_perm_ids = set(group.permissions.values_list("id", flat=True))
    return render(request, "core/role_form.html", {
        "group": group,
        "all_permissions": all_permissions,
        "current_perm_ids": current_perm_ids,
    })


@login_required
def role_delete(request, group_id):
    if not is_super_admin(request.user):
        messages.error(request, "Permission নেই")
        return redirect("dashboard")
    Group.objects.filter(id=group_id).delete()
    messages.success(request, "Role ডিলিট হয়েছে")
    return redirect("role_list")