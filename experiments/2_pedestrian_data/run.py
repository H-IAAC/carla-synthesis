import carla
import random
import time
import os
from time import sleep

from modules.imu import create_imu, imu_listener, plot_and_save_imu
from modules.Camera import Camera
from modules.PositionModule import PositionModule

# CONFIG
NUM_VEHICLES = 3
NUM_PEDESTRIANS = 3
SIMULATION_TIME = 30
SAVE_DIR = "data"

os.makedirs(SAVE_DIR, exist_ok=True)

def spawn_vehicle(world, blueprint_library, traffic_manager):
    vehicles = []
    spawn_points = world.get_map().get_spawn_points()
    for i in range(NUM_VEHICLES):
        vehicle_bp = random.choice(blueprint_library.filter('vehicle.*'))
        vehicle = world.spawn_actor(vehicle_bp, spawn_points[i])
        vehicle.set_autopilot(True, traffic_manager.get_port())
        
        imu = create_imu(vehicle, world, carla.Transform(carla.Location(x=0, z=1)))
        pos = PositionModule(f"vehicle{vehicle.id}", vehicle, 0.05)
        
        vehicles.append((f"vehicle_{vehicle.id}", vehicle, imu, pos))
    return vehicles

def spawn_pedestrians(world, blueprint_library):
    pedestrians = []

    walker_bps = blueprint_library.filter('walker.pedestrian.*')

    batch = []
    for i in range(NUM_PEDESTRIANS):
        
        location = world.get_random_location_from_navigation()
        if location is None:
            continue
        spawn_point_pedestrian = carla.Transform(location)
        
        walker_bp = random.choice(walker_bps)
        walker = world.try_spawn_actor(walker_bp, spawn_point_pedestrian)
        batch.append(walker)
        
        if walker is not None:
            imu = create_imu(walker, world, carla.Transform(carla.Location(z=1)))
            pos = PositionModule(f"pedestrian{walker.id}", walker, 0.05)
            
            controller_bp = blueprint_library.find('controller.ai.walker')
            controller = world.spawn_actor(controller_bp, carla.Transform(), attach_to=walker)
            controller.start()
            controller.go_to_location(world.get_random_location_from_navigation())
            controller.set_max_speed(1 + random.random())
            
            
            pedestrians.append((f"pedestrian_{walker.id}", walker, imu, pos))

    return pedestrians

def main():
    
    random.seed(time.time())
    
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)
    world = client.load_world('Town01')

    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = 0.05
    world.apply_settings(settings)

    traffic_manager = client.get_trafficmanager(8001)

    blueprint_library = world.get_blueprint_library()

    all_agents = []

    vehicles = spawn_vehicle(world, blueprint_library, traffic_manager)
    pedestrians = spawn_pedestrians(world, blueprint_library)
    all_agents.extend(vehicles)
    all_agents.extend(pedestrians)

    imu_data_storage = {}
    for name, actor, imu, pos in all_agents:
        agent_folder = os.path.join(SAVE_DIR, name)
        os.makedirs(agent_folder, exist_ok=True)
        imu_data_storage[name] = []
        imu_listener(name, imu, imu_data_storage)
        pos.start(agent_folder)

    try:
        tempo = 0
        while tempo < SIMULATION_TIME:
            world.tick()
            sleep(0.05)
            print(f"Tempo: {tempo}")
            
            for _, _, _, pos in all_agents:
                pos.tick()
            
            tempo += 0.05
            
            
        for name, _, _, pos in all_agents:
            agent_folder = os.path.join(SAVE_DIR, name)
            os.makedirs(f'{SAVE_DIR}/{name}/imu', exist_ok=True)
            print(f'{SAVE_DIR}/{name}/imu')
            plot_and_save_imu(name, imu_data_storage[name], f'{SAVE_DIR}/{name}/imu')
            pos.save_data(agent_folder)
            pos.plot_data(agent_folder)

    finally:
        print("Encerrando simulação e limpando...")
        for _, actor, imu, _ in all_agents:
            imu.stop()
            imu.destroy()
            actor.destroy()

        settings.synchronous_mode = False
        world.apply_settings(settings)
        print("Pronto.")

if __name__ == '__main__':
    main()
