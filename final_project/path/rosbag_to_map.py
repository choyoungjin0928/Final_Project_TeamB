import rosbag
import pickle
import tf

from geometry_msgs.msg import PoseStamped

if __name__ == '__main__':
    bag = rosbag.Bag("/home/nvidia/xycar_ws/src/xycar_slam/src/slam.bag")
    path = {'x': [], 'y': [], 'yaw': []}
    for topic, msg, t in bag.read_messages(topics=['/tracked_pose']):
        path['x'].append(msg.pose.position.x)
        path['y'].append(msg.pose.position.y)
        orientation_q = msg.pose.orientation
        _, _, yaw = tf.transformations.euler_from_quaternion([
            orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w
        ])
        path['yaw'].append(yaw)

    with open("reference_path_slam.pkl", "wb") as f:
        pickle.dump(path, f)
