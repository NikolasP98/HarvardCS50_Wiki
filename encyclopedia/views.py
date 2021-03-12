from django.shortcuts import render, redirect
from markdown2 import Markdown
from . import forms, util
import random
from django.contrib import messages


def error404(request):
	return render(request, "encyclopedia/404.html")


def index(request):
	print(util.list_entries())
	return render(request, "encyclopedia/index.html", {
		"entries": util.list_entries()
	})


def wikiLink(request, name):
	if name.upper() not in [x.upper() for x in util.list_entries()]:
		return error404(request)
	else:
		return render(request, "encyclopedia/wikiPage.html", {
			"name": name,
			"content": Markdown().convert(util.get_entry(name))
		})

def randomPage(request):
	rand = int(random.randint(0, len(util.list_entries())-1))
	article = util.list_entries()[rand]
	return redirect("wiki:article", article)

def delete(request, title):
    page_list = [x.upper() for x in util.list_entries()]
    if title.upper() in page_list:
        util.delete_entry(title)
        messages.success(request, "The page was deleted successfuly!")
    return redirect("wiki:index")

def editor(request, title):
	articleContent = util.get_entry(title)
	page_list = [x.upper() for x in util.list_entries()]
 
	if request.method == "POST":
		
		form = forms.ArticleForm(request.POST)
		if form.is_valid():
			new_title = form.cleaned_data["title"]
			content = form.cleaned_data["content"]
			if new_title.upper() not in page_list:
				util.delete_entry(title)
			util.save_entry(new_title, content)
			messages.success(request, "The page was updated correctly!")
			return redirect('wiki:article', new_title)
	return render(request, "encyclopedia/editPage.html", {
		"name": title,
		"form": forms.ArticleForm(initial={"title": title, "content": articleContent})
	})

def create(request):
	page_list = [x.upper() for x in util.list_entries()]
	if request.method == "POST":
		form = forms.ArticleForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			content = form.cleaned_data["content"]
			if title.upper() in page_list:
				title = util.list_entries()[page_list.index(title.upper())]
				messages.error(request, f"This entry already exists!\nEither change the title of this version or edit the original entry by <a href='edit/{title}'>clicking here!</a>")
				return render(request, "encyclopedia/createpage.html", {
					"form": form
				})
			util.save_entry(title, content)
			messages.success(request, "The wiki page was uploaded correctly!")
			return redirect('wiki:index')
		else:
			return render(request, "encyclopedia/createpage.html", {
				"form": form
			})
	return render(request, "encyclopedia/createpage.html", {
		"form": forms.ArticleForm()
	})

def search(request):
	results = []
	entries = util.list_entries()

	if request.method == "GET":
		q = request.GET.get("q")
		if q != '':
			for entry in entries:
				if q.upper() in entry.upper():
					results.append(entry)
					if q.upper() == entry.upper():
						return redirect("wiki:article", entry)
			print(results)
			return render(request, "encyclopedia/searchResult.html", {
				"query": q,
				"entries": results
			})