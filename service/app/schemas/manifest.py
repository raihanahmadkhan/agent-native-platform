from pydantic import BaseModel


class CapabilityDescriptor(BaseModel):
    name: str
    category: str  # READ | WRITE | FINANCIAL | DESTRUCTIVE
    description: str
    input_schema: dict
    output_schema: dict


class ManifestResponse(BaseModel):
    service: str
    capabilities: list[CapabilityDescriptor]
