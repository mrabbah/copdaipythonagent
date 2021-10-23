# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import sys
import time
import zmq

class MinimalSubscriber(Node):

    def __init__(self, name):
        super().__init__(name)
        self.name = name
        root_folder = "/tmp/"
        proto = "ipc://"
        topic_folder = "cdp"
        tracing_topic = "%s%s%s/%s" % (proto, root_folder, topic_folder, "trace")
        context = zmq.Context()
        self.tracing_socket = context.socket(zmq.DEALER)
        self.tracing_socket.connect(tracing_topic)
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        time_nanosec = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
        trace_msg = "%s,%s,%d\n" % (self.name, msg.data, time_nanosec)
        self.tracing_socket.send_string(trace_msg)
        # self.get_logger().info('%s heared: "%s"' % (self.name, msg.data))


def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber(sys.argv[1])

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
