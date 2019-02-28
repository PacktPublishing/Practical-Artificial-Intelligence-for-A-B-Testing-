import numpy as np
import random

# define the multi-armed bandit machine
class MultiBandit( object ):
    def __init__( self, prob_list ):
        self.prob_list = prob_list

    def pull( self, bandit_machine ):
        if np.random.random() < self.prob_list[ bandit_machine]:
            event = 1
        else:
            event = 0

        return event

prob_list = [0.3, 0.8]
num_bandit = len( prob_list )

# define the experiment
bandit = MultiBandit( prob_list )

trials = 1000
episodes = 200

prob_reward_array = np.zeros( num_bandit )
accumulated_reward_array = list()
avg_accumulated_reward_array = list()

for episode in range( episodes ):
    reward_array = np.zeros( num_bandit )
    bandit_machine_array = np.full( num_bandit, 1.0e-5 )
    accumulated_reward = 0

    for trial in range( trials ):
        bandit_machine = np.argmax( prob_list )

        reward = bandit.pull( bandit_machine )

        reward_array[ bandit_machine ] += reward
        bandit_machine_array[ bandit_machine ] += 1
        accumulated_reward += reward

    prob_reward_array += reward_array / bandit_machine_array
    accumulated_reward_array.append( accumulated_reward )
    avg_accumulated_reward_array.append( np.mean( accumulated_reward_array ) )

prob_machine_01 = 100*np.round( prob_reward_array[0] / episodes, 2 ) 
prob_machine_02 = 100*np.round( prob_reward_array[1] / episodes, 2 ) 

print( '\n Prob Bandit machine 01:{} - Prob Bandit machine 02:{}'.format( prob_machine_01, prob_machine_02 ) )

print( '\nAvg accumulated reward: {}\n'.format( np.mean( avg_accumulated_reward_array ) ) )













