from dataclasses import dataclass
import carla
import os

@dataclass
class Camera:
    label: str
    transform: carla.Transform
    sensor: carla.Actor

    def __init__(self, label, world, x, y, z, rotation, vehicle=None):
        blueprint = world.get_blueprint_library().find('sensor.camera.rgb')
        self.transform = carla.Transform(carla.Location(x=x, y=y, z=z), carla.Rotation(pitch=rotation))
        self.sensor = world.spawn_actor(blueprint, self.transform, attach_to=vehicle)
        self.label = label

    # Callback para salvar imagens
    def __save_image_disk__(self, image, output_dir):
        image.save_to_disk(f"{output_dir}/image_{image.frame}.png")
        print(f"Imagem salva: image_{image.frame}.png")

    def start(self, experiment_dir):

        if not os.path.exists(f'{experiment_dir}/camera_{self.label}'):
            os.makedirs(f'{experiment_dir}/camera_{self.label}')                

        if self.sensor is not None:
            output_dir = f'{experiment_dir}/camera_{self.label}'
            self.sensor.listen(lambda image: self.__save_image_disk__(image, output_dir))

    def stop(self):
        if self.sensor is not None:
            self.sensor.stop()
            
    def destroy(self):
        if self.sensor is not None:
            self.sensor.destroy()
            self.sensor = None
        else:
            print("Sensor já destruído ou não inicializado.")
