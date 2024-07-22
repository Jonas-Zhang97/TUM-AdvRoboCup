#include <pick_place/pick.h>

int main(int argc, char** argv)
{
  ros::init(argc, argv, "pick_node");

  Pick pick();
  ros::spin();

  return 0;
}