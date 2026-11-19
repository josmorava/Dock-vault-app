from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from inertia import inertia, render

from .models import User


@inertia("Auth/Login")
def login_page(request):
    return {}


@require_http_methods(["POST"])
def login_submit(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    user = authenticate(request, username=email, password=password)
    if user is None:
        return render(request, "Auth/Login", props={"error": "Credenciales inválidas"})
    login(request, user)
    return redirect("documents:index")


@require_http_methods(["POST"])
def logout_submit(request):
    logout(request)
    return redirect("login")


def _settings_props(request, errors=None):
    is_admin = request.user.is_admin or request.user.is_superuser
    props = {
        "user": {
            "email": request.user.email,
            "name": request.user.name,
            "session_timeout_minutes": request.user.session_timeout_minutes,
            "is_admin": is_admin,
        },
        "errors": errors or {},
    }
    if is_admin:
        props["users"] = [
            {**u, "is_admin": u["is_admin"] or u["is_superuser"]}
            for u in User.objects.order_by("email").values(
                "id", "email", "name", "is_admin", "is_superuser"
            )
        ]
    return props


@login_required
@inertia("Settings/Index")
def settings_page(request):
    return _settings_props(request)


@login_required
@require_http_methods(["PUT"])
def update_profile(request):
    request.user.name = request.POST.get("name", "").strip()
    request.user.save(update_fields=["name"])
    return redirect("settings")


@login_required
@require_http_methods(["PUT"])
def update_email(request):
    current_password = request.POST.get("current_password", "")
    new_email = request.POST.get("email", "").strip()

    if not request.user.check_password(current_password):
        return render(
            request, "Settings/Index",
            props=_settings_props(request, errors={"email": "Contraseña actual incorrecta"}),
        )
    if not new_email:
        return render(
            request, "Settings/Index",
            props=_settings_props(request, errors={"email": "El email no puede estar vacío"}),
        )
    if User.objects.exclude(pk=request.user.pk).filter(email__iexact=new_email).exists():
        return render(
            request, "Settings/Index",
            props=_settings_props(request, errors={"email": "Ese email ya está en uso"}),
        )

    request.user.email = new_email
    request.user.username = new_email
    request.user.save(update_fields=["email", "username"])
    return redirect("settings")


@login_required
@require_http_methods(["PUT"])
def update_password(request):
    current_password = request.POST.get("current_password", "")
    new_password = request.POST.get("new_password", "")
    confirmation = request.POST.get("new_password_confirmation", "")

    if not request.user.check_password(current_password):
        return render(
            request, "Settings/Index",
            props=_settings_props(request, errors={"password": "Contraseña actual incorrecta"}),
        )
    if new_password != confirmation:
        return render(
            request, "Settings/Index",
            props=_settings_props(request, errors={"password": "Las contraseñas nuevas no coinciden"}),
        )
    try:
        validate_password(new_password, user=request.user)
    except ValidationError as exc:
        return render(
            request, "Settings/Index",
            props=_settings_props(request, errors={"password": " ".join(exc.messages)}),
        )

    request.user.set_password(new_password)
    request.user.save(update_fields=["password"])
    update_session_auth_hash(request, request.user)
    return redirect("settings")


@login_required
@require_http_methods(["POST"])
def create_user(request):
    if not (request.user.is_admin or request.user.is_superuser):
        return redirect("settings")

    email = request.POST.get("email", "").strip()
    name = request.POST.get("name", "").strip()
    password = request.POST.get("password", "")

    if not email or not password:
        return render(
            request, "Settings/Index",
            props=_settings_props(request, errors={"new_user": "Email y contraseña son obligatorios"}),
        )
    if User.objects.filter(email__iexact=email).exists():
        return render(
            request, "Settings/Index",
            props=_settings_props(request, errors={"new_user": "Ese email ya está registrado"}),
        )
    try:
        validate_password(password)
    except ValidationError as exc:
        return render(
            request, "Settings/Index",
            props=_settings_props(request, errors={"new_user": " ".join(exc.messages)}),
        )

    User.objects.create_user(username=email, email=email, name=name, password=password)
    return redirect("settings")
