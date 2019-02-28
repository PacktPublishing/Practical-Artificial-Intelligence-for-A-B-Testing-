from flask import Flask, redirect, render_template, url_for
import numpy as np

app = Flask( __name__ )

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
        # code the omniscient agent
        bandit_machine = np.argmax( agent.get_prob_list() )

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

    agent = OmniscientAgent( prob_list, trials, episodes )

    app.config['AGENT'] = agent
    app.run()

