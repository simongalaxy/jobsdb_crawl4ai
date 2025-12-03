"""Data models for job advertisement extraction."""

from pydantic import BaseModel, Field


class JobAd(BaseModel):
    """Schema for extracting job advertisement details."""

    post_title: str = Field(description="Post Title")
    company_name: str = Field(description="Company Name")
    job_ad_url: str = Field(description="URL link of this job advertisement")
    responsbilities: str = Field(description="Duties or Responsibilites of this post")
    qualifications: str = Field(
        description="Qualifications and skills requirement of this post."
    )
    salary: str | None = Field(description="Salary of this post")
    experience: str | None = Field(description="Working Experiences required by this post.")
