from django.apps import AppConfig
from threading import Thread
from racing.LoadBalancer import run_loop

class TestThread(Thread):
    def run(self):
        run_loop()
        

class RacingConfig(AppConfig):
    name = 'racing'
    def ready(self):
        pass
        TestThread().start()
