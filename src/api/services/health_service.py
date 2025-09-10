from src.api.adapters.health_adapter import HealthAdapter
from src.models.health import HealthResponseModel


class HealthService:
    def __init__(self):
        self.health_adapter = HealthAdapter()

    def ready(self) -> HealthResponseModel:
        ready_model = self.health_adapter.ready()
        return HealthResponseModel(message=ready_model.message)

    def live(self) -> HealthResponseModel:
        live_model = self.health_adapter.live()
        return HealthResponseModel(message=live_model.message)
