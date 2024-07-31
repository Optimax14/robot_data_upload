#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import random

# Define possible object classes
object_classes = ['table', 'chair', 'lamp']
data = []

def generate_random_pose():
    return [random.randint(-5, 5), random.randint(-5, 5), 0]

for i in range(1, 31):
    entry = {
        'name': f'{i:06d}', 
        'pose': generate_random_pose(),  
        'class': random.choice(object_classes)  
    }
    data.append(entry)
print(data)

def get_first_occurrence_pose(data, target_class):
    for entry in data:
        if entry['class'] == target_class:
            return entry['pose']
    return None

def movebase_client(x, y):
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    def send_goal_and_wait():
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        goal.target_pose.pose.orientation.w = 1  

        client.send_goal(goal)
        wait = client.wait_for_result()  
        return wait

    def get_status():
        state = client.get_state()
        if state == actionlib.GoalStatus.SUCCEEDED:
            rospy.loginfo("Goal reached successfully!")
            return "SUCCEEDED"
        elif state == actionlib.GoalStatus.PREEMPTED:
            rospy.logwarn("Goal was preempted (interrupted)!")
            return "PREEMPTED"
        elif state == actionlib.GoalStatus.ABORTED:
            rospy.logerr("Goal was aborted!")
            return "ABORTED"
        elif state == actionlib.GoalStatus.REJECTED:
            rospy.logerr("Goal was rejected!")
            return "REJECTED"
        elif state == actionlib.GoalStatus.PENDING:
            rospy.loginfo("Goal is pending (not yet started)!")
            return "PENDING"
        elif state == actionlib.GoalStatus.ACTIVE:
            rospy.loginfo("Goal is currently being executed!")
            return "ACTIVE"

    retry = False
    for attempt in range(2):
        rospy.loginfo(f"Attempt {attempt + 1} to reach the goal.")
        if send_goal_and_wait():
            status = get_status()
            if status == "SUCCEEDED":
                return client.get_result()
            elif status == "ABORTED":
                retry = True
        else:
            rospy.logerr("Action server not available or timed out!")

        if retry and attempt == 0:
            rospy.loginfo("Retrying due to goal being aborted...")

    rospy.logerr("Failed to reach the goal after retrying.")
    return None

if __name__ == '__main__':
    try:
        rospy.init_node('movebase_client_py')

        target_class = input(f"Enter the target class from {object_classes}: ").strip()

        if target_class not in object_classes:
            print(f"Invalid class. Please choose from {object_classes}.")
        else:
            pose = get_first_occurrence_pose(data, target_class)
            if pose:
                x, y, z = pose
                rospy.loginfo(f"Navigating to {target_class} at pose {pose}.")
                result = movebase_client(x, y)
                if result:
                    rospy.loginfo("Goal execution done!")
            else:
                rospy.loginfo(f"No entries found for the class '{target_class}'.")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
