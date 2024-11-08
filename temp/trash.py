import gymnasium as gym
import sumo_rl
env = gym.make('sumo-rl-v0',
                net_file='../network_details/intersection.net.xml',
                route_file='../routes/High Traffic Scenerio/test/emergency_0/intersection.rou.xml',
                out_csv_name='../output/this.csv',
                min_green=25,
                yellow_time=5,
                delta_time=10,
                use_gui=True,
                num_seconds=500)
obs, info = env.reset()
done = False
action = 0  
cnt = 0
while not done:
    next_obs, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated
    cnt = cnt + 1
    if action == 1: 
        action = 2
    elif action == 0:
        action = 3
    elif action == 2:
        action = 0
    elif action == 3:
        action = 1

obs, info = env.reset()
env.close()