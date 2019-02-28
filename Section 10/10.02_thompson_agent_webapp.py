from flask import Flask, redirect, render_template, url_for
import numpy as np

app = Flask( __name__ )

class ThompsonAgent( object ):
    def __init__( self, pro_list, trials, episodes ):
        self.prob_list = prob_list
        self.trials = trials
        self.episodes = episodes

        self.trial = 0
        self.episode = 0
        self.current_bandit = 0
        self.accumulated_reward = 0

        self.success_array = np.ones( len( self.prob_list ) )
        self.failure_array = np.ones( len( self.prob_list ) )

        self.reward_array = np.zeros( len( self.prob_list ) )
        self.prob_reward_array = np.zeros( len( self.prob_list ) )
        self.bandit_array = np.full( len( self.prob_list ), 1.0e-5 ) 
        self.accumulated_reward_array = list()
        self.avg_accumulated_reward_array = list()

    def set_current_bandit( self, bandit_machine ):
        self.current_bandit = bandit_machine
        return None

    def set_success_array( self, bandit_machine ):
        self.success_array[ bandit_machine ] += 1
        return None

    def set_failure_array( self, bandit_machine ):
        self.failure_array[ bandit_machine ] += 1
        return None

    def set_reward_array( self, bandit_machine, reward ):
        self.reward_array[ bandit_machine ] += reward
        return None

    def set_bandit_array( self, bandit_machine ):
        self.bandit_array[ bandit_machine ] += 1
        return None

    def set_trial( self, reset ):
        if reset == 1:
            self.trial = 0
            self.reward_array = np.zeros( len( self.prob_list ) )
            self.bandit_array = np.full( len( self.prob_list ), 1.0e-5 )
            self.accumulated_reward = 0
        else:
            self.trial += 1

        return None

    def set_episode( self ):
        self.episode += 1
        return None

    def set_prob_reward_array( self ):
        self.prob_reward_array += self.reward_array / self.bandit_array
        return None

    def set_accumulated_reward( self, reward ):
        self.accumulated_reward += reward
        return None

    def set_append_accumulated_reward( self ):
        self.accumulated_reward_array.append( self.accumulated_reward )
        return None

    def set_append_avg_accumulated_reward( self ):
        self.avg_accumulated_reward_array.append( np.mean( self.accumulated_reward_array ) )
        return None

    def reset_episode( self ):
        self.episode = 0
        return None

    # getters
    def get_prob_list( self ):
        return self.prob_list

    def get_current_bandit( self ):
        return self.current_bandit

    def get_success_array( self ):
        return self.success_array
    
    def get_failure_array( self ):
        return self.failure_array

    def get_prob_reward_array( self ):
        return self.prob_reward_array

    def get_avg_accumulated_reward_array( self ):
        return self.avg_accumulated_reward_array

    def get_trial( self ):
        return self.trial

    def get_trials( self ):
        return self.trials

    def get_episode( self ):
        return self.episode

    def get_episodes( self ):
        return self.episodes

@app.route( '/home' )
def index():
    # retrieve the agent
    agent = app.config['AGENT']

    print( 'Episode: {}/{}'.format( agent.get_episode(), agent.get_episodes() ) )
    print( 'Trial: {}/{}'.format( agent.get_trial(), agent.get_trials() ) )
    if agent.get_episode() > agent.get_episodes():
        # episodes are over
        # compute the final prob
        prob_reward_array = agent.get_prob_reward_array()
        prob_01 = 100*np.round( prob_reward_array[0] / agent.get_episodes(), 2 )
        prob_02 = 100*np.round( prob_reward_array[1] / agent.get_episodes(), 2 )

        # avg the accumulated reward
        avg_accumulated_reward = agent.get_avg_accumulated_reward_array()

        # print the final 
        print( '\nProb Bandit 01:{}% - Prob Bandit 02:{}%'.format( prob_01, prob_02 ) )
        print( '\n Avg accumulated reward: {}\n'.format( np.mean( avg_accumulated_reward ) ) )

        # reset the episodes
        agent.reset_episode()

    elif agent.get_trial() > agent.get_trials():
        # trials are over
        # increase the episode
        agent.set_episode()

        # compute the partial results
        agent.set_prob_reward_array()

        # append the accumualted reward
        agent.set_append_accumulated_reward()

        # append the avg accumulated reward
        agent.set_append_avg_accumulated_reward()

        # reset the trial and initial variables
        agent.set_trial( reset=1 )

        # get the partial results
        partial_result = agent.get_prob_reward_array()
        prob_01 = partial_result[0] / agent.get_episode()
        prob_02 = partial_result[1] / agent.get_episode()

        # print the partial results
        print( '\n Prob Bandit 01:{} - Prob Bandit 02:{}\n'.format( prob_01, prob_02 ) )
        return redirect( url_for( 'index' ) )

    else:
        # trials are not over
        prob_reward = np.random.beta( agent.get_success_array(), agent.get_failure_array() )
        bandit_machine = np.argmax( prob_reward )

        print( 'Success array: {}'.format( agent.get_success_array() ) )
        print( 'Failure array: {}'.format( agent.get_failure_array() ) )

        # set the current bandit machine
        agent.set_current_bandit( bandit_machine )

        # pick up the web page
        if bandit_machine == 0: # red Yes button
            return render_template( 'layout_red.html' )
        else:
            return render_template( 'layout_blue.html' )

@app.route( '/yes', methods=['POST'] )
def yes_event():
    agent = app.config['AGENT']

    # set the reward
    reward = 1

    # get the current bandit machine
    bandit_machine = agent.get_current_bandit()

    # increase the success array
    agent.set_success_array( bandit_machine )

    # add a reward to the bandit machine
    agent.set_reward_array( bandit_machine, reward )

    # increase how many times the bandit machine gets the lever pulled
    agent.set_bandit_array( bandit_machine )

    # sum the accumulated reward
    agent.set_accumulated_reward( reward )

    # increase the number of trial
    agent.set_trial( reset=0 )

    return redirect( url_for( 'index' ) )

@app.route( '/no', methods=['POST'] )
def no_event():
    agent = app.config['AGENT']

    # set the reward
    reward = 0

    # get the current bandit machine
    bandit_machine = agent.get_current_bandit()

    # increase the failure array
    agent.set_failure_array( bandit_machine )

    # add a reward to the bandit machine
    agent.set_reward_array( bandit_machine, reward )

    # increase how many times the bandit machine gets the lever pulled
    agent.set_bandit_array( bandit_machine )

    # sum the accumulated reward
    agent.set_accumulated_reward( reward )

    # increase the number of trial
    agent.set_trial( reset=0 )
    return redirect( url_for( 'index' ) )

if __name__ == "__main__":
    trials = 100
    episodes = 20

    prob_list = [0.3, 0.8]

    agent = ThompsonAgent( prob_list, trials, episodes )

    app.config['AGENT'] = agent
    app.run()

