from panda3d.core import CardMaker, NodePath, BitMask32

class MotionBlur:
    def __init__(self, render, player, floor):
        # Store references for potential further use
        self.player = player
        self.floor = floor

        # Disable clearing the color buffer for accumulation effect
        base.win.set_clear_color_active(False)

        # Create a full-screen quad for the motion blur effect
        cardmaker = CardMaker("motion_blur_quad")
        cardmaker.set_frame_fullscreen_quad()

        # Create the quad and parent it to render2d for screen-space effects
        self.motion_quad = NodePath(cardmaker.generate())
        self.motion_quad.reparent_to(render)

        # Initially, no blur (fully transparent)
        self.motion_quad.set_color(0, 0, 0, 0.0)
        self.motion_quad.set_transparency(True)

        # Adjust the bin so it renders in the proper order (after the floor but before the character)
        self.motion_quad.set_bin("fixed", 1)
        self.motion_quad.set_depth_test(False)
        self.motion_quad.set_depth_write(False)
        self.motion_quad.set_transparency(True)

        # Control visibility for specific cameras
        self.floor.hide(BitMask32.bit(2))  # Hide from character camera
        self.floor.show(BitMask32.bit(1))  # Show in floor camera
        
        self.player.hide(BitMask32.bit(1))  # Hide from floor camera
        self.player.show(BitMask32.bit(2))  # Show in character camera

    def enable_blur(self):
        # Increase opacity to accumulate previous frames (creating the blur effect)
        self.motion_quad.set_color(0, 0, 0, 0.5)
        self.motion_quad.set_bin("fixed", 1)

    def disable_blur(self):
        # Reset opacity to disable the motion blur effect
        self.motion_quad.set_color(0, 0, 0, 0.0)

    def cleanup(self):
        if self.motion_quad is None or self.motion_quad.is_empty():
            return
        self.motion_quad.removeNode()
        self.motion_quad = None