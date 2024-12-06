from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProjectInferenceSimulatorEntity(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
    )

    title: Optional[str] = Field(None, alias='TITLE')
    status: Optional[str] = Field(None, alias='STATUS')
    url: Optional[str] = Field(None, alias='URL')
    started_at: Optional[str] = Field(None, alias='STARTED AT')
    finished_at: Optional[str] = Field(None, alias='FINISHED_AT')
