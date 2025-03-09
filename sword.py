from panda3d.core import BitMask32, TransformState, Vec3
from panda3d.bullet import BulletRigidBodyNode, BulletConvexHullShape
from direct.actor.Actor import Actor

class Sword:
    def __init__(self, physics_world):
        self.physics_world = physics_world  # Reference to Bullet world

        # Load the sword model
        self.model = loader.loadModel("sword.bam")
        print("[DEBUG] Sword model loaded.")

        # Create a Bullet convex hull shape from the sword's geometry
        self.shape = BulletConvexHullShape()
        geom_nodes = self.model.findAllMatches('**/+GeomNode')
        for node_path in geom_nodes:
            geom_node = node_path.node()
            for i in range(geom_node.getNumGeoms()):
                geom = geom_node.getGeom(i)
                self.shape.addGeom(geom)
        print("[DEBUG] BulletConvexHullShape created.")

        # Create a Bullet rigid body node
        self.body = BulletRigidBodyNode('Sword')
        self.body.addShape(self.shape)
        self.body.setKinematic(True)  # Kinematic so we move it manually
        self.body_np = render.attachNewNode(self.body)  # Keep in render!

        # Attach the visual model to this node (NOT the Bullet node)
        self.model.reparentTo(self.body_np)
        self.body_np.node().setIntoCollideMask(BitMask32.bit(0))


        # Add physics body to the Bullet world
        self.physics_world.attachRigidBody(self.body)
        print("[DEBUG] Sword added to scene and physics.")
        taskMgr.add(self.update_physics_position, "update_sword_position")

    def equip(self, player, joint_name="CC_Base_R_Hand"):
        """
        Attach the sword visually and physically to the player's hand.
        """
        # Expose the actual joint for attaching the weapon
        joint_mount = player.actor.exposeJoint(None, "modelRoot", joint_name)

        if joint_mount:
            # Attach the entire physics node (body + model) to the joint
            self.body_np.reparentTo(joint_mount)
            print(f"[DEBUG] Sword model + physics attached to '{joint_name}'.")

            # Reset position, rotation, and scale
            self.body_np.setPos(0, 0, 0)
            self.body_np.setHpr(0, 0, 0)  # Ensure correct rotation when attached
            self.body_np.setScale(1)  # Reset scale to avoid inheritance of scale issues

            # Adjust sword orientation if needed (e.g., for correct alignment in the hand)
            # Example: Rotate 90 degrees on Z-axis to properly orient the sword

            # Set the sword to collide only with certain layers or objects
            self.body_np.node().setIntoCollideMask(BitMask32.bit(0))  # Adjust for proper mask

            # Optionally, ensure that the player’s hand has a different mask to avoid unwanted collisions
            player.actor.node().setIntoCollideMask(BitMask32.bit(1))  # Example mask for player hands

            # Update Bullet physics manually (since it's kinematic)
            taskMgr.add(self.update_physics_position, "update_sword_physics")
        else:
            print(f"[ERROR] Joint '{joint_name}' not found.")

    def unequip(self):
        """Detach the sword from the player and reset to physics world."""
        self.body_np.reparentTo(render)  # Move back to world space
        print("[DEBUG] Sword unequipped.")

    def update_physics_position(self, task):
        """Manually sync the Bullet body with the joint's world position."""
        if self.body_np.getParent() is not None:
            # Get the current transform (position and rotation) of the sword
            transform = self.body_np.getNetTransform()

            # Set angular velocity to zero to prevent spinning
            self.body.setLinearVelocity(Vec3(0, 0, 0))
            self.body.setAngularVelocity(Vec3(0, 0, 0))

            # Update position and rotation based on parent's transform (player's hand)
            self.body_np.setPos(self.body_np.getParent().getPos(render))  # Sync position
            self.body_np.setHpr(self.body_np.getParent().getHpr(render))  # Sync rotation

            # Ensure the sword stays in sync with the parent's scale (if necessary)
            self.body_np.setScale(self.body_np.getParent().getScale())  # Adjust scale if needed

            # Update Bullet physics body with the transform
            self.body.setTransform(self.body_np.getTransform())
            self.body_np.setPos(0, 0, 0)
            self.body_np.setHpr(0, 0, 0)
            # Print debug information to verify the sword's position and rota

        return task.cont
