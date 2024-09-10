import os
import subprocess
import trips_generator.weibull_trips as weibull_trips
from trips_generator.config import *
from scenes_config import *


def create_directory(path: str) -> None:
    """
    Create a directory if it doesn't already exist.

    Args:
        path (str): The path of the directory to create.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def generate_trips(scene: str, env_type: str, emergency_prob: float) -> None:
    """
    Generates trip files using the Weibull distribution and converts them to SUMO route files.

    Args:
        scene (str): The current scene being processed.
        env_type (str): The environment type, either 'train' or 'test'.
        emergency_prob (float): The probability of generating an emergency vehicle.
    """
    # Generate the trips using Weibull distribution
    weibull_trips.main(
        src_nodes,
        dst_nodes,
        scene_src_probabilities[scene],
        turn_prob,
        emergency_prob,
        shape,
        scene_number_cars[scene],
        total_timesteps,
    )

    # Run the DUARouter to convert trips to routes
    subprocess.run(
        [
            "duarouter",
            "-n",
            "intersection.net.xml",  # Input network file
            "-t",
            "trips.trips.xml",  # Input trips file
            "-o",
            f"routes/{scene}/{env_type}/emergency_{emergency_prob}/intersection.rou.xml",  # Output routes file
        ]
    )


def process_scene(scene: str) -> None:
    """
    Process each scene by generating directories and trip files for both 'test' and 'train' environments.

    Args:
        scene (str): The scene name to process.
    """
    # Create base directories for the scene
    create_directory(f"routes/{scene}")

    # Process both 'test' and 'train' environments
    for env_type in ["test", "train"]:
        create_directory(f"routes/{scene}/{env_type}")

        # Generate trips for both normal and emergency conditions
        for e_prob in [0, emergency_prob]:
            output_dir = f"routes/{scene}/{env_type}/emergency_{e_prob}"
            create_directory(output_dir)

            # Generate trips and routes for the current configuration
            generate_trips(scene, env_type, e_prob)


def main() -> None:
    """
    Main function to generate trips and route files for all scenes.
    """
    # Ensure the base routes directory exists
    create_directory("routes")

    # Process each scene's configuration
    for scene in scene_src_probabilities:
        process_scene(scene)


if __name__ == "__main__":
    main()
