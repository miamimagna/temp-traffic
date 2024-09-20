import gymnasium as gym
import sumo_rl

env = gym.make('sumo-rl-v0',
                net_file='../network_details/intersection.net.xml',
                route_file='../routes/High Traffic Scenerio/test/emergency_0/intersection.rou.xml',
                out_csv_name='../outputs/round_robin_HT_0',
                min_green=25,
                yellow_time=5,
                delta_time=10,
                use_gui=True,
                num_seconds=5400)

obs, info = env.reset()
done = False
 
action_index = 0  
while not done:
    action = action_index % 4
    
    next_obs, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated

    action_index += 1

obs, info = env.reset()
env.close()