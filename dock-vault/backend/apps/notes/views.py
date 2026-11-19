from django.contrib.auth.decorators import login_required
from inertia import inertia

from .models import Note


@login_required
@inertia("Notes/Index")
def index(request):
    notes = list(
        Note.objects.filter(owner=request.user).values("id", "title", "content", "updated_at")
    )
    return {"notes": notes}
