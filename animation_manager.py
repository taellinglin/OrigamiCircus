class AnimationManager:
    def __init__(self):
        self.current_animation = None
        self.animation_priorities = {
            "witch_jump_start": 3,
            "witch_jump_land": 3,
            "witch_fall": 2,
            "witch_run": 1,
            "witch_walk": 1,
            "witch_idle": 0
        }
        self.is_in_air = False  # Track whether the player is in the air (jumping or falling)

    def play_animation(self, player, anim_name: str, override: bool = False):
        if anim_name is None:
            return

        # Prevent playing the same animation repeatedly unless override is True
        if self.current_animation == anim_name and not override:
            return

        # Get current and new animation priorities
        current_priority = self.animation_priorities.get(self.current_animation, -1)
        new_priority = self.animation_priorities.get(anim_name, -1)

        # If the player is in the air, only jump animations or fall animations should play
        if self.is_in_air:
            if anim_name not in ["witch_jump_start", "witch_jump_land", "witch_fall"]:
                return  # Ignore any non-jump/fall animations when in air

        # Only play if the new animation has a higher or equal priority
        if override or new_priority >= current_priority:
            # If the animation is not looping, stop it before playing the new one
            if anim_name not in ["witch_run", "witch_walk", "witch_idle"]:
                player.actor.stop()  # Stop current animation if it's not a looping animation
            
            # Play new animation
            if anim_name in ["witch_run", "witch_walk", "witch_idle"]:
                player.actor.loop(anim_name)  # Looping animations
            else:
                player.actor.play(anim_name)  # Non-looping animations
            self.current_animation = anim_name
            print(f"Animation playing: {anim_name} (Override: {override})")

    def adjust_animation_speed(self, player, speed_factor: float):
        """ Adjust the speed of the currently playing animation. """
        if self.current_animation is not None:
            player.actor.set_play_rate(speed_factor, self.current_animation)
            print(f"Animation speed set to {speed_factor} for {self.current_animation}")

    def set_air_state(self, is_in_air: bool):
        """ Set whether the player is in the air or on the ground. """
        self.is_in_air = is_in_air
        print(f"Player is {'in the air' if is_in_air else 'on the ground'}")
