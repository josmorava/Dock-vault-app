from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from inertia import inertia

from .models import Category, Document


@login_required
@inertia("Documents/Index")
def index(request):
    qs = Document.objects.filter(owner=request.user).select_related("category").prefetch_related("tags")

    query = request.GET.get("q")
    if query:
        qs = qs.filter(name__icontains=query) | qs.filter(note__icontains=query)

    category = request.GET.get("category")
    if category:
        qs = qs.filter(category_id=category)

    tag = request.GET.get("tag")
    if tag:
        qs = qs.filter(tags__id=tag)

    documents = [
        {
            "id": str(doc.id),
            "name": doc.name,
            "file_type": doc.file_type,
            "category": {"id": str(doc.category_id), "name": doc.category.name, "color": doc.category.color},
            "tags": [{"id": str(t.id), "name": t.name} for t in doc.tags.all()],
            "note": doc.note,
            "created_at": doc.created_at.isoformat(),
        }
        for doc in qs.distinct()
    ]

    categories = list(
        Category.objects.filter(models_q_owner_or_default(request.user)).values("id", "name", "color")
    )

    return {"documents": documents, "categories": categories}


def models_q_owner_or_default(user):
    from django.db.models import Q

    return Q(owner=user) | Q(is_default=True)
