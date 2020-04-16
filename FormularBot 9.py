from tools import  *
from objects import *
from routines import *


class FormularBot(GoslingAgent):
    def run(agent):

        relative_target = agent.ball.location - agent.friend_goal.location
        distance_ball_friendly_goal = relative_target.magnitude()

        enemies = agent.foes
        closest = enemies[0]
        closest_distance = (enemies[0].location - agent.ball.location).magnitude()
        x = 0
        y = 0
        for item in enemies:
            item_distance = (item.location - agent.ball.location).magnitude()
            if item_distance < closest_distance:
                closest = item
                closest_distance = item_distance
                y = x
            x =+ 1

        my_goal_to_ball,my_ball_distance = (agent.ball.location - agent.friend_goal.location).normalize(True)
        goal_to_me = agent.me.location - agent.friend_goal.location
        my_distance = my_goal_to_ball.dot(goal_to_me)
        me_onside = my_distance + 80 < my_ball_distance

        close = (agent.me.location - agent.ball.location).magnitude() < 750
        distance_to_ball = (agent.me.location - agent.ball.location).flatten().magnitude()
        distance_to_friendly_goal = (agent.me.location - agent.friend_goal.location).flatten().magnitude()

        relative_target = agent.ball.location - agent.friend_goal.location
        distance_ball_friendly_goal = relative_target.magnitude()

        left_field = Vector3(4200*-side(agent.team),agent.ball.location.y + 1000*-side(agent.team),0)
        right_field = Vector3(4200*side(agent.team),agent.ball.location.y + 1000*-side(agent.team),0)
        targets = {"goal": (agent.foe_goal.left_post,agent.foe_goal.right_post), "upfield": (left_field,right_field)}
        shots = find_hits(agent,targets)

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
            #print(closest_to_ball)
            #print(distance_to_ball,closest_ally_to_ball_distance)
            #print(close)
            #print(me_onside)
            #print(distance_ball_friendly_goal)
            #agent.line(agent.foe_goal.left_post,agent.foe_goal.right_post)
            #print(Vector3(agent.ball.location))
            #print(closest_ally_friendly_goal_distance,distance_to_friendly_goal)
            #agent.line(agent.friend_goal.location, agent.ball.location, [255,255,255])
            #my_point = agent.friend_goal.location + (my_goal_to_ball * my_distance)
            #agent.line(my_point - Vector3(0,0,100), my_point + Vector3(0,0,500), [0,255,0])

        if closest_ally_friendly_goal_distance > distance_to_friendly_goal and distance_ball_friendly_goal > 6000 and agent.stack != goto_friendly_goal and len(agent.friends) > 0:
            agent.clear()
        elif (agent.stack == short_shot or agent.stack == jump_shot or agent.stack == aerial_shot) and not(me_onside and (closest_to_ball or closest_ally_friendly_goal_distance > distance_to_friendly_goal and distance_ball_friendly_goal < 5000 or (agent.ball.location.y * side(agent.team) * -1 > 4200 * side(agent.team) * -1) and agent.ball.location.x < 1500 and agent.ball.location.x > -1500)):
            agent.clear()

        if len(agent.stack) < 1:
            if agent.kickoff_flag and closest_to_ball:
                agent.push(kickoff(int(agent.me.location.x * side(agent.team))))

            elif closest_ally_friendly_goal_distance > distance_to_friendly_goal and len(agent.friends) > 0 and (distance_ball_friendly_goal > 6000 or agent.kickoff_flag):
                agent.push(goto_friendly_goal)
            elif me_onside and (closest_to_ball or closest_ally_friendly_goal_distance > distance_to_friendly_goal and distance_ball_friendly_goal < 5000 or (agent.ball.location.y * side(agent.team) * -1 > 4200 * side(agent.team) * -1) and agent.ball.location.x < 1500 and agent.ball.location.x > -1500):
                if len(shots["goal"]) > 0:
                    agent.push(shots["goal"][0])
                    #send(random.choice(chat_ids))
                elif len(shots["upfield"]) > 0 and abs(agent.friend_goal.location.y - agent.ball.location.y) < 8490:
                    agent.push(shots["upfield"][0])
                else:  
                    agent.push(short_shot(agent.foe_goal.location))
            elif distance_ball_friendly_goal > 6000:
                if agent.me.boost < 20:
                    agent.push(get_nearest_big_boost)
                else:
                    agent.push(go_centre)
            else:
                if not close:
                    if closest_ally_friendly_goal_distance > distance_to_friendly_goal:
                        agent.push(goto_friendly_goal)
                    else:
                        agent.push(go_centre)
                else:
                    agent.push(get_nearest_big_boost)
