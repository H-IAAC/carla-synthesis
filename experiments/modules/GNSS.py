import matplotlib.pyplot as plt
import carla
import csv
import os

class GNSS:
    label: str
    transform: carla.Transform
    sensor: carla.Actor
    data: dict
    time: float
    tick_time: float

    def __init__(self, label, world, x, y, z, pitch, yaw, roll, tick_time, attached_ob=None):
        blueprint = world.get_blueprint_library().find('sensor.other.gnss')
        blueprint.set_attribute('sensor_tick', str(tick_time))
        self.transform = carla.Transform(carla.Location(x=x, y=y, z=z), carla.Rotation(pitch=pitch, yaw=yaw, roll=roll))
        self.sensor = world.spawn_actor(blueprint, self.transform, attach_to=attached_ob)
        self.tick_time = tick_time
        self.label = label
        self.data = {}
        self.time = 0.0

    def callback(self, data):
        self.data[self.time] = {
            'latitude': data.latitude,
            'longitude': data.longitude,
            'altitude': data.altitude
        }
        self.time += self.tick_time

    def start(self, experiment_dir):
        if not os.path.exists(f'{experiment_dir}/GNSS_{self.label}'):
            os.makedirs(f'{experiment_dir}/GNSS_{self.label}')                

        if self.sensor is not None:
            self.sensor.listen(lambda event: self.callback(event))

    def stop(self):
        if self.sensor is not None:
            self.sensor.stop()

    def save_data(self, experiment_dir):
        file_path = f'{experiment_dir}/GNSS_{self.label}/data.csv'
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Time', 'Latitude', 'Longitude', 'Altitude'])
            cont = 0
            for time, data in self.data.items():
                if cont < 2:
                    cont += 1
                    continue
                writer.writerow([time, data['latitude'], data['longitude'], data['altitude']])

    def plot_data(self, experiment_dir):
        latitudes = [data['latitude'] for data in self.data.values()]
        longitudes = [data['longitude'] for data in self.data.values()]
        altitudes = [data['altitude'] for data in self.data.values()]

        plt.figure(figsize=(10, 6))
        plt.subplot(3, 1, 1)
        plt.plot(self.data.keys(), latitudes, label='Latitude')
        plt.title('GNSS Data')
        plt.ylabel('Latitude (°)')
        plt.grid()

        plt.subplot(3, 1, 2)
        plt.plot(self.data.keys(), longitudes, label='Longitude', color='orange')
        plt.ylabel('Longitude (°)')
        plt.grid()

        plt.subplot(3, 1, 3)
        plt.plot(self.data.keys(), altitudes, label='Altitude', color='green')
        plt.xlabel('Time (s)')
        plt.ylabel('Altitude (m)')
        plt.grid()

        plt.tight_layout()
        plt.savefig(f'{experiment_dir}/GNSS_{self.label}/plot.png')
        plt.close()

    def destroy(self):
        if self.sensor is not None:
            self.sensor.destroy()
            self.sensor = None
        else:
            print("Sensor já destruído ou não inicializado.")