import requests
from bs4 import BeautifulSoup

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse

from recipe.models import Recipe, Instruction


class ScrapeView(View):
    def get(self, request, *args, **kwargs):
        for i in range(2, 120):
            try:
                url_list = 'https://eda.ru/recepty?page=' + str(i)
                resp = requests.get(url_list)
                soup = BeautifulSoup(resp.text)
                items = soup.findAll('h3', {'class': 'item-title'})
                urls = ['https://eda.ru/' + [child for child in item.children][1]['href'] for item in items]
                for url in urls:
                    resp = requests.get(url)
                    soup = BeautifulSoup(resp.text)
                    title = soup.find('h1', {'class': 'recipe__name'}).text.strip()
                    steps = [[child for child in step.children][-1] for step in soup.findAll('span', {'class': 'instruction__description'})]
                    recipe = Recipe(name=title)
                    recipe.save()
                    for step in steps:
                        Instruction(step=step, recipe=recipe).save()
            except Exception as e:
                pass
        return HttpResponse('ok')


class RecipeView(View):
    def get(self, request, *args, **kwargs):
        if not request.GET.get('search_for') and not request.GET.get('recipe'):
            return HttpResponseBadRequest('No search_for field')
        if request.GET.get('search_for'):
            recipes = Recipe.objects.filter(name__icontains=request.GET.get('search_for'))
            return JsonResponse({'recipes': [recipe.name for recipe in recipes]})
        if request.GET.get('recipe'):
            steps = Instruction.objects.filter(recipe__name=request.GET.get('recipe'))
            return JsonResponse({'steps': [step.step for step in steps]})
