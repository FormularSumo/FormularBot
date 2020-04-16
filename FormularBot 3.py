from tools import  *
from objects import *
from routines import *


class FormularBot3(GoslingAgent):
    def run(agent):
        
        my_goal_to_ball,my_ball_distance = (agent.ball.location - agent.friend_goal.location).normalize(True)
        goal_to_me = agent.me.location - agent.friend_goal.location
        my_distance = my_goal_to_ball.dot(goal_to_me)


        me_onside = my_distance + 80 < my_ball_distance
        close = (agent.me.location - agent.ball.location).magnitude() < 2000
        have_boost = agent.me.boost > 20
        relative_target = agent.ball.location - agent.friend_goal.location
        distance_ball_friendly_goal = relative_target.flatten().magnitude()
        
        left_field = Vector3(4200*-side(agent.team),agent.ball.location.y + 1000*-side(agent.team),0)
        right_field = Vector3(4200*side(agent.team),agent.ball.location.y + 1000*-side(agent.team),0)
        targets = {"goal" : (agent.foe_goal.left_post + Vector3(50*side(agent.team),0,0),agent.foe_goal.right_post - Vector3(50*side(agent.team),0,0)), "upfield": (left_field,right_field)}
        shots = find_hits(agent,targets)

        if agent.index == 0:
            agent.debug_stack()
            #print(distance_ball_friendly_goal)
            #agent.line(agent.foe_goal.left_post + Vector3(50*side(agent.team),0,0),agent.foe_goal.right_post - Vector3(50*side(agent.team),0,0), [0,0,0])
            #agent.line(agent.foe_goal.left_post,agent.foe_goal.right_post, [255,255,255])

        

        if len(agent.stack) < 1:
            if agent.kickoff_flag:
                agent.push(kickoff)
            else:
                if len(shots["goal"]) > 0:
                    agent.push(shots["goal"][0])
                elif len(shots["upfield"]) > 0 and abs(agent.friend_goal.location.y - agent.ball.location.y) < 8490:
                    agent.push(shots["upfield"][0])
                else:    
                    if (not have_boost) and distance_ball_friendly_goal > 6000 and close == False :
                        agent.push(get_nearest_big_boost)
                    else:
                        agent.push(short_shot(agent.foe_goal.location))