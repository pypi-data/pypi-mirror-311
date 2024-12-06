from typing import Any, NamedTuple, Protocol, TypeVar, Generic, Iterable
from helpers.robot.arm import AnimateableRobotArm

import plotly.graph_objects as go


class JointAngles(NamedTuple):
    """Angles describing the configuration of a robot arm.

    Attributes:
        theta_1: The angle of the first joint.
        theta_2: The angle of the second joint.

    Example:
        This is useful for animating the robot arm at different configurations. See the
        [`animate`](helpers.robot.animation.html#helpers.robot.animation.animate) function for more details.
    """

    theta_1: float
    theta_2: float

    @staticmethod
    def combining(
        theta_1s: Iterable[float], theta_2s: Iterable[float]
    ) -> list["JointAngles"]:
        """Combines two lists of angles into a single list of `JointAngles`."

        Args:
            theta_1s: The angles of the first joint.
            theta_2s: The angles of the second joint.

        Returns:
            A list of `JointAngles` where each element is a pair of angles from the input lists.

        Example:
            ```python
            theta_1s = [pi, pi / 2, 0]
            theta_2s = [0, pi / 2, pi]
            joint_angles = JointAngles.combining(theta_1s, theta_2s)
            print(joint_angles)
            # Output: [
            #   JointAngles(theta_1=pi, theta_2=0),
            #   JointAngles(theta_1=pi / 2, theta_2=pi / 2),
            #   JointAngles(theta_1=0, theta_2=pi)
            # ]
            ```
        """
        return [
            JointAngles(theta_1, theta_2)
            for theta_1, theta_2 in zip(theta_1s, theta_2s)
        ]


RobotT = TypeVar("RobotT", infer_variance=True, bound=AnimateableRobotArm)


class AnimationFramesProvider(Protocol, Generic[RobotT]):
    def __call__(
        self, robot: RobotT, joint_angles: list[JointAngles]
    ) -> list[go.Figure]:
        """Returns the frames of the robot arm animation."""
        ...


def animate(
    robot: RobotT,
    joint_angles: list[JointAngles],
    *,
    animation_frames_for: AnimationFramesProvider[RobotT],
    align_starting_position: bool = False,
    subtitle: str = "",
) -> None:
    if align_starting_position:
        robot.rotate_to(*joint_angles[0])

    starting_frame = robot.draw(show=False, trace=[robot.end_effector_position()])
    figure = go.Figure(
        data=starting_frame.data,
        layout=starting_frame.layout,
        frames=[
            go.Frame(data=figure.data)
            for figure in animation_frames_for(robot, joint_angles)
        ],
    )

    figure.update_layout(
        title=f"Animated {robot.name} {subtitle}",
        updatemenus=[animation_configuration()],
    )
    figure.show()


def animation_configuration() -> dict[str, Any]:
    return dict(
        type="buttons",
        buttons=[
            dict(
                label="Play",
                method="animate",
                args=[
                    None,
                    {
                        "frame": {"duration": 10, "redraw": True},
                        "fromcurrent": True,
                        "transition": {"duration": 0},
                    },
                ],
            )
        ],
    )
