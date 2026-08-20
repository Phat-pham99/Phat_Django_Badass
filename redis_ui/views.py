from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .forms import SetForm, QueryForm, DeleteForm
from .services import list_keys, get_key_info, set_key, delete_key


@staff_member_required(login_url="/admin/login/")
@csrf_protect
def redis_manager(request):
    context = {
        "set_form": SetForm(),
        "query_form": QueryForm(),
        "delete_form": DeleteForm(),
        "keys": [],
        "key_info": None,
    }

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "set":
            form = SetForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                ok = set_key(data["key"], data["value"], data.get("ttl_seconds"))
                messages.success(request, f"SET {data['key']} = OK ({ok})")
            else:
                context["set_form"] = form

        elif action == "query":
            form = QueryForm(request.POST)
            if form.is_valid():
                key = form.cleaned_data["key"]
                context["key_info"] = get_key_info(key)
                messages.info(request, f"Queried key: {key}")
            else:
                context["query_form"] = form

        elif action == "delete":
            form = DeleteForm(request.POST)
            if form.is_valid():
                key = form.cleaned_data["key"]
                count = delete_key(key)
                messages.warning(request, f"DELETED {key} ({count} key(s) removed)")
            else:
                context["delete_form"] = form

    pattern = request.GET.get("pattern", "*") or "*"
    keys, _ = list_keys(pattern=pattern, count=200)
    context["keys"] = keys
    context["pattern"] = pattern

    return render(request, "redis_ui/redis_manager.html", context)