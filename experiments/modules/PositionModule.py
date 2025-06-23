import matplotlib.pyplot as plt
import carla
import csv
import os

class PositionModule:
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
         if not os.path.exists(f'{experiment_dir}/Position_{self.label}'):
            os.makedirs(f'{experiment_dir}/Position_{self.label}')                

    def tick(self):
        try:
            world = self.attached_ob.get_world()
            sim_time = world.get_snapshot().timestamp.elapsed_seconds
            current_data = self.attached_ob.get_location()
            self.data[sim_time] = {
                'x': current_data.x,
                'y': current_data.y,
                'z': current_data.z
            }
        except Exception as e:
            print(f"Error getting Position data: {e}")

    def save_data(self, experiment_dir):
        file_path = f'{experiment_dir}/Position_{self.label}/data.csv'
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Time', 'X', 'Y', 'Z'])
            for time, data in self.data.items():
                writer.writerow([time, data['x'], data['y'], data['z']])

    def plot_data(self, experiment_dir, midpoint=None):
        time = []
        gps_x = []
        gps_y = []
        gps_z = []
        filename = f'{experiment_dir}/Position_{self.label}/data.csv'
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                time.append(float(row['Time']))
                gps_x.append(float(row['X']))
                gps_y.append(float(row['Y']))
                gps_z.append(float(row['Z']))

        plt.figure(figsize=(15, 8))
        sc = plt.scatter(gps_x, gps_y, c=time, cmap='viridis', s=10, label='Trajectory')
        plt.scatter(gps_x[0], gps_y[0], label='Start', color='cyan', s=100)
        plt.scatter(gps_x[-1], gps_y[-1], label='End', color='magenta', s=100)
        
        if midpoint is not None:
            plt.scatter(midpoint.x, midpoint.y, label='Midpoint', color='red', s=200, marker='X')
        
        plt.xlabel('Position X (m)', fontsize=18)
        plt.ylabel('Position Y (m)', fontsize=18)
        plt.legend(fontsize=16)
        plt.tick_params(axis='both', labelsize=16)
        cbar = plt.colorbar(sc)
        cbar.set_label('Time (s)', fontsize=18)
        cbar.ax.tick_params(labelsize=16)
        plt.tight_layout()
        plt.savefig(f'{experiment_dir}/Position_{self.label}/Position.png')