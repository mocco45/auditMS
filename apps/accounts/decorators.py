from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


def groups_required(*group_names):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.groups.filter(name__in=group_names).exists():
                return HttpResponseForbidden(
                    "You are not authorized to access this page"
                )
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
