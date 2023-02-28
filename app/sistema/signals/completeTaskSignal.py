from django.core.signals import Signal
from celery import shared_task

completeTaskSignal = Signal()

def completeTaskSignalHandler(sender, **kwargs):
    task_id = kwargs.get("task_id")
    process_id = kwargs.get("process_id")

    print("completeTaskSignalHandler", task_id, process_id)
    
completeTaskSignal.connect(completeTaskSignalHandler)