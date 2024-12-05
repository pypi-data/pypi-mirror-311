from typing import TYPE_CHECKING, Any, Optional

from pydantic import BaseModel

from .group import Group
from .term import Term

if TYPE_CHECKING:
    pass

from .lang_dict import LangDict


class CourseAttribute(BaseModel):
    """
    Class representing a course attribute.
    """

    name: LangDict | None = None
    values: list[LangDict] | None = None


class Course(BaseModel):
    """
    Class representing a course.
    """

    id: str | None = None
    name: LangDict | None = None
    homepage_url: str | None = None
    profile_url: str | None = None
    is_currently_conducted: bool | None = None
    terms: list[Term] | None = None
    fac_id: str | None = None
    lang_id: str | None = None
    ects_credits_simplified: float | None = None
    description: LangDict | None = None
    bibliography: LangDict | None = None
    learning_outcomes: LangDict | None = None
    assessment_criteria: LangDict | None = None
    practical_placement: LangDict | None = None
    attributes: list[CourseAttribute] | None = None
    attributes2: list[CourseAttribute] | None = None


class CourseUnit(BaseModel):
    """
    Class representing a course unit.
    """

    id: str
    homepage_url: str | None = None
    profile_url: str | None = None
    learning_outcomes: LangDict | None = None
    assessment_criteria: LangDict | None = None
    topics: LangDict | None = None
    teaching_methods: LangDict | None = None
    bibliography: LangDict | None = None
    course_edition: Optional["CourseEdition"] = None
    class_groups: list[Group] | None = None


class CourseEdition(BaseModel):
    """
    Class representing a course edition.
    """

    course_id: str | None = None
    course_name: LangDict | None = None
    term_id: str | None = None
    homepage_url: str | None = None
    profile_url: str | None = None
    coordinators: list[dict[str, Any]] | None = None
    lecturers: list[dict[str, Any]] | None = None
    passing_status: str | None = None  # passed, failed, not_yet_passed
    user_groups: list[Group] | None = None

    description: LangDict | None = None
    bibliography: LangDict | None = None
    notes: LangDict | None = None
    course_units_ids: list[str] | None = None
    participants: list[dict[str, Any]] | None = None
    grades: list[dict[str, Any]] | None = None
    attributes: list[dict[str, list[LangDict]]] | None = None


class CourseEditionConducted(BaseModel):
    """
    Class representing a conducted course edition.
    """

    id: str | None = None
    course: Course | None = None
    term: Term | None = None
