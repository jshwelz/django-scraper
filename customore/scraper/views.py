from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from celery.result import AsyncResult

# from scrapper.sample_tasks import create_task

from scraper.sample_tasks import create_task

@csrf_exempt
def run_task(request):    
    if request.POST:
        print('potato')        
        try:
            keyword = request.POST.get('keyword')                        
            task = create_task.delay(keyword)
        except Exception as e:
            print(e)        
        return JsonResponse({'task_id': task.id}, status=202)


@csrf_exempt
def get_status(request, task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JsonResponse(result, status=200)

