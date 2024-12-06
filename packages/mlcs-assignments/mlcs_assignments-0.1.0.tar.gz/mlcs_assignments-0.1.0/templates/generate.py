import subprocess
import click
from click import Choice, Parameter, Context

from enum import Enum
from typing import Any, TypeAlias, Callable
from templates.template import not_solved, solved, generate, configure
from ruff import __main__ as ruff

Generator: TypeAlias = Callable[[], None]


def generate_robot_arm() -> None:
    directory = "Exercise 1"
    template = "robot-arm.template.ipynb"
    configuration = configure(
        {
            "1.3.1": not_solved(),
            "2.1.1": solved(
                comment="The solution is provided for you to save time, so you can take a quick look and skip ahead."
            ),
            "2.1.2": not_solved(),
            "3.2.1": not_solved(),
            "3.2.2": solved(
                comment="Bam! Another surprise solution. Take a look and skip ahead."
            ),
            "4.3.1": not_solved(),
            "4.3.2": not_solved(),
            "4.3.3": solved(),
            "4.3.4": solved(
                comment="We're almost there so here's a little help to speed things up."
            ),
            "4.3.5-prep": solved(
                comment="Your final boost to get you to the finish line."
            ),
            "4.3.5": not_solved(),
        }
    )

    generate(
        from_template=template,
        using=configuration,
        to=f"{directory}/robot-arm.ipynb",
    )

    generate(
        from_template=template,
        using=configuration.all_solved(),
        to=f"{directory}/robot-arm-solution.ipynb",
    )

    generate(
        from_template=template,
        using=configuration.none_solved(),
        to=f"{directory}/robot-arm-challenge.ipynb",
    )


def generate_motor_controller() -> None:
    directory = "Exercise 2"
    template = "motor-controller.template.ipynb"
    configuration = configure(
        {
            "1.1.1": not_solved(),
            "1.3.1": not_solved(),
            "2.2.1": not_solved(),
            "2.3.1": not_solved(),
            "2.4.1": not_solved(),
            "2.5.1": not_solved(),
            "2.7.1": not_solved(),
            "2.10.1": not_solved(),
            "2.11.1": not_solved(),
            "2.11.2": not_solved(),
            "3.1.1": solved(),
            "3.1.2": solved(),
            "3.1.3": solved(),
            "3.1.4": solved(),
            "3.1.5": solved(),
            "3.1.6": solved(),
            "3.1.7": solved(),
            "3.2.1": not_solved(),
        }
    )

    generate(
        from_template=template,
        using=configuration,
        to=f"{directory}/motor-controller.ipynb",
    )

    generate(
        from_template=template,
        using=configuration.all_solved(),
        to=f"{directory}/motor-controller-solution.ipynb",
    )

    generate(
        from_template=template,
        using=configuration.none_solved(),
        to=f"{directory}/motor-controller-challenge.ipynb",
    )


class Exercise(Enum):
    ROBOT_ARM = ("robot-arm", generate_robot_arm)
    MOTOR_CONTROLLER = ("motor-controller", generate_motor_controller)

    generate: Generator

    def __init__(self, reference: str, generate: Generator) -> None:
        self._value_ = reference
        self.generate = generate

    @staticmethod
    def options() -> list[str]:
        return [exercise.value for exercise in Exercise]

    @staticmethod
    def get(exercise: str) -> "Exercise":
        for it in Exercise:
            if it.value == exercise.lower():
                return it

        raise ValueError(f"Exercise {exercise} not found.")


class ExerciseChoice(Choice):
    def __init__(self) -> None:
        super().__init__(Exercise.options(), case_sensitive=False)

    def convert(
        self, value: Any, param: Parameter | None, ctx: Context | None
    ) -> Exercise:
        value = super().convert(value, param, ctx)
        return Exercise.get(value)


def format_exercises() -> None:
    subprocess.run(["ruff", "format"], check=True)


@click.command()
@click.option(
    "--exercises",
    type=ExerciseChoice(),
    default=[Exercise.ROBOT_ARM.value, Exercise.MOTOR_CONTROLLER.value],
    multiple=True,
    help="The exercises to generate.",
)
def main(exercises: list[Exercise]) -> None:
    for exercise in exercises:
        exercise.generate()

    format_exercises()


if __name__ == "__main__":
    main()
