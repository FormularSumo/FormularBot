from tools import  *
from objects import *
from routines import *



class FormularBot(GoslingAgent):
    def run(agent):
        agent.debug_stack()
        targets = {"goal" : (agent.foe_goal.left_post,agent.foe_goal.right_post)}
        shots = find_hits(agent,targets)
        if len(agent.stack) < 1:
            if len(shots["goal"]) > 0:
                agent.push(shots["goal"][0])
            else:    
                if agent.me.boost < 30:
                    agent.push(get_nearest_big_boost)
                    
                else:
                    agent.push(short_shot(agent.foe_goal.location))
