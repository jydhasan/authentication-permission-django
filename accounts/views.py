# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not username or not email or not password:
            messages.error(request, "সব ফিল্ড পূরণ করুন")
            return redirect("register")

        if password != confirm_password:
            messages.error(request, "Password মিলছে না")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "এই Username আগে থেকে আছে")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "এই Email আগে থেকে ব্যবহৃত")
            return redirect("register")

        user = User.objects.create_user(
            username=username, email=email, password=password, phone=phone
        )

        # নতুন user-কে default role দাও (optional)
        default_group, _ = Group.objects.get_or_create(name="Sales")
        user.groups.add(default_group)

        messages.success(request, "Registration সফল হয়েছে, এখন Login করুন")
        return redirect("login")

    return render(request, "accounts/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_active:
                messages.error(request, "আপনার Account নিষ্ক্রিয়")
                return redirect("login")
            login(request, user)
            messages.success(request, f"স্বাগতম, {user.username}")
            return redirect("dashboard")
        else:
            messages.error(request, "ভুল Username অথবা Password")
            return redirect("login")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logout সফল হয়েছে")
    return redirect("login")