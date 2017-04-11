#!/usr/bin/env python
from __future__ import print_function

#import roslib
#roslib.load_manifest('my_package')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class cam_circle:

  def __init__(self):
    self.image_pub = rospy.Publisher("image_topic_out",Image, queue_size=10)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("image_topic_in",Image, self.callback)

  # Callback when a new image arrived
  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    # Draw a circle
    (rows,cols,channels) = cv_image.shape
    center = (cols/2,rows/2)
    thickness = 5
    radius = min(cols/2,rows/2) - thickness
    cv2.circle(cv_image, center, radius, 255, thickness)

    # display
    cv2.imshow("Image with circle", cv_image)
    cv2.waitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError as e:
      print(e)

def main(args):
  ic = cam_circle()
  rospy.init_node('cam_circle', anonymous=True)
  print("OpenCV Version: {}".format(cv2.__version__))
  print("Python Version: {}".format(sys.version))
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)