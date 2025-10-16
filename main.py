import vgamepad as vg
import pygame
import time
import threading
from threading import Lock

# Initialize pygame for input handling
pygame.init()

# Create virtual Xbox 360 gamepad
gamepad = vg.VX360Gamepad()

# Global variables for tracking state
running = True
mouse_sensitivity = 1.5
right_stick_x = 0.0
right_stick_y = 0.0
left_stick_x = 0.0
left_stick_y = 0.0
gamepad_lock = Lock()

# WASD key states
key_states = {
    'w': False,
    'a': False,
    's': False,
    'd': False,
    'space': False
}

def normalize_stick_value(value, deadzone=0.1):
    """Normalize stick values to -1.0 to 1.0 range with deadzone"""
    if abs(value) < deadzone:
        return 0.0
    return max(-1.0, min(1.0, value))

def update_gamepad():
    """Update the virtual gamepad state"""
    global left_stick_x, left_stick_y, right_stick_x, right_stick_y
    
    with gamepad_lock:
        # Update left stick (WASD)
        gamepad.left_joystick_float(
            x_value_float=normalize_stick_value(left_stick_x),
            y_value_float=normalize_stick_value(-left_stick_y)  # Invert Y for correct direction
        )
        
        # Update right stick (mouse)
        gamepad.right_joystick_float(
            x_value_float=normalize_stick_value(right_stick_x),
            y_value_float=normalize_stick_value(-right_stick_y)  # Invert Y for correct direction
        )
        
        # Update gamepad
        gamepad.update()

def handle_keyboard_input():
    """Handle keyboard input for WASD and spacebar"""
    global left_stick_x, left_stick_y, key_states, running
    
    # Create a small window for capturing input
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Xbox Controller Emulator - WASD: Left Stick, Mouse: Right Stick, LMB: X, Space: Y")
    clock = pygame.time.Clock()
    
    # Center mouse for relative movement
    pygame.mouse.set_pos(200, 150)
    pygame.event.set_grab(True)
    
    print("Xbox 360 Controller Emulator Started!")
    print("Controls:")
    print("- WASD: Left stick")
    print("- Mouse movement: Right stick")
    print("- Left mouse button: X button")
    print("- Spacebar: Y button")
    print("- ESC: Exit")
    print("\nWindow must be focused for input capture!")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
                elif event.key == pygame.K_w:
                    key_states['w'] = True
                elif event.key == pygame.K_a:
                    key_states['a'] = True
                elif event.key == pygame.K_s:
                    key_states['s'] = True
                elif event.key == pygame.K_d:
                    key_states['d'] = True
                elif event.key == pygame.K_SPACE:
                    key_states['space'] = True
                    with gamepad_lock:
                        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
                        gamepad.update()
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    key_states['w'] = False
                elif event.key == pygame.K_a:
                    key_states['a'] = False
                elif event.key == pygame.K_s:
                    key_states['s'] = False
                elif event.key == pygame.K_d:
                    key_states['d'] = False
                elif event.key == pygame.K_SPACE:
                    key_states['space'] = False
                    with gamepad_lock:
                        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
                        gamepad.update()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    with gamepad_lock:
                        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
                        gamepad.update()
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    with gamepad_lock:
                        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
                        gamepad.update()
            
            elif event.type == pygame.MOUSEMOTION:
                # Handle mouse movement for right stick
                rel_x, rel_y = event.rel
                global right_stick_x, right_stick_y
                
                # Apply sensitivity and accumulate movement
                right_stick_x += rel_x * mouse_sensitivity * 0.01
                right_stick_y += rel_y * mouse_sensitivity * 0.01
                
                # Clamp values
                right_stick_x = max(-1.0, min(1.0, right_stick_x))
                right_stick_y = max(-1.0, min(1.0, right_stick_y))
        
        # Update left stick based on WASD
        left_stick_x = 0.0
        left_stick_y = 0.0
        
        if key_states['a']:
            left_stick_x -= 1.0
        if key_states['d']:
            left_stick_x += 1.0
        if key_states['w']:
            left_stick_y += 1.0
        if key_states['s']:
            left_stick_y -= 1.0
        
        # Apply mouse movement decay for right stick (so it returns to center)
        right_stick_x *= 0.95
        right_stick_y *= 0.95
        
        # Update the gamepad
        update_gamepad()
        
        # Draw simple status on screen
        screen.fill((30, 30, 30))
        font = pygame.font.Font(None, 24)
        
        # Status text
        status_text = [
            f"Left Stick (WASD): ({left_stick_x:.2f}, {left_stick_y:.2f})",
            f"Right Stick (Mouse): ({right_stick_x:.2f}, {right_stick_y:.2f})",
            f"X Button (LMB): {'Pressed' if pygame.mouse.get_pressed()[0] else 'Released'}",
            f"Y Button (Space): {'Pressed' if key_states['space'] else 'Released'}",
            "",
            "Press ESC to exit"
        ]
        
        for i, text in enumerate(status_text):
            color = (255, 255, 255) if text else (100, 100, 100)
            rendered = font.render(text, True, color)
            screen.blit(rendered, (10, 10 + i * 30))
        
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    pygame.quit()

def main():
    """Main function to start the controller emulator"""
    global running
    
    try:
        # Start keyboard/mouse input handling
        handle_keyboard_input()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        running = False
        # Reset gamepad state
        with gamepad_lock:
            gamepad.reset()
            gamepad.update()
        print("Controller emulator stopped.")

if __name__ == "__main__":
    main()


