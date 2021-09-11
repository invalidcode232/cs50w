from django.shortcuts import render
from django.http import HttpResponseRedirect
import markdown2
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, name):
    entries = util.list_entries()

    # if name.lower() in (entry.lower() for entry in entries):
    if util.is_in_entry(name, entries):
        return render(request, "encyclopedia/wiki.html", {
            "name": name,
            "content": markdown2.markdown(util.get_entry(name)),
        })
    else:
        return render(request, "encyclopedia/notfound.html", {
            "name": name
        })


def search(request):
    entries = util.list_entries()
    query = request.GET.get("q")

    if not query:
        return render(request, "encyclopedia/error.html", {
            "error": "You need to provide a valid query!"
        })

    if util.is_in_entry(query, entries):
        return render(request, "encyclopedia/wiki.html", {
            "name": query,
            "content": markdown2.markdown(util.get_entry(query)),
        })

    res = [entry for entry in entries if query.lower() in entry.lower()]

    if not len(res):
        return render(request, "encyclopedia/notfound.html", {
            "name": query
        })

    return render(request, "encyclopedia/search.html", {
        "entries": res
    })


def new_entry(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if not title or not content:
            return render(request, "encyclopedia/error.html", {
                "error": "Please provide valid title and entry!"
            })

        entries = util.list_entries()
        if util.is_in_entry(title, entries):
            return render(request, "encyclopedia/error.html", {
                "error": f"{title} already existed"
            })

        util.save_entry(title, content)

        return HttpResponseRedirect(title)
    else:
        return render(request, "encyclopedia/new.html")


def edit(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if util.get_entry(title) is None:
            return render(request, "encyclopedia/error.html", {
                "error": "Entry not found!"
            })

        util.save_entry(title, content)

        return HttpResponseRedirect(title)
    else:
        title = request.GET.get("title")
        content = util.get_entry(title)

        if content is None:
            return render(request, "encyclopedia/error.html", {
                "error": "Entry not found!"
            })

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })


def random_entry(request):
    entries = util.list_entries()
    return HttpResponseRedirect(random.choice(entries))
