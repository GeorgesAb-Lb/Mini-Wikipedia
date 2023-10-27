from django.shortcuts import render
import markdown
from . import util
from random import choice

def convert_md(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = convert_md(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry is unavailable"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_md(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            })
        else:
            recommendation = []
            all_entries = util.list_entries()
            for entry in all_entries:
                if entry_search.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendation": recommendation
            })
def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        title_exist = util.get_entry(title)
        if title_exist is not None:
            return render(request, "encyclopedia/error.html", {
                "message" : "Entry Already Exists"
            })
        elif title is not None and content is not None:
            util.save_entry(title, content)
            html_content = convert_md(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })
def edit(request):
    if request.method == "POST":
        title = request.POST['entry']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })


def save(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convert_md(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
def random(request):
    all_entries = util.list_entries()
    random_entry = choice(all_entries)
    html_content = convert_md(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": html_content
    })

