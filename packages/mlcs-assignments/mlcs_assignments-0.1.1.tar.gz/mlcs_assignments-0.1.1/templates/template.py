from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader

from typing import Final


TEMPLATE_DIRECTORY: Final[str] = "templates"


@dataclass(frozen=True)
class ExerciseConfiguration:
    solution: bool
    comment: str = ""


@dataclass(frozen=True)
class TemplateConfiguration:
    exercise: dict[str, ExerciseConfiguration]

    def none_solved(self) -> "TemplateConfiguration":
        return TemplateConfiguration(
            exercise={exercise: not_solved() for exercise in self.exercise}
        )

    def all_solved(self) -> "TemplateConfiguration":
        return TemplateConfiguration(
            exercise={exercise: solved() for exercise in self.exercise}
        )


def not_solved() -> ExerciseConfiguration:
    return ExerciseConfiguration(solution=False)


def solved(comment: str = "") -> ExerciseConfiguration:
    return ExerciseConfiguration(
        solution=True, comment="# " + comment if comment else ""
    )


def configure(exercises: dict[str, ExerciseConfiguration]) -> TemplateConfiguration:
    return TemplateConfiguration(exercise=exercises)


def create_environment() -> Environment:
    return Environment(
        loader=FileSystemLoader("."),
        block_start_string="# {%",  # This way formatters can still format the code
        variable_start_string="# {{",
        comment_start_string="# {#",
        comment_end_string="#}",
        trim_blocks=True,
        lstrip_blocks=True,
    )


def generate(*, from_template: str, using: TemplateConfiguration, to: str) -> None:
    # Set up the Jinja2 environment
    env = create_environment()

    # Load the template
    template = env.get_template(f"{TEMPLATE_DIRECTORY}/{from_template}")

    # Render the template with the context
    output = template.render({"exercise": using.exercise})

    # Save the output to a file
    with open(to, "w", encoding="utf-8") as f:
        f.write(output)

    print("File generated successfully.")
