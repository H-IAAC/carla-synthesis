import matplotlib.pyplot as plt
import pandas as pd

def create_sensor_blueprint(world):
    blueprint_library = world.get_blueprint_library()
    imu_bp = blueprint_library.find('sensor.other.imu')
    imu_bp.set_attribute('sensor_tick', '0.05')
    return imu_bp

def imu_listener(agent_name, imu_actor, data_storage):
    def callback(imu_data):
        data_storage[agent_name].append({
            'timestamp': imu_data.timestamp,
            'accel_x': imu_data.accelerometer.x,
            'accel_y': imu_data.accelerometer.y,
            'accel_z': imu_data.accelerometer.z - 9.81,
            'gyro_x': imu_data.gyroscope.x,
            'gyro_y': imu_data.gyroscope.y,
            'gyro_z': imu_data.gyroscope.z
        })
    imu_actor.listen(callback)
    
def plot_and_save_imu(agent_name, data, save_dir):
    clean_data = [d for d in data if isinstance(d, dict) and len(d) == 7]

    clean_data = clean_data[5:]

    if not clean_data:
        print(f"[Aviso] Nenhum dado válido restante para {agent_name}.")
        return

    df = pd.DataFrame(clean_data)
    df.to_csv(f"{save_dir}/imu.csv", index=False)

    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(df['timestamp'], df['accel_x'], label='accel_x')
    plt.plot(df['timestamp'], df['accel_y'], label='accel_y')
    plt.plot(df['timestamp'], df['accel_z'], label='accel_z')
    plt.xlabel("Time (s)", fontsize=18)
    plt.ylabel("Acceleration (m/s²)", fontsize=18)
    plt.legend(fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    plt.subplot(2, 1, 2)
    plt.plot(df['timestamp'], df['gyro_x'], label='gyro_x')
    plt.plot(df['timestamp'], df['gyro_y'], label='gyro_y')
    plt.plot(df['timestamp'], df['gyro_z'], label='gyro_z')
    plt.xlabel("Time (s)", fontsize=18)
    plt.ylabel("Angular Velocity (rad/s)", fontsize=18)
    plt.legend(fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    plt.tight_layout()
    plt.savefig(f"{save_dir}/imu_plot.png")
    plt.close()

def create_imu(vehicle, world, imu_transform):
    imu_bp = create_sensor_blueprint(world)
    return world.spawn_actor(imu_bp, imu_transform, attach_to=vehicle)