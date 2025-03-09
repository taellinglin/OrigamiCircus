# player_animation.py
from direct.actor.Actor import Actor

def play_animation(actor: Actor, anim_name: str = None, override: bool = False):
    if anim_name is None:
        return
    # Prevent restarting the same animation unless override is True
    if actor.getCurrentAnim() == anim_name and not override:
        return
    actor.stop()
    actor.loop(anim_name)
    if override:
        print(f"Animation overridden: {anim_name}")
    else:
        print(f"Animation playing: {anim_name}")
def tween_to_idle_or_move(player):
    # Only update movement animations if the witch is on the ground and not jumping.
    if not player.is_on_ground or player.is_jumping:
        return
    if player.is_running:
        play_animation(player.actor, "witch_run")
    elif player.is_walking:
        play_animation(player.actor, "witch_walk")
    else:
        play_animation(player.actor, "witch_idle")



def update_animation(player):
    # (Not used directly if we handle updates in the jump task.)
    velocity = player.actor_rb.node().getLinearVelocity()
    
    if player.is_jumping:
        if velocity.z > 0.5:
            play_animation(player.actor, "witch_jump_start", override=True)
        elif velocity.z < -0.5:
            play_animation(player.actor, "witch_jump_land", override=True)
        return
    if player.is_on_ground:
        tween_to_idle_or_move(player)
