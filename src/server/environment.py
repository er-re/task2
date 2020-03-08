import os

env = os.environ.get("PYTHON_ENV", "development")

all_environments = {
    "development": {"port": 5000, "debug": True, "swagger-url": "/api/swagger"},
    "production": {"port": 8080, "debug": False, "swagger-url": None}
}

environment_config = all_environments[env]
