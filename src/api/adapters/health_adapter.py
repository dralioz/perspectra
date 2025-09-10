from src.models.health import HealthCheck


class HealthAdapter:
    def ready(self):
        return HealthCheck(status=200, message="The application is ready")

    def live(self):
        return HealthCheck(status=200, message="The application is live")
