from tools import  *
from objects import *
from routines import *
        


class DemoBot(GoslingAgent):
    def run(agent):
        if agent.index == 0:
            agent.debug_stack()
        if len(agent.stack) < 1:     
            if agent.kickoff_flag:
                agent.push(kickoff(int(agent.me.location.x * side(agent.team))))
            else:
                agent.push(demo_enemy_closest_ball(True))