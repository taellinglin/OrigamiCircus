# controls.py
from gamepadInput import GamepadInput
from panda3d.core import InputDevice
class Controls:
    def __init__(self, player):
        self.player = player
        self.gamepad_input = GamepadInput()

        # Set up event listeners for gamepad inputs:
        # Listen for the face A button press.
        base.accept("gamepad-face_a", self.on_gamepad_button)
        
        # Listen for analog stick movements.
        # Here we assume "gamepad-left_x" and "gamepad-left_y" events are fired when the left stick moves.
        base.accept("gamepad-left_x", self.handle_left_x)
        base.accept("gamepad-left_y", self.handle_left_y)

    def handle_left_x(self, device, value):
        """
        Called when the left analog stick's X axis moves.
        We map this to axis 0.
        """
        # Pass the x-axis value to the player (axis 0)
        self.player.on_gamepad_move(0, value)

    def handle_left_y(self, device, value):
        """
        Called when the left analog stick's Y axis moves.
        We map this to axis 1.
        """
        self.player.on_gamepad_move(1, value)

    def on_gamepad_button(self, device=None):
        """
        Called when the face A button is pressed.
        """
        self.player.play_animation('witch_talk', 300)

    def update(self, task):
        """
        Update function to be called every frame.
        In addition to the event-based input, we poll the gamepad's axis values directly.
        """
        # Check if a gamepad is connected
        if self.gamepad_input.gamepad is not None:
            # Poll the left analog stick axes; adjust axis indices if needed
            left_x = self.gamepad_input.gamepad.findAxis(InputDevice.Axis.left_x)
            left_y = self.gamepad_input.gamepad.findAxis(InputDevice.Axis.left_y)
            self.player.on_gamepad_move(0, left_x.value)
            self.player.on_gamepad_move(1, left_y.value)
        return task.cont
