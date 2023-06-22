import carla
from agents.navigation import basic_agent
client = carla.Client('localhost', 2000)
client.set_timeout(100.0)
world = client.get_world()
# town 04
map = world.get_map()
blueprint_library = world.get_blueprint_library()
start_location = carla.Location(x=20320.0/100, y=-21710.0/100, z=1)
# start_location_transform = carla.Transform(start_location,carla.Rotation(pitch=0,roll=0,yaw=0))
end_location = carla.Location(x=28920.0/100, y=-24650.0/100, z=0)

try:
    # # get the waypoints of the start and end location
    start_waypoint = map.get_waypoint(start_location)
    end_waypoint = map.get_waypoint(end_location)
    # spawn the vehicle at the start waypoint
    vehicle_bp = blueprint_library.find('vehicle.tesla.model3')
    spawn_point = start_waypoint.transform
    spawn_point.location.z += 1.0
    vehicle = world.spawn_actor(vehicle_bp, spawn_point)
    agent = basic_agent.BasicAgent(vehicle)
    agent.ignore_traffic_lights(True)
    agent.set_destination(end_location=end_location,start_location=start_location)
    # Main simulation loop
    while not agent.done():
        # Execute one step of navigation
        control = agent.run_step()
        # Apply control commands to the vehicle
        vehicle.apply_control(control)
finally:
    # destroy the vehicle
    vehicle.destroy()