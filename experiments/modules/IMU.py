import matplotlib.pyplot as plt
import carla
import csv
import os

class IMU:
    label: str
    transform: carla.Transform
    sensor: carla.Actor
    data: dict
    time: float
    tick_time: float
    syncronous_mode: bool

    def __init__(self, label, world, x, y, z, pitch, yaw, roll, tick_time, attached_ob=None, syncronous_mode=True):
        blueprint = world.get_blueprint_library().find('sensor.other.imu')
        if syncronous_mode:
            blueprint.set_attribute('sensor_tick', str(tick_time))
        self.transform = carla.Transform(carla.Location(x=x, y=y, z=z), carla.Rotation(pitch=pitch, yaw=yaw, roll=roll))
        self.sensor = world.spawn_actor(blueprint, self.transform, attach_to=attached_ob)
        self.tick_time = tick_time
        self.label = label
        self.data = {}
        self.time = 0.0
        self.syncronous_mode = syncronous_mode

    def callback(self, data):
        self.data[self.time] = {
            'gyro': data.gyroscope,
            'accel': data.accelerometer - carla.Vector3D(x=0,y=0,z=9.81),
            'compass': data.compass
        }
        
        self.time += data.timestamp - self.time

    def start(self, experiment_dir):
        if not os.path.exists(f'{experiment_dir}/IMU_{self.label}'):
            os.makedirs(f'{experiment_dir}/IMU_{self.label}')                

        if self.sensor is not None:
            self.sensor.listen(lambda event: self.callback(event))

    def stop(self):
        if self.sensor is not None:
            self.sensor.stop()

    def save_data(self, experiment_dir):
        file_path = f'{experiment_dir}/IMU_{self.label}/data.csv'
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Time', 'Accel_x', 'Accel_y', 'Accel_z', 'Gyro_x', 'Gyro_y', 'Gyro_z', 'Compass'])
            cont = 0
            for time, data in self.data.items():
                if cont < 2:
                    cont += 1
                    continue
                writer.writerow([time, data['accel'].x, data['accel'].y, data['accel'].z,
                                 data['gyro'].x, data['gyro'].y, data['gyro'].z,
                                 data['compass']])

        
    def plot_data(self, experiment_dir: str):
        
        time = []
        accel_x = []
        accel_y = []
        accel_z = []
        gyro_x = []
        gyro_y = []
        gyro_z = []
        compass = []

        filename = f'{experiment_dir}/IMU_{self.label}/data.csv'
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                time.append(float(row['Time']))
                accel_x.append(float(row['Accel_x']))
                accel_y.append(float(row['Accel_y']))
                accel_z.append(float(row['Accel_z']))
                gyro_x.append(float(row['Gyro_x']))
                gyro_y.append(float(row['Gyro_y']))
                gyro_z.append(float(row['Gyro_z']))
                compass.append(float(row['Compass']))

        # plot acceleration data (all axes in one plot)
        plt.figure(figsize=(15, 7))
        plt.plot(time, accel_x, label='Accel X', color='red')
        plt.plot(time, accel_y, label='Accel Y', color='green')
        plt.plot(time, accel_z, label='Accel Z', color='blue')
        plt.xlabel('Time (s)', fontsize=18)
        plt.ylabel('Acceleration (m/s²)', fontsize=18)
        plt.legend(fontsize=16)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.tight_layout()
        plt.savefig(f'{experiment_dir}/IMU_{self.label}/accel.png')

        # plot gyroscope data (all axes in one plot)
        plt.figure(figsize=(15, 7))
        plt.plot(time, gyro_x, label='Gyro X', color='red')
        plt.plot(time, gyro_y, label='Gyro Y', color='green')
        plt.plot(time, gyro_z, label='Gyro Z', color='blue')
        plt.xlabel('Time (s)', fontsize=18)
        plt.ylabel('Angular Velocity (rad/s)', fontsize=18)
        plt.legend(fontsize=16)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.tight_layout()
        plt.savefig(f'{experiment_dir}/IMU_{self.label}/gyro.png')

        # plot compass data
        plt.figure(figsize=(15, 7))
        plt.plot(time, compass, label='Compass', color='purple')
        plt.xlabel('Time (s)', fontsize=18)
        plt.ylabel('Compass (degrees)', fontsize=18)
        plt.legend(fontsize=16)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.tight_layout()
        plt.savefig(f'{experiment_dir}/IMU_{self.label}/compass.png')

    
    def destroy(self):
        if self.sensor is not None:
            self.sensor.destroy()
            self.sensor = None
        else:
            print("Sensor já destruído ou não inicializado.")
