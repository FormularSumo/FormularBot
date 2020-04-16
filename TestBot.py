from tools import  *
from objects import *
from routines import *
import time

class TestBot(GoslingAgent):
    def run(agent):

        distance_to_ball = (agent.me.location - agent.ball.location).flatten().magnitude()

        allies = agent.friends
        cally_to_ball = "none"
        ally_to_ball_distance = 99999
        ally_to_friendly_goal = "none"
        ally_to_friendly_goal_distance = 99999

        for item in allies:
            item_distance = (item.location - agent.ball.location).flatten().magnitude()
            item_goal_distance = (item.location - agent.friend_goal.location).flatten().magnitude()
            if item_distance < ally_to_ball_distance:
                ally_to_ball = item
                ally_to_ball_distance = item_distance
            if item_goal_distance < ally_to_friendly_goal_distance:
                ally_to_friendly_goal = item
                ally_to_friendly_goal_distance = item_goal_distance

        closest_ally_to_ball_distance = ally_to_ball_distance
        closest_ally_friendly_goal_distance = ally_to_friendly_goal_distance 


        closest_to_ball = distance_to_ball <= closest_ally_to_ball_distance

        if agent.index == 0:
            agent.debug_stack()
        if len(agent.stack) < 1:
            #if agent.kickoff_flag and closest_to_ball:
                #agent.push(kickoff(int(agent.me.location.x * side(agent.team))))      
            agent.push(half_flip())     


            
