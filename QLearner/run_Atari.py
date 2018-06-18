"""
Deep Q network,

Using:
Tensorflow: 0.11
gym: 0.8.0
"""


import gym
from RL_brain import DeepQNetwork
import scipy
import skimage.transform
import numpy as np

env = gym.make('Kangaroo-v4')
env = env.unwrapped

print(env.action_space)
print(env.observation_space)
#print(env.observation_space.high)
#print(env.observation_space.low)

RL = DeepQNetwork(n_actions=18, n_features=9072, learning_rate=0.001, e_greedy=0.9,
                  replace_target_iter=300, memory_size=3000,
                  e_greedy_increment=0.0002,)

total_steps = 0


for i_episode in range(1000):

    observation = skimage.transform.rescale(env.reset(),0.3).flatten()
    #print(np.shape(observation))
    #print(np.shape(skimage.transform.rescale(observation,0.3).flatten()))
    ep_r = 0

    while True:
        env.render()

        action = RL.choose_action(observation)

        observation_, reward, done, info = env.step(action)
        observation_ = skimage.transform.rescale(observation_,0.3).flatten()
        
        #position, velocity = observation_

        # the higher the better
        #reward = abs(position - (-0.5))     # r in [0, 1]

        RL.store_transition(observation, action, reward, observation_)

        if total_steps > 1000:
            RL.learn()

        ep_r += reward
        if done:
            get = '| Get | ----'
            print('Epi: ', i_episode,
                  get,
                  '| Ep_r: ', round(ep_r, 4),
                  '| Epsilon: ', round(RL.epsilon, 2))
            break

        observation = observation_
        total_steps += 1

RL.plot_cost()

