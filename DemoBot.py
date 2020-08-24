from tools import  *
from objects import *
from routines import *

class DemoBot(GoslingAgent):
    def run(agent):
        #Works out kickoff position and passes that variable onto kickoff function in routines
        x_position = int(agent.me.location.x * side(agent.team))
        if x_position == 2047 or x_position == 2048:
            kickoff_position = 'diagonal_right'
        elif x_position == -2047 or x_position == -2048:
            kickoff_position = 'diagonal_left'
        elif x_position == -255 or x_position == -256:
            kickoff_position = 'back_left'
        elif x_position == 255 or x_position == 256:
            kickoff_position = 'back_right'
        elif x_position == 0:
            kickoff_position = 'back_centre'
        else:
            kickoff_position = 'unknown'

        if agent.index == 0:
            agent.debug_stack()
            
        if len(agent.stack) < 1:     
            if agent.kickoff_flag:
                agent.push(kickoff(kickoff_position))
            else:
                #If not going doing kickoff pushes demo routine to stack
                agent.push(demo_enemy_closest_ball)
        
        #Jumps if turtling
        if agent.me.velocity[0] == 0 and agent.me.orientation[2][2] < 0:
            agent.controller.jump = True