from panda3d.core import Vec3, BitMask32
from panda3d.bullet import BulletRigidBodyNode, BulletCapsuleShape, ZUp
from direct.task import Task

def setup_actor_physics(player):
    shape = BulletCapsuleShape(0.5, 0.5, ZUp)
    body_node = BulletRigidBodyNode('Actor')
    body_node.setMass(320.0)
    body_node.addShape(shape)
    body_node.setIntoCollideMask(BitMask32.bit(1))
    player.actor_rb = player.render.attach_new_node(body_node)
    player.actor.reparentTo(player.actor_rb)
    player.actor.set_bin("fixed", 2)
    player.bullet_world.attachRigidBody(body_node)
    player.actor_rb.set_pos(0, 0, 1)

def jump(player):
    # Only allow jump if the witch is on the ground.
    if player.actor_rb.get_pos().z > 1.0 or not player.is_on_ground:
        print("Not on the ground, cannot jump")
        return

    jump_impulse_delay = 0.3  # seconds before applying additional impulse
    jump_impulse = Vec3(0, 0, 10)  # initial jump impulse

    player.actor_rb.getNode(0).set_linear_velocity(Vec3(0, 0, 0))
    player.actor_rb.getNode(0).apply_central_impulse(jump_impulse)
    print(f"Jump initiated: Applied impulse {jump_impulse}")

    from player_animation import play_animation
    play_animation(player.actor, "witch_jump_start", override=True)

    # Set jump flags
    player.is_jumping = True
    player.is_talking = True
    player.is_on_ground = False

    # Schedule the jump animation check and the strong impulse.
    taskMgr.add(lambda task: check_jump_animation(player, task), "check_jump_animation")
    taskMgr.doMethodLater(jump_impulse_delay, lambda task: apply_jump_impulse(player, task), "jump_impulse_task")

def check_jump_animation(player, task):
    pos_z = player.actor_rb.get_pos().z
    velocity_z = player.actor_rb.getNode(0).get_linear_velocity().z
    print(f"check_jump_animation: pos_z={pos_z}, velocity_z={velocity_z}")

    from player_animation import play_animation

    # If ascending, keep playing the jump start animation.
    if velocity_z > 0.5:
        if player.current_animation != "witch_jump_start":
            play_animation(player.actor, "witch_jump_start", override=True)
    # If descending, trigger the landing animation once.
    elif velocity_z < -0.5:
        if not player.is_landing:
            play_animation(player.actor, "witch_jump_land", override=True)
            player.is_landing = True

    # Landing condition: adjust the threshold if needed.
    if pos_z <= 1.0 and abs(velocity_z) < 0.1:
        print("Landing detected")
        player.is_jumping = False
        player.is_falling = False
        player.is_landing = False
        from player_animation import tween_to_idle_or_move
        tween_to_idle_or_move(player)
        return Task.done

    return Task.cont

def apply_jump_impulse(player, task):
    # Only apply the strong jump impulse if the witch is still on the ground (should be rare due to the jump logic).
    if player.actor_rb.get_pos().z <= 1.0 and not player.is_jumping:
        player.is_jumping = True
        player.is_on_ground = False
        from player_animation import play_animation
        play_animation(player.actor, "witch_jump_start", override=True)
        taskMgr.doMethodLater(0.2, lambda task: execute_jump(player, task), "execute_jump")
    return Task.done

def execute_jump(player, task):
    player.actor_rb.node().applyCentralImpulse(Vec3(0, 0, 5000))
    print("execute_jump: Applied strong jump impulse")
    return Task.done

def check_landing(player, task):
    pos_z = player.actor_rb.get_pos().z
    velocity_z = player.actor_rb.node().get_linear_velocity().z
    print(f"check_landing: pos_z={pos_z}, velocity_z={velocity_z}")

    from player_animation import tween_to_idle_or_move

    if velocity_z < -0.5 and not player.is_landing:
        from player_animation import play_animation
        play_animation(player.actor, "witch_jump_land", override=True)
        player.is_landing = True

    if pos_z <= 1.0 and abs(velocity_z) < 0.1:
        player.is_jumping = False
        player.is_falling = False
        player.is_landing = False
        player.is_on_ground = True
        tween_to_idle_or_move(player)
        return Task.done

    return Task.cont
