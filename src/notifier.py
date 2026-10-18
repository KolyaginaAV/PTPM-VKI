from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send_notification(self, message):
        pass

class RealNotifier(Notifier):
    def send_notification(self, message):
        print(f"[СЕРВЕР] Отправлено уведомление: {message}")