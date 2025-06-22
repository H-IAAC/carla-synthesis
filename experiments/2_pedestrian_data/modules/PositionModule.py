import matplotlib.pyplot as plt
import carla
import csv
import os

class PositionModule:
    label: str
    attached_ob: carla.Actor
    data: dict
    time: float
    tick_time: float

    def __init__(self, label, obj, thick_time):
        
        self.attached_ob = obj
        self.label = label
        self.tick_time = thick_time
        self.data = {}
        self.time = 0.0

    def start(self, experiment_dir):
         if not os.path.exists(f'{experiment_dir}/Position_{self.label}'):
            os.makedirs(f'{experiment_dir}/Position_{self.label}')                

    def tick(self):
        try:
            current_data = self.attached_ob.get_location()
            self.data[self.time] = {
                'x': current_data.x,
                'y': current_data.y,
                'z': current_data.z
            }
            self.time += self.tick_time
        except Exception as e:
            print(f"Error getting Position data: {e}")

    def save_data(self, experiment_dir):
        file_path = f'{experiment_dir}/Position_{self.label}/data.csv'
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Time', 'X', 'Y', 'Z'])
            for time, data in self.data.items():
                writer.writerow([time, data['x'], data['y'], data['z']])

    def plot_data(self, experiment_dir):
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

        fig, axs = plt.subplots(2, 1, figsize=(15, 15))

        axs[0].plot(time, gps_x, label='Position X', color='blue')
        axs[0].plot(time, gps_y, label='Position Y', color='orange')
        axs[0].plot(time, gps_z, label='Position Z', color='green')
        axs[0].set_ylabel('Position Coordinates (m)', fontsize=18)
        axs[0].legend(fontsize=16)
        axs[0].tick_params(axis='both', labelsize=16)

        sc = axs[1].scatter(gps_x, gps_y, c=time, cmap='viridis', s=10, label='Trajectory')
        axs[1].scatter(gps_x[0], gps_y[0], label='Start', color='green', s=100)
        axs[1].scatter(gps_x[-1], gps_y[-1], label='End', color='orange', s=100)
        axs[1].set_xlabel('Position X (m)', fontsize=18)
        axs[1].set_ylabel('Position Y (m)', fontsize=18)
        axs[1].legend(fontsize=16)
        axs[1].tick_params(axis='both', labelsize=16)
        cbar = fig.colorbar(sc, ax=axs[1])
        cbar.set_label('Time (s)', fontsize=18)
        cbar.ax.tick_params(labelsize=16)

        plt.tight_layout()
        plt.savefig(f'{experiment_dir}/Position_{self.label}/Position.png')
