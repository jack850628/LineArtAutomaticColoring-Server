from celery import Celery  
  
app = Celery('line-art-automatic-coloring-serverTask')
app.config_from_object('tasks.celeryconfig')
app.finalize()