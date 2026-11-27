class Observer:
    """Interface de base des observateurs."""

    def update(self, event, data=None):
        raise NotImplementedError


class EventManager:
    """Gère les abonnés et diffuse les événements."""

    def __init__(self):
        self.observers = []

    def subscribe(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def unsubscribe(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify(self, event, data=None):
        for observer in self.observers:
            observer.update(event, data)