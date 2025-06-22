import random
import carla
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.IMU import IMU
from modules.GNSS import GNSS
from modules.PositionModule import PositionModule
from modules.VelocityModule import VelocityModule
from modules.Camera import Camera

from datetime import datetime

N_VEHICLES = 2
SIM_TIME = 30 # Total simulation time in seconds
TICK_TIME = 0.05  # Period (1 / frequency) in seconds

timestamp = datetime.now().strftime('%Y-%m-%d_%Hh-%Mm-%Ss')
experiment_dir = f'data/exp_{timestamp}'

if not os.path.exists(experiment_dir):
    os.makedirs(experiment_dir)

try:
    agentes = []
    imu_data = {}
    gnss_data = {}

    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)

    world = client.load_world('Town01')
    
    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.05
    world.apply_settings(settings)
    
    traffic_manager = client.get_trafficmanager(8001)
    traffic_manager.set_synchronous_mode(True)
    traffic_manager.set_global_distance_to_leading_vehicle(2.0)

    blueprint_library = world.get_blueprint_library()
    vehicle_bp = blueprint_library.filter('vehicle.*')
    spawn_points = world.get_map().get_spawn_points()
    
    vehicle = world.spawn_actor(vehicle_bp.find("vehicle.bmw.grandtourer"), spawn_points[0])
    vehicle.set_autopilot(True, traffic_manager.get_port())

    if vehicle is not None:
        agentes.append(vehicle)
    else:
        raise Exception("Failed to spawn vehicle")
    
    for _ in range(N_VEHICLES - 1): # NPC vehicles
        vehicle_npc = world.try_spawn_actor(random.choice(vehicle_bp), random.choice(spawn_points))
        if vehicle_npc is not None:
            agentes.append(vehicle_npc)
            vehicle_npc.set_autopilot(True, traffic_manager.get_port())

    camera = Camera("vehicle", world, 0, 0, 2, 0, 0, 0, vehicle)
    imu = IMU("vehicle", world, 0, 0, 0, 0, 0, 0, TICK_TIME, vehicle)
    gnss = GNSS("vehicle", world, 0, 0, 0, 0, 0, 0, TICK_TIME, vehicle)
    position = PositionModule("vehicle", vehicle, TICK_TIME)
    velocity = VelocityModule("vehicle", vehicle, TICK_TIME)

    imu.start(experiment_dir)
    gnss.start(experiment_dir)
    camera.start(experiment_dir)
    position.start(experiment_dir)
    velocity.start(experiment_dir)
    
    tempo = 0.0
    times = []
    xs = []
    ys = []
    
    
    while tempo < SIM_TIME:
        world.tick()

        position.tick()
        velocity.tick()        

        print(tempo)
           
        tempo += TICK_TIME
        time.sleep(TICK_TIME)
        
    camera.stop()
    imu.stop()
    gnss.stop()
    
    imu.save_data(experiment_dir)
    gnss.save_data(experiment_dir)
    position.save_data(experiment_dir)
    velocity.save_data(experiment_dir)
    
    imu.plot_data(experiment_dir)
    gnss.plot_data(experiment_dir)
    position.plot_data(experiment_dir)
    velocity.plot_data(experiment_dir)

finally:
    for agent in agentes:
        if agent.is_alive:
            agent.destroy()
    print("All actors destroyed.")
    