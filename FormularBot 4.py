from tools import  *
from objects import *
from routines import *


class FormularBot(GoslingAgent):
    def run(agent):

        my_goal_to_ball,my_ball_distance = (agent.ball.location - agent.friend_goal.location).normalize(True)
        goal_to_me = agent.me.location - agent.friend_goal.location
        my_distance = my_goal_to_ball.dot(goal_to_me)
        me_onside = my_distance + 80 < my_ball_distance

        close = (agent.me.location - agent.ball.location).magnitude() < 4000

        relative_target = agent.ball.location - agent.friend_goal.location
        distance_ball_friendly_goal = relative_target.magnitude()

        left_field = Vector3(4200*-side(agent.team),agent.ball.location.y + 1000*-side(agent.team),0)
        right_field = Vector3(4200*side(agent.team),agent.ball.location.y + 1000*-side(agent.team),0)
        targets = {"goal": (agent.foe_goal.left_post,agent.foe_goal.right_post), "upfield": (left_field,right_field)}
        shots = find_hits(agent,targets)

        allies = agent.friends
        closest_ally_to_ball = "none"
        closest_ally_to_ball_distance = 9999
        distance_to_ball = (agent.me.location - agent.ball.location).flatten().magnitude()

        for item in allies:
            item_distance = (item.location - agent.ball.location).flatten().magnitude()
            if item_distance < closest_ally_to_ball_distance:
                closest_ally_to_ball = item
                closest_ally_to_ball_distance = item_distance
        

        if agent.index == 0:
            agent.debug_stack()
            #agent.line(agent.friend_goal.location, agent.ball.location, [255,255,255])
            #my_point = agent.friend_goal.location + (my_goal_to_ball * my_distance)
            #agent.line(my_point - Vector3(0,0,100), my_point + Vector3(0,0,500), [0,255,0])



        if len(agent.stack) < 1:
            if agent.kickoff_flag and distance_to_ball <= closest_ally_to_ball_distance:
                agent.push(kickoff)
            elif me_onside:
                if len(shots["goal"]) > 0:
                    agent.push(shots["goal"][0])
                    #send(random.choice(chat_ids))
                elif len(shots["upfield"]) > 0 and abs(agent.friend_goal.location.y - agent.ball.location.y) < 8490:
                    agent.push(shots["upfield"][0])
                else:  
                    agent.push(short_shot(agent.foe_goal.location))
                    if len(agent.stack) < 1:
                        if agent.me.location.y > 0*side(agent.team):
                            agent.push(ball_chase)
                        else:
                            agent.push(goto_friendly_goal)
            elif distance_ball_friendly_goal > 6000:
                if agent.me.boost < 20:
                    agent.push(get_nearest_big_boost)
                else:
                    agent.push(demo_enemy_closest_ball(True))
            else:
                agent.push(goto_friendly_goal)
