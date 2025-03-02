from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional

class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ArchitectureRequest(BaseModel):
    functional_requirement: Optional[str] = Field(
        None, description="Functional requirement text", min_length=20, max_length=2000
    )
    architecture: Optional[str] = Field(None, description="Core architecture pattern")
    custom_arch: Optional[str] = Field("", description="Custom architecture details if Hybrid/Custom")
    services: List[str] = Field(default_factory=list, description="Selected business services")
    custom_service: Optional[str] = Field("", description="Additional business services")
    integration: List[str] = Field(default_factory=list, description="Integration methods selected")
    custom_integration: Optional[str] = Field("", description="Additional integration methods")
    data_storage: List[str] = Field(default_factory=list, description="Primary data store options")
    caching: List[str] = Field(default_factory=list, description="Secondary storage and caching options")
    data_processing: List[str] = Field(default_factory=list, description="Data processing patterns")
    custom_storage: Optional[str] = Field("", description="Additional storage options")
    security: List[str] = Field(default_factory=list, description="Security measures")
    compliance: List[str] = Field(default_factory=list, description="Compliance standards")
    custom_security: Optional[str] = Field("", description="Additional security policies")
    deployment: Optional[str] = Field(None, description="Deployment environment")
    scaling: List[str] = Field(default_factory=list, description="Scaling strategies")
    monitoring: List[str] = Field(default_factory=list, description="Monitoring tools")
    custom_deployment: Optional[str] = Field("", description="Additional deployment preferences")
    expected_concurrency: Optional[int] = Field(None, description="Expected concurrency")
    latency: Optional[int] = Field(None, description="Latency requirement in ms")
    throughput: Optional[int] = Field(None, description="Throughput target in req/sec")
    resilience: List[str] = Field(default_factory=list, description="Resilience features")
    custom_resilience: Optional[str] = Field("", description="Additional resilience requirements")
    advanced_features: List[str] = Field(default_factory=list, description="Advanced features")
    custom_advanced: Optional[str] = Field("", description="Additional advanced features")
    provider: Optional[str] = Field("huggingface", description="(Not used; provider is set via env)")

class ArchitectureResponse(BaseModel):
    architecture: str

class InvokeRequest(BaseModel):
    prompt: str = Field(..., min_length=50, max_length=5000)

class InvokeResponse(BaseModel):
    job_id: str
    status: JobStatus
    message: str

class JobStatusResponse(BaseModel):
    job_id: str
    status: JobStatus
    result: Optional[str]
    error: Optional[str]
    progress: int
