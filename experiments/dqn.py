import os
import sys

import gymnasium as gym
from stable_baselines3.dqn.dqn import DQN


# if "SUMO_HOME" in os.environ:
#     tools = os.path.join(os.environ["SUMO_HOME"], "tools")
#     sys.path.append(tools)
# else:
#     sys.exit("Please declare the environment variable 'SUMO_HOME'")
import traci

from sumo_rl import SumoEnvironment


if __name__ == "__main__":
    env = SumoEnvironment(
        net_file="../network_details/intersection.net.xml",
        route_file="../routes/High Traffic Scenerio/test/emergency_0.05/intersection.rou.xml",
        out_csv_name="../outputs/2way-single-intersection/dqn",
        single_agent=True,
        use_gui=False,
        num_seconds=5400,
    )

    model = DQN(
        env=env,
        policy="MlpPolicy",
        learning_rate=0.001,
        learning_starts=0,
        train_freq=1,
        target_update_interval=500,
        exploration_initial_eps=0.05,
        exploration_final_eps=0.01,
        verbose=1,
    )
    model.learn(total_timesteps=5400)
