from scipy.stats import binom, beta
from matplotlib import pyplot as plt
import numpy as np
import random

def reward_plot( success_array, failure_array ):
    linestyles = ['-', '--']

    x = np.linspace( 0, 1, 1002 )[1:-1]

    plt.clf()
    plt.xlim( 0, 1 )
    plt.ylim( 0, 30 )

    for a, b, ls in zip( success_array, failure_array, linestyles ):
        dist = beta( a, b )

        plt.plot( x, dist.pdf( x ), ls=ls, c='black', label='Alpha:{}, Beta:{}'.format( a, b ))

        plt.draw()
        plt.pause( 0.01 )

        plt.legend( loc=0 )

class ThompsonAgent( object ):
    def __init__( self, prob_list ):
        self.prob_list = prob_list

    def pull( self, bandit_machine ):
        if np.random.random() < self.prob_list[ bandit_machine ]:
            reward = 1
        else:
            reward = 0
        return reward

prob_list = [0.3, 0.8 ]

trials = 1000
episodes = 200

eps_init = 1
decay = 0.01

eps_array = [ ( eps_init * ( 1 - decay ) ) ** i for i in range( trials ) ]

bandit = ThompsonAgent( prob_list )

prob_reward_array = np.zeros( len( prob_list ) )
accumulated_reward_array = list()
avg_accumulated_reward_array = list()

for episode in range( episodes ):
    if episode % 10 == 0:
        print( 'Episode: {} / {}'.format( episode, episodes ) )

    success_array = np.ones( len( prob_list ) )
    failure_array = np.ones( len( prob_list ) )

    reward_array = np.zeros( len( prob_list ) )
    bandit_array = np.full( len( prob_list ), 1.0e-5 )
    accumulated_reward = 0

    for trial in range( trials ):
        # define the random strategy
        prob_reward = np.random.beta( success_array, failure_array )
        bandit_machine = np.argmax( prob_reward )

        # get the reward
        reward = bandit.pull( bandit_machine )

        if reward == 1:
            success_array[ bandit_machine ] += 1
        else:
            failure_array[ bandit_machine ] += 1

        # plot
        reward_plot( success_array, failure_array )

        # save the partial results
        reward_array[ bandit_machine ] += reward
        bandit_array[ bandit_machine ] += 1
        accumulated_reward += reward

    # compute the partial results
    prob_reward_array += reward_array / bandit_array
    accumulated_reward_array.append( accumulated_reward )
    avg_accumulated_reward_array.append( np.mean( accumulated_reward_array ) )

# compute the final results
prob_01 = 100*np.round( prob_reward_array[0] / episodes, 2 )
prob_02 = 100*np.round( prob_reward_array[1] / episodes, 2 )

# print the final results
print( '\n Prob Bandit 01:{}% - Prob Bandit 02:{}%\n'.format( prob_01, prob_02 ) )
print( '\nAvg accumulated reward:{}\n'.format( np.mean( avg_accumulated_reward_array ) ) )
