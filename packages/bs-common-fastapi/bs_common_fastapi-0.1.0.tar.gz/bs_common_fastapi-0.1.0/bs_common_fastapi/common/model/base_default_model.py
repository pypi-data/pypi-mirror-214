from pydantic import BaseModel, Extra, Field, root_validator


class BaseBodyDefaultModel(BaseModel):
    class Config:
        extra = Extra.forbid

    @root_validator(pre=True)
    def empty_payload(cls, values):
        if len(values) == 0:
            raise ValueError('Invalid Payload')
        return values


class HomeModel(BaseModel):
    app_name: str = Field(description='Application name')
    app_version: str = Field(description='Application version')


class HealthCheckModel(BaseModel):
    status: str = Field(description='Service Status')


class ErrorDefaultModel(BaseModel):
    message: str = Field(description='Message Error')

    class Config:
        schema_extra = {
            'examples': [{
                'message': 'An error has occurred'
            }]
        }
