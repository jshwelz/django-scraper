from django.http import JsonResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from celery.result import AsyncResult
from scraper.celery_tasks import create_task_lazada, create_task_shopee
from importlib import import_module
from django.conf import settings

@csrf_exempt
def run_task(request):    
    if request.POST:        
        try:
            keyword = request.POST.get('keyword')                        
            task_lazada = create_task_lazada.delay(keyword)
            task_shopee = create_task_shopee.delay(keyword)
        except Exception as e:
            print(e)        
        return JsonResponse({'task_lazada_id': task_lazada.id, 'task_shopee_id': task_shopee.id}, status=202)


@csrf_exempt
def get_status(request, task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JsonResponse(result, status=200)
    