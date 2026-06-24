import threading
class ServiceRunner:
    def __init__(self):
        self.services = []

    def start(self, service, *args):
        thread = threading.Thread(
            target = service.run, args = args, daemon= True)
        thread.start()

        self.services.append((service, thread))
        
    def stop_all(self):
        for service, _ in self.services:
            service.stop()

    def wait(self):
        for _, thread in self.services:
            thread.join()