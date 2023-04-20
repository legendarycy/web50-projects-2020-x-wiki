from django.shortcuts import render
from django.http import HttpResponseRedirect
from encyclopedia import util
import markdown

def load_page(request, title):
    valid_entries = util.list_entries()
    valid_entries_l = [i.lower() for i in valid_entries]
    formatted_title = title.lower().strip().replace(" ", "_")
    if formatted_title in valid_entries_l:
        entry_index = valid_entries_l.index(formatted_title)
        content = util.get_entry(valid_entries[entry_index])
        return render(request, "encyclopedia/page.html", {
            "title": valid_entries[entry_index],
            "content": markdown.markdown(content)
        })
    else:
        return render(request, "encyclopedia/page.html", {
            "title": "Not Found",
            "content": f"'{title}' is not a valid entry."
        })