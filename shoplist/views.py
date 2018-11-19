import json

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from shoplist.models import ShoplistModel


@method_decorator(csrf_exempt, name='dispatch')
class ShoplistView(View):
    def get(self, request, *args, **kwargs):
        if not request.GET.get('email'):
            return HttpResponseBadRequest('No email field.')
        items = [x['item'] for x in ShoplistModel.objects.filter(email=request.GET['email']).values('item')]
        return JsonResponse({'items': items})

    def post(self, request, *args, **kwargs):
        with open('/tmp/debug', 'a') as f:
            print(request.POST, file=f)
        if not request.POST.get('email') or (not request.POST.getlist('items') and not request.POST.get('remove')):
            return HttpResponseBadRequest('No email or items field.')
        email = request.POST.get('email')
        if request.POST.get('remove'):
            ShoplistModel.objects.filter(email=email).delete()
            return HttpResponse('removed')
        for item in request.POST.getlist('items'):
            obj = ShoplistModel(email=email, item=item)
            obj.save()
        return HttpResponse('saved')
