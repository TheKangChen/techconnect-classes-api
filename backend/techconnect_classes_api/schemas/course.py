from pydantic import BaseModel, ConfigDict, Field, HttpUrl


# Base schemas
class CourseBase(BaseModel):
    course_name: str = Field(
        ..., examples=["Intermediate Python Functions", "Microsoft Excel For Beginners"]
    )


class HandoutResponse(BaseModel):
    language_code: str = Field(..., examples=["en", "es", "zh", "bn", "fr", "ru"])
    url: HttpUrl = Field(..., description="Url to course handout")


# API endpoint schemas
class CourseNodeQuery(BaseModel):
    """Schema for the query parameters of /courses endpoint."""

    level: str | None = None
    format: str | None = None
    series: str | None = None


class CourseNodeResponse(CourseBase):
    """Schema for the /courses endpoint."""

    id: int = Field(..., ge=1)

    model_config = ConfigDict(from_attributes=True)


class CourseDetailResponse(CourseBase):
    """Schema for the /courses/{id}/ endpoint."""

    description: str = Field(..., description="Course description.")
    series: list[str] = Field(
        ...,
        description="The series or topic a course is part of.",
        examples=["3d printing", "microsoft excel", "python"],
    )
    level: str = Field(..., examples=["none", "beginner", "intermediate", "advanced"])
    format: str = Field(..., examples=["class", "lab", "workshop"])
    prereqs: list[str] | None = Field(default=None, description="Course prerequisites.")
    available_handouts: list[HandoutResponse] | None = None
    additional_materials: list[HttpUrl] | None = None
    link_to_upcoming_sessions: HttpUrl = Field(
        ...,
        description="Upcoming sessions of course on NYPL techconnect classes page.",
        examples=["https://www.nypl.org/techconnect?keyword=Python+for+Beginners"],
    )


class CourseHandoutsResponse(BaseModel):
    """Schema for the response from /courses/{id}/handouts."""

    handouts: list[HandoutResponse] | None = None


class CourseAdditionalMaterialsResponse(BaseModel):
    """Schema for the response from /courses/{id}/additional-material."""

    additional_materials: list[HttpUrl] | None = None


class CourseFormatsResponse(BaseModel):
    """Schema for the response from /courses/formats."""

    formats: list[str] = Field(..., examples=["class", "lab", "workshop"])


class CourseLevelsResponse(BaseModel):
    """Schema for the response from /courses/levels."""

    levels: list[str] = Field(
        ..., examples=["none", "beginner", "intermediate", "advanced"]
    )


class CourseSeriesResponse(BaseModel):
    """Schema for the response from /courses/series."""

    series: list[str] = Field(
        ..., examples=["3d printing", "microsoft excel", "python"]
    )


class CourseLanguagesResponse(BaseModel):
    """Schema for the response from /courses/languages."""

    languages: dict[str, str] = Field(
        ...,
        examples=[
            {
                "english: en",
                "chinese: zh",
                "spanish: es",
                "bengali: bn",
                "french: fr",
                "russian: ru",
            }
        ],
    )
