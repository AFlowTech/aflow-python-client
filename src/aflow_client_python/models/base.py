from pydantic import BaseModel

try:
    from pydantic import ConfigDict
except ImportError:
    ConfigDict = None


if not hasattr(BaseModel, "model_dump"):
    class AFlowBaseModel(BaseModel):
        class Config:
            allow_population_by_field_name = True

        def model_dump(self, *args, **kwargs):
            return self.dict(*args, **kwargs)

        @classmethod
        def model_construct(cls, *args, **kwargs):
            return cls.construct(*args, **kwargs)
else:
    class AFlowBaseModel(BaseModel):
        model_config = ConfigDict(populate_by_name=True)

        def model_dump(self, *args, **kwargs):
            return super().model_dump(*args, **kwargs)

        @classmethod
        def model_construct(cls, *args, **kwargs):
            return super().model_construct(*args, **kwargs)
