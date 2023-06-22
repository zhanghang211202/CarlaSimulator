import carla
import PIL.Image as Image
import time
import numpy as np
from agents.navigation import basic_agent
import random

town_name = 'town10'
def process_rgb_image(image):
    image.convert(carla.ColorConverter.Raw)
    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))
    array = array[:, :, :3]
    array = array[:, :, ::-1]
    temp = np.copy(array)
    img = Image.fromarray(temp, mode="RGB")
    print('before save')
    img_name = 'carla_images_ft/images/{}/{:0>8}.png'.format(town_name, image.frame)
    img.save(img_name)

def process_seg_image(img_frame,image):
    image.convert(carla.ColorConverter.CityScapesPalette)
    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))
    array = array[:, :, :3]
    array = array[:, :, ::-1]
    temp = np.copy(array)
    img = Image.fromarray(temp, mode="RGB")
    print('before save seg')
    img_name = 'carla_images_ft/labels/{}/{:0>8}.png'.format(town_name, img_frame.frame)
    img.save(img_name)

def get_random_waypoint():
    waypoint = random.choice(map.get_spawn_points())
    return waypoint

# python script location(x,y,z  m)  location in carlaUE4(cm)

# Connect to the CARLA server and get the world and map
client = carla.Client('localhost', 2000)
client.set_timeout(100.0)
world = client.get_world()
# settings = world.get_settings()
# settings.fixed_delta_seconds = 0.01
# world.apply_settings(settings)
map = world.get_map()
spectator = world.get_spectator()
settings = world.get_settings()
# settings.actor_active_distance = 2000
# 定义RGB相机的参数
rgb_bp = world.get_blueprint_library().find('sensor.camera.rgb')
rgb_bp.set_attribute('image_size_x', '3840')
rgb_bp.set_attribute('image_size_y', '2160')
rgb_bp.set_attribute('fov', '40')
rgb_bp.set_attribute('sensor_tick', '3.0')
rgb_bp.set_attribute('motion_blur_intensity', '0.0')

# 定义分割相机的参数
seg_bp = world.get_blueprint_library().find('sensor.camera.semantic_segmentation')
seg_bp.set_attribute('image_size_x', '3840')
seg_bp.set_attribute('image_size_y', '2160')
seg_bp.set_attribute('fov', '40')
seg_bp.set_attribute('sensor_tick', '3.0')

weather = carla.WeatherParameters()
weather.sun_azimuth_angle = 90
weather.sun_altitude_angle = 90
world.set_weather(weather)
car_bp = world.get_blueprint_library().filter('vehicle.*')[0]
car_bp.set_attribute('role_name', 'hero')
spawn_point = map.get_spawn_points()[1]
my_car = world.spawn_actor(car_bp, spawn_point)
time.sleep(1)
rgb_transform = carla.Transform(carla.Location(x=1.6, z=1.3))
rgb_camera = world.spawn_actor(rgb_bp, rgb_transform, attach_to=my_car)
# print(rgb_transform)
seg_transform = carla.Transform(carla.Location(x=1.6, z=1.3))
seg_camera = world.spawn_actor(seg_bp, seg_transform, attach_to=my_car)


rgb_image_queue = []
segmentation_image_queue = []
agent = basic_agent.BasicAgent(my_car)
agent.set_target_speed(60)
agent.ignore_traffic_lights(True)
rgb_camera.listen(rgb_image_queue.append)
seg_camera.listen(segmentation_image_queue.append)
waypoint = get_random_waypoint()
agent.set_destination(waypoint.location)
while(True):
    if len(rgb_image_queue) >= 100 and len(segmentation_image_queue) >= 100:
        break
    spectator.set_transform(rgb_camera.get_transform())
    control = agent.run_step()
    if my_car.get_location().distance(waypoint.location) < 2.0:
        waypoint = get_random_waypoint()
        agent.set_destination(waypoint.location)
    my_car.apply_control(control)
    world.tick()

for i in range(len(rgb_image_queue)):
    process_rgb_image(rgb_image_queue[i])
    process_seg_image(rgb_image_queue[i],segmentation_image_queue[i])
    print('save image {}'.format(i))
    time.sleep(0.01)


my_car.destroy()
rgb_camera.destroy()
seg_camera.destroy()
