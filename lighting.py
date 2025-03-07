# lighting.py
from panda3d.core import DirectionalLight, AmbientLight

class Lighting:
    def __init__(self, render):
        self.render = render
        self.setup_lights()

    def setup_lights(self):
        # Setup directional light
        dlight = DirectionalLight('dlight')
        dlight.set_color((0.1, 0.1, 0.1, 0.00025))
        dlnp = self.render.attach_new_node(dlight)
        dlnp.set_hpr(0, -60, 0)
        self.render.set_light(dlnp)

        # Setup ambient light
        alight = AmbientLight('alight')
        alight.set_color((0.2, 0.2, 0.2, 0.0000025))
        alnp = self.render.attach_new_node(alight)
        self.render.set_light(alnp)
