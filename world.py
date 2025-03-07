# world.py
import os
import random
from panda3d.core import GeomVertexFormat, GeomVertexData, Geom, GeomNode, GeomTriangles, GeomVertexWriter
from panda3d.bullet import BulletWorld, BulletPlaneShape, BulletRigidBodyNode
from panda3d.core import Vec3

class World:
    def __init__(self, render, bullet_world):
        self.render = render
        self.bullet_world = bullet_world
        self.ground_np = None
        self.setup_world()

    def setup_world(self):
        # Setup Bullet physics world
        self.bullet_world.setGravity(Vec3(0, 0, -9.81))

        # Procedurally generate the ground mesh and setup floor collision
        self.create_ground()

    def create_ground(self):
        # Create a Bullet collision shape for the ground (a plane)
        shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        floor_node = BulletRigidBodyNode('Floor')
        floor_node.setMass(0)  # Static
        floor_node.addShape(shape)
        self.floor_np = self.render.attach_new_node(floor_node)
        self.floor_np.set_pos(0, 0, -1)
        self.bullet_world.attachRigidBody(floor_node)

        # Procedurally generate ground mesh
        self.generate_ground_mesh()

    def generate_ground_mesh(self):
        grid_size = 20
        num_divisions = 100
        start = -1000.0
        end = 1000.0
        step = (end - start) / num_divisions

        format = GeomVertexFormat.get_v3t2()
        vdata = GeomVertexData("ground", format, Geom.UHStatic)
        vertex = GeomVertexWriter(vdata, "vertex")
        texcoord = GeomVertexWriter(vdata, "texcoord")

        # Generate vertices and texture coordinates
        for i in range(num_divisions + 1):
            for j in range(num_divisions + 1):
                x = start + j * step
                y = start + i * step
                vertex.addData3f(x, y, -1)
                u = (x - start) / (end - start) * 256
                v = (y - start) / (end - start) * 256
                texcoord.addData2f(u, v)

        # Generate triangles for the grid
        tris = GeomTriangles(Geom.UHStatic)
        for i in range(num_divisions):
            for j in range(num_divisions):
                vi = i * (num_divisions + 1) + j
                vi_right = vi + 1
                vi_down = vi + (num_divisions + 1)
                vi_down_right = vi_down + 1
                tris.addVertices(vi, vi_right, vi_down_right)
                tris.addVertices(vi, vi_down_right, vi_down)

        geom = Geom(vdata)
        geom.addPrimitive(tris)
        node = GeomNode("ground")
        node.addGeom(geom)
        self.ground_np = self.render.attach_new_node(node)
        # Get all the texture files from the ./checkerboards/ directory
        texture_dir = './checkerboards/'
        texture_files = [f for f in os.listdir(texture_dir) if f.endswith('.png')]

        # Select a random texture file
        random_texture_file = random.choice(texture_files)

        # Load the random texture
        random_texture_path = os.path.join(texture_dir, random_texture_file)
        self.ground_np.set_texture(base.loader.load_texture(random_texture_path))
