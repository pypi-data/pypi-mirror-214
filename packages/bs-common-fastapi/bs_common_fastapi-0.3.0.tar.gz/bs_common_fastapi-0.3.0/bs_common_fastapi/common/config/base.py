import os

from pydantic import BaseSettings

from bs_common_fastapi.common.model.base_default_model import ErrorDefaultModel


class BaseConfig(BaseSettings):
    APP_NAME: str = os.getenv('APP_NAME')
    APP_VERSION: str = os.getenv('APP_VERSION')
    APP_DESCRIPTION: str = os.getenv('APP_DESCRIPTION')
    APP_ENVIRONMENT: str = os.getenv('APP_ENVIRONMENT')
    APP_PORT: int = int(os.getenv('APP_PORT'))
    APP_HOST: str = os.getenv('APP_HOST')
    APP_CONTACT_NAME: str = os.getenv('APP_CONTACT_NAME')
    APP_CONTACT_EMAIL: str = os.getenv('APP_CONTACT_EMAIL')
    APP_CONTACT_URL: str = os.getenv('APP_CONTACT_URL')
    APP_MAX_LIMIT_VALUE: int = os.getenv('APP_MAX_LIMIT_VALUE', 1000)
    APP_DESCRIPTION_SKIP: str = os.getenv('APP_DESCRIPTION_SKIP', '')
    APP_DESCRIPTION_LIMIT: str = os.getenv('APP_DESCRIPTION_LIMIT', '')
    APP_DESCRIPTION_FIELDS = str = os.getenv('APP_DESCRIPTION_FIELDS', '')
    APP_COMMON_RESPONSES = {
        404: {
            'model': ErrorDefaultModel
        },
        422: {
            'model': ErrorDefaultModel
        },
        500: {
            'model': ErrorDefaultModel
        },
    }
