import carla
import matplotlib.pyplot as plt

def load_xodr_to_carla(client, xodr_path):
    with open(xodr_path, 'r') as f:
        xodr_content = f.read()

    world = client.generate_opendrive_world(xodr_content)
    return world

def plot_road_geometry_and_spawns(world, waypoint_distance=0.5):
    carla_map = world.get_map()
    waypoints = carla_map.generate_waypoints(waypoint_distance)

    lane_x = []
    lane_y = []

    for wp in waypoints:
        lane_x.append(wp.transform.location.x)
        lane_y.append(wp.transform.location.y)

    spawn_points = carla_map.get_spawn_points()
    spawn_x = [sp.location.x for sp in spawn_points]
    spawn_y = [sp.location.y for sp in spawn_points]

    plt.figure(figsize=(10, 10))
    plt.scatter(lane_x, lane_y, s=1, c='black', label='Roads')
    plt.scatter(spawn_x, spawn_y, c='red', marker='o', label='Spawn Points')

    plt.xlabel('X coordinate (m)', fontsize=18)
    plt.ylabel('Y coordinate (m)', fontsize=18)
    plt.axis('equal')
    plt.legend(fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(True)
    plt.savefig("maps/mapa_unicamp.png")
    plt.close()

def main():
    xodr_file_path = "maps/unicamp.xodr"

    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)

    try:
        world = load_xodr_to_carla(client, xodr_file_path)
        plot_road_geometry_and_spawns(world, waypoint_distance=0.5)
    except RuntimeError as e:
        print(f'Erro ao carregar o mapa: {e}')
    except Exception as e:
        print(f'Erro geral: {e}')

if __name__ == '__main__':
    main()
