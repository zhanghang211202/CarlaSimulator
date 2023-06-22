import carla
import PIL.Image as Image
import time
import numpy as np

loc_list=[]
z_list = []


# town04_loc_list = [carla.Location(x= 40720/100, y=-22675/100, z=0/100),
#                    carla.Location(x= -15380.0/100, y=3020/100, z=710/100),
#                    carla.Location(x= -905/100, y=8000/100, z=0/100),
#                    carla.Location(x= -37190/100, y=1200/100, z=0/100),
#                    carla.Location(x= 7170/100, y=3325/100, z=1100/100)]

town04_loc_list = [
                    carla.Location(x= 30600.0/100, y=-16900.0/100, z=0/100),
                    carla.Location(x= -1230.0/100, y=5760.0/100, z=0/100),
                    carla.Location(x= 40720/100, y=-22675/100, z=0/100),
                    carla.Location(x= -37190/100, y=1200/100, z=0/100),
                    carla.Location(x= 19880.0/100, y=-17050.0/100, z=0/100),
                   ]

town05_loc_list = [
                    carla.Location(x= 8870.0/100, y=190.0/100, z=0/100),
                    carla.Location(x= -10980.0/100, y=-60.0/100, z=0/100),
                    carla.Location(x= -17450.0/100, y=-9160.0/100, z=0/100),
                    carla.Location(x= 1620.0/100, y=-8780.0/100, z=0/100),
                    carla.Location(x= -19160.0/100, y=10590.0/100, z=0/100),
                   ]

town06_loc_list = [
                   carla.Location(x= 25370.0/100, y=14750.0/100, z=0/100),
                   carla.Location(x= 42510.0/100, y=4540.0/100, z=0/100),
                   carla.Location(x= 26210.0/100, y=-2030.0/100, z=0/100),
                   carla.Location(x= 560/100, y=6550/100, z=0/100),
                   ]

town12_loc_list = [
                   carla.Location(x=237220.0/100, y=614100.0/100, z=36951.0/100),
                   # carla.Location(x= 42510.0/100, y=4540.0/100, z=0/100),
                   # carla.Location(x= 26210.0/100, y=-2030.0/100, z=0/100),
                   # carla.Location(x= 730.0/100, y=16330.0/100, z=0/100),
                   ]

town12_2_1_loc_list = [
                   carla.Location(x=-139568.0/100, y=488860.0/100, z=37612.0/100),
                   # carla.Location(x= 42510.0/100, y=4540.0/100, z=0/100),
                   # carla.Location(x= 26210.0/100, y=-2030.0/100, z=0/100),
                   # carla.Location(x= 730.0/100, y=16330.0/100, z=0/100),
                   ]
town12_3_1_loc_list = [
                   carla.Location(x=105730.0/100, y=430080.0/100, z=36594.0/100),
                   carla.Location(x=46710.0/100, y=472660.0/100, z=37033.0/100),
                   # carla.Location(x= 730.0/100, y=16330.0/100, z=0/100),
                   ]
town12_3_2_loc_list = [
                   carla.Location(x=178170.0/100, y=227990.0/100, z=36626.0/100),
                   # carla.Location(x= 730.0/100, y=16330.0/100, z=0/100),
                   ]
# town04_z_list = [0, 3, 0, 7, 10]
town04_z_list = [0.2, 0.2, 0, 7, 0]
town04_100z_list = [0.2, 0.2, 0, 2, 0.2]
town05_z_list = [0,0,0,0.2,0.2]
town06_z_list = [0,0,0,0]
town12_z_list = [36951.0/100+1]
town12_2_1_z_list = [37612.0/100+1]
town12_3_1_z_list = [36594.0/100,37033.0/100]
town12_3_2_z_list = [36626.0/100-1]
# modify here
loc_list = town12_3_2_loc_list
z_list = town12_3_2_z_list
# 200 or 100
distance_name = 100
# 214.4 or 108
distance = 108
# for 200 3.6 for 100 2
speed = 2
town_name = 'town12'
rgb_image_queue  = []
segmentation_image_queue  = []

def process_rgb_image(image):
    image.convert(carla.ColorConverter.Raw)
    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))
    array = array[:, :, :3]
    array = array[:, :, ::-1]
    temp = np.copy(array)
    img = Image.fromarray(temp, mode="RGB")
    print('before save')
    img_name = 'carla_images_cloudy/images/{}/{}/{:0>8}.png'.format(town_name, distance_name, image.frame)
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
    img_name = 'carla_images_cloudy/labels/{}/{}/{:0>8}.png'.format(town_name, distance_name, img_frame.frame)
    img.save(img_name)

# python script location(x,y,z  m)  location in carlaUE4(cm)

