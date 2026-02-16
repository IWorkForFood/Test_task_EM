import os
from celery import current_app as celery_app
from celery.schedules import crontab
from datetime import timedelta
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery_app.task(name="test_task")
def test_task():
    dir_path = "./process_files"
    absolute_path = os.path.abspath(dir_path)

    # Проверка существования директории
    
    if not os.path.exists(absolute_path):
        return {
            "status": "error",
            "message": f"Directory not found: {absolute_path}",
            "processed": 0,
            "removed": 0,
            "errors": 1
        }
    
    stats = {
        "status": "success",
        "processed": 0,
        "removed": 0,
        "errors": 0,
        "error_details": []
    }
    
    
    try:
        # Один проход os.walk достаточно для рекурсивного обхода
        for root, dirs, files in os.walk(absolute_path):
            for file in files:
                if file.endswith('.md'):
                    stats["processed"] += 1
                    file_path = os.path.join(root, file)
                    
                    try:
                        os.remove(file_path) 
                        stats["removed"] += 1
                    except Exception as e:
                        stats["errors"] += 1
                        stats["error_details"].append({
                            "file": file_path,
                            "error": str(e)
                        })
        
        # Формируем итоговый статус
        if stats["errors"] > 0:
            stats["status"] = "partial_success"
        if stats["processed"] == 0:
            stats["status"] = "empty"
            stats["message"] = "No .md files found to process"
        
        return stats
        
    except Exception as e:
        return {
            "status": "failed",
            "message": str(e),
            "processed": 0,
            "removed": 0,
            "errors": 1,
            "error_details": [str(e)]
        }




celery_app.conf.beat_schedule = {
    'run-test-task-every-5-minutes': {
        'task': 'test_task',
        'schedule': timedelta(seconds=10),
        # 'schedule': crontab(hour=2, minute=30),  # Ежедневно в 02:30
        'args': (),
        'kwargs': {},
        'options': {
            'queue': 'default',
            'expires': 300,  # Задача отменяется, если не запустилась за 5 минут
        },
    },
}

