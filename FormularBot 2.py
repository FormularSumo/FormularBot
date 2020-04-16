from tools import  *
from objects import *
from routines import *


class FormularBot0.2(GoslingAgent):
    def run(agent):
        
        close = (agent.me.location - agent.ball.location).magnitude() < 2000
        have_boost = agent.me.boost > 20
        relative_target = agent.ball.location - agent.friend_goal.location
        distance_ball_friendly_goal = relative_target.flatten().magnitude()


        if agent.index == 0:
            agent.debug_stack()


        targets = {"goal" : (agent.foe_goal.left_post,agent.foe_goal.right_post)}
        shots = find_hits(agent,targets)
        


        if len(agent.stack) < 1:
            if agent.kickoff_flag:
                agent.push(kickoff())
            else:
                if len(shots["goal"]) > 0:
                    agent.push(shots["goal"][0])
                else:    
                    if (not have_boost) and distance_ball_friendly_goal > 6000 and close == False :
                        agent.push(get_nearest_big_boost)
                    else:
                        agent.push(short_shot(agent.foe_goal.location))