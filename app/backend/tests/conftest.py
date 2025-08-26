import pytest
from django.conf import settings

@pytest.fixture(autouse=True, scope="session")
def configure() :
    settings.REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = ("rest_framework.permissions.AllowAny",)
