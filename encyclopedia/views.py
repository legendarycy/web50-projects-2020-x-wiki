from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from . import util
import numpy as np

#list entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#search
def load_results(request):
    valid_entries = util.list_entries()
    valid_entries_l = [i.lower() for i in valid_entries]
    #retrieve the query from the get request
    query_orig = request.GET.get('q', '')
    query = query_orig.strip().replace(" ", "_")

    if query.lower() in valid_entries_l:
        q = valid_entries[valid_entries_l.index(query.lower())]
        return HttpResponseRedirect(f"/wiki/{q}")
    else:
        similar_l = [i for i in valid_entries_l if i.find(query.lower()) != -1]
        result_index = [valid_entries_l.index(i) for i in similar_l]
        return render(request, "encyclopedia/results.html", {
            "query": query_orig,
            "q_results": [valid_entries[i] for i in result_index]
        })

#random page
def random_page(request):
    entries = util.list_entries()
    rs = entries[np.random.randint(0, len(entries))]
    return HttpResponseRedirect(f"/wiki/{rs}")

#form class
class ntform(forms.Form):
        title = forms.CharField(
            label = "Title"
        )
        content = forms.CharField(
             widget = forms.Textarea(
                attrs = {
                    "placeholder": "Input content here"
                }
             ),
             label = ""
        )

#new entry page
def new_entry(request):
    if request.method == "POST":
         form = ntform(request.POST)
         if form.is_valid():
            title = form.cleaned_data['title'].strip().replace(" ", "_")
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("index"))
         else:
            return render(request, "new_entry.html", {
                "form": form
            })
    else:
        form = ntform()
        referer = request.META.get('HTTP_REFERER')
        path = request.path

        if path == '/edit_entry' and referer != None:
            page_name = referer.split('wiki/')[1]
            form = ntform(initial = {
                'title': page_name.replace("_", " "),
                'content': util.get_entry(page_name)
            })
        elif path == '/edit_entry' and referer == None:
            return HttpResponseRedirect(reverse("index"))
        return render(request, "encyclopedia/new_entry.html", {
                "form": form
        })