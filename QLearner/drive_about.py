"""
Deep Q network,

Using:
Tensorflow: 0.11
gym: 0.8.0
"""


from RL_brain import DeepQNetwork
import scipy
import skimage.transform
import numpy as np
import driving_env

n_act = 3
height = 64
width = 64
n_c = 3

RL = DeepQNetwork(n_actions=n_act, n_features=height*width*n_c, learning_rate=0.001, e_greedy=0.9,
                  replace_target_iter=300, memory_size=3000,
                  e_greedy_increment=0.0002,)

total_steps = 0

env = driving_env.driving_env(height,width)
for i_episode in range(1000):
    
    observation = env.reset()
    ep_r = 0

    while True:

        action = RL.choose_action(observation)

        observation_, reward, done, info = env.step(action)

        RL.store_transition(observation, action, reward, observation_)

        ep_r += reward
        if done:
            observation = env.reset()
            get = '| Get | ----'
            print('Epi: ', i_episode,
                  get,
                  '| Ep_r: ', round(ep_r, 4),
                  '| Epsilon: ', round(RL.epsilon, 2))
            break

        observation = observation_
        total_steps += 1
        if total_steps > 100:
                        RL.learn()
        
RL.plot_cost()

