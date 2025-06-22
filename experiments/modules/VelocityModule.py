import matplotlib.pyplot as plt
import carla
import csv
import os

class VelocityModule:
    label: str
    attached_ob: carla.Actor
    data: dict
    time: float
    
    def __init__(self, label, obj):
        
        self.attached_ob = obj
        self.label = label
        self.data = {}
        self.time = 0.0

    def start(self, experiment_dir):
        if not os.path.exists(f'{experiment_dir}/Velocity_{self.label}'):
            os.makedirs(f'{experiment_dir}/Velocity_{self.label}')

    def tick(self):
        try:
            world = self.attached_ob.get_world()
            sim_time = world.get_snapshot().timestamp.elapsed_seconds
            current_data = self.attached_ob.get_velocity()
            self.data[sim_time] = {
                'x': current_data.x,
                'y': current_data.y,
                'z': current_data.z
            }
        except Exception as e:
            print(f"Error getting Velocity data: {e}")

    def save_data(self, experiment_dir):
        file_path = f'{experiment_dir}/Velocity_{self.label}/data.csv'
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Time', 'X', 'Y', 'Z'])
            for time, data in self.data.items():
                writer.writerow([time, data['x'], data['y'], data['z']])

    def plot_data(self, experiment_dir):
        times = list(self.data.keys())
        x_values = [self.data[time]['x'] for time in times]
        y_values = [self.data[time]['y'] for time in times]
        z_values = [self.data[time]['z'] for time in times]

        plt.figure(figsize=(10, 6))
        plt.plot(times, x_values, label='X Velocity', color='r')
        plt.plot(times, y_values, label='Y Velocity', color='g')
        plt.plot(times, z_values, label='Z Velocity', color='b')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity (m/s)')
        plt.legend()
        plt.grid(True)

        plt.savefig(f'{experiment_dir}/Velocity_{self.label}/plot.png')
        plt.close()