# Connect to the CARLA server and get the world and map
client = carla.Client('localhost', 2000)
client.set_timeout(100.0)
world = client.get_world()
map = world.get_map()
spectator = world.get_spectator()
settings = world.get_settings()
settings.actor_active_distance = 2000
# 定义RGB相机的参数
rgb_bp = world.get_blueprint_library().find('sensor.camera.rgb')
rgb_bp.set_attribute('image_size_x', '3840')
rgb_bp.set_attribute('image_size_y', '2160')
rgb_bp.set_attribute('fov', '40')
# rgb_bp.set_attribute('sensor_tick', '4.0')

# 定义分割相机的参数
seg_bp = world.get_blueprint_library().find('sensor.camera.semantic_segmentation')
seg_bp.set_attribute('image_size_x', '3840')
seg_bp.set_attribute('image_size_y', '2160')
seg_bp.set_attribute('fov', '40')
# seg_bp.set_attribute('sensor_tick', '4.0')

weather = carla.WeatherParameters()
weather.sun_altitude_angle = 90
weather.cloudiness = 50
world.set_weather(weather)

for index, spawn_location in enumerate(loc_list):
    # Specify the location where the car should be spawned
    # spawn_location = carla.Location(x=-22750.0/100, y=-10235.0/100, z=1000.0/100) # tire
    # town 04
    # 40720,-22675,0,0  -15380,3020,710,3  -905,8000,0,0  -37190,1200,0,7  7170,3325,1100,10
    # spawn_location = carla.Location(x= 40720/100, y=-22675/100, z=0/100)
    # spawn_location = carla.Location(x= -15380.0/100, y=3020/100, z=710/100)
    # spawn_location = carla.Location(x= -905/100, y=8000/100, z=0/100)
    # spawn_location = carla.Location(x= -37190/100, y=1200/100, z=0/100)
    # spawn_location = carla.Location(x= 7170/100, y=3325/100, z=1100/100)
    print('new object')
    transforms = carla.Transform(spawn_location,carla.Rotation(pitch=0,roll=0,yaw=0))


    # Get the waypoint closest to the spawn location
    waypoint = map.get_waypoint(spawn_location)
    spectator.set_transform(waypoint.transform)
    blueprint_library = world.get_blueprint_library()
    # Calculate a new location 200 meters behind the waypoint along the road
    # road_direction = spawn_waypoint.transform.rotation.yaw
    # new_location = spawn_waypoint.transform.location - carla.Location(x=200.0 * math.cos(math.radians(road_direction)), y=200.0 * math.sin(math.radians(road_direction)), z=0.0)

    # new_location = waypoint.transform.location - 200 * waypoint.transform.get_forward_vector()
    for i in range(0, 3):
        # new_location = waypoint.transform.location - (100-4*i) * waypoint.transform.get_forward_vector()
        new_location = waypoint.transform.location - (distance-speed*i) * waypoint.transform.get_forward_vector()
        # town 4
        # new_location.z = 0
        # new_location.z = 3
        # new_location.z = 0
        # new_location.z = 7
        new_location.z = z_list[index]
        # Spawn a car at the new location
        car_bp = blueprint_library.filter('vehicle.*')[0]
        car_bp.set_attribute('role_name', 'hero')
        spawn_point = carla.Transform(new_location, waypoint.transform.rotation)
        spectator.set_transform(spawn_point)
        my_car = world.spawn_actor(car_bp, spawn_point)
        time.sleep(2)
        # car_controller = car.get_control()
        # car_controller.throttle = 0.0  # 油门设为 0
        # car_controller.brake = 1.0  # 制动设为 1
        # car_controller.steer = 0.0  # 转向角度设为 0
        # car.apply_control(car_controller)
        rgb_transform = carla.Transform(carla.Location(x=1.6, z=1.3))
        rgb_camera = world.spawn_actor(rgb_bp, rgb_transform, attach_to=my_car)
        # print(rgb_transform)
        seg_transform = carla.Transform(carla.Location(x=1.6, z=1.3))
        seg_camera = world.spawn_actor(seg_bp, seg_transform, attach_to=my_car)
        spectator.set_transform(rgb_camera.get_transform()) # 设置相机视角
        rgb_camera.listen(rgb_image_queue.append)
        seg_camera.listen(segmentation_image_queue.append)
        time.sleep(1)
        world.tick()
        if len(rgb_image_queue) > 0:
            rgb_image = rgb_image_queue[-1]
            rgb_image_queue.clear()
            process_rgb_image(rgb_image)
            # Capture and save the segmentation image
        if len(segmentation_image_queue) > 0:
            segmentation_image = segmentation_image_queue[-1]
            segmentation_image_queue.clear()
            process_seg_image(rgb_image,segmentation_image)
        # time.sleep(4)

        # Register the callback function to the RGB camera
        my_car.destroy()
        rgb_camera.destroy()
        seg_camera.destroy()
