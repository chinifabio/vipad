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
mouse_sensitivity = 2.0  # Increased sensitivity for better camera control
right_stick_x = 0.0
right_stick_y = 0.0
left_stick_x = 0.0
left_stick_y = 0.0
gamepad_lock = Lock()
mouse_captured = False  # Track if mouse is captured

# Key states for all controls
key_states = {
    'w': False,
    'a': False,
    's': False,
    'd': False,
    'space': False,
    'q': False,      # L shoulder
    'e': False,      # R shoulder
    'tab': False,    # Select/Minus
    'enter': False,  # Start/Plus
    'shift': False,  # Left trigger
    'ctrl': False,   # Right trigger
    'z': False,      # A button
    'x': False,      # B button
    'c': False,      # Y button (in addition to space)
    'v': False       # Left stick click
}

def normalize_stick_value(value, deadzone=0.05):
    """Normalize stick values to -1.0 to 1.0 range with smaller deadzone for Ryujinx"""
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
    """Handle keyboard input for all controller buttons"""
    global left_stick_x, left_stick_y, key_states, running
    
    # Create a window for capturing input
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Ryujinx Controller Emulator - Focus this window for input!")
    clock = pygame.time.Clock()
    
    # Start with mouse not captured
    mouse_captured = False
    pygame.event.set_grab(False)
    
    print("Ryujinx Xbox 360 Controller Emulator Started!")
    print("Controls for Nintendo Switch games:")
    print("- WASD: Left stick (movement)")
    print("- Mouse: Right stick (camera) - ONLY when captured")
    print("- Left Click: X button (confirm/primary)")
    print("- Right Click: A button (back/secondary)")
    print("- Space/C: Y button (jump/special)")
    print("- Z: A button (alternative)")
    print("- Q: Left shoulder (L)")
    print("- E: Right shoulder (R)")
    print("- Shift: Left trigger (ZL)")
    print("- Ctrl: Right trigger (ZR)")
    print("- Tab: Select/Minus")
    print("- Enter: Start/Plus")
    print("- V: Left stick click (L3)")
    print("- Middle Click: Right stick click (R3)")
    print("- F1: Toggle mouse capture ON/OFF")
    print("- ESC: Exit")
    print("\nPress F1 to capture/release mouse for camera control!")
    print("Mouse capture is currently: OFF")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
                elif event.key == pygame.K_F1:
                    # Toggle mouse capture
                    mouse_captured = not mouse_captured
                    pygame.event.set_grab(mouse_captured)
                    if mouse_captured:
                        pygame.mouse.set_pos(300, 200)
                        print("Mouse capture: ON - Mouse controls right stick")
                    else:
                        print("Mouse capture: OFF - Mouse is free")
                # Movement keys
                elif event.key == pygame.K_w:
                    key_states['w'] = True
                elif event.key == pygame.K_a:
                    key_states['a'] = True
                elif event.key == pygame.K_s:
                    key_states['s'] = True
                elif event.key == pygame.K_d:
                    key_states['d'] = True
                # Face buttons
                elif event.key == pygame.K_SPACE:
                    key_states['space'] = True
                    with gamepad_lock:
                        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
                        gamepad.update()
                elif event.key == pygame.K_c:
                    key_states['c'] = True
                    with gamepad_lock:
                        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
                        gamepad.update()
                elif event.key == pygame.K_z:
                    key_states['z'] = True
                    with gamepad_lock:
                        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                        gamepad.update()
                # Shoulder buttons
                elif event.key == pygame.K_q:
                    key_states['q'] = True
                    with gamepad_lock:
                        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
                        gamepad.update()
                elif event.key == pygame.K_e:
                    key_states['e'] = True
                    with gamepad_lock:
                        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
                        gamepad.update()
                # Triggers
                elif event.key == pygame.K_LSHIFT:
                    key_states['shift'] = True
                    with gamepad_lock:
                        gamepad.left_trigger_float(value_float=1.0)
                        gamepad.update()
                elif event.key == pygame.K_LCTRL:
                    key_states['ctrl'] = True
                    with gamepad_lock:
                        gamepad.right_trigger_float(value_float=1.0)
                        gamepad.update()
                # System buttons
                elif event.key == pygame.K_TAB:
                    key_states['tab'] = True
                    with gamepad_lock:
                        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
                        gamepad.update()
                elif event.key == pygame.K_RETURN:
                    key_states['enter'] = True
                    with gamepad_lock:
                        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
                        gamepad.update()
                # Stick clicks
                elif event.key == pygame.K_v:
                    key_states['v'] = True
                    with gamepad_lock:
                        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
                        gamepad.update()
            
            elif event.type == pygame.KEYUP:
                # Movement keys
                if event.key == pygame.K_w:
                    key_states['w'] = False
                elif event.key == pygame.K_a:
                    key_states['a'] = False
                elif event.key == pygame.K_s:
                    key_states['s'] = False
                elif event.key == pygame.K_d:
                    key_states['d'] = False
                # Face buttons
                elif event.key == pygame.K_SPACE:
                    key_states['space'] = False
                    with gamepad_lock:
                        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
                        gamepad.update()
                elif event.key == pygame.K_c:
                    key_states['c'] = False
                    with gamepad_lock:
                        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
                        gamepad.update()
                elif event.key == pygame.K_z:
                    key_states['z'] = False
                    with gamepad_lock:
                        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                        gamepad.update()
                # Shoulder buttons
                elif event.key == pygame.K_q:
                    key_states['q'] = False
                    with gamepad_lock:
                        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
                        gamepad.update()
                elif event.key == pygame.K_e:
                    key_states['e'] = False
                    with gamepad_lock:
                        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
                        gamepad.update()
                # Triggers
                elif event.key == pygame.K_LSHIFT:
                    key_states['shift'] = False
                    with gamepad_lock:
                        gamepad.left_trigger_float(value_float=0.0)
                        gamepad.update()
                elif event.key == pygame.K_LCTRL:
                    key_states['ctrl'] = False
                    with gamepad_lock:
                        gamepad.right_trigger_float(value_float=0.0)
                        gamepad.update()
                # System buttons
                elif event.key == pygame.K_TAB:
                    key_states['tab'] = False
                    with gamepad_lock:
                        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
                        gamepad.update()
                elif event.key == pygame.K_RETURN:
                    key_states['enter'] = False
                    with gamepad_lock:
                        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
                        gamepad.update()
                # Stick clicks
                elif event.key == pygame.K_v:
                    key_states['v'] = False
                    with gamepad_lock:
                        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
                        gamepad.update()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button - X button (confirm)
                    with gamepad_lock:
                        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
                        gamepad.update()
                elif event.button == 3:  # Right mouse button - A button (back)
                    with gamepad_lock:
                        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                        gamepad.update()
                elif event.button == 2:  # Middle mouse button - Right stick click
                    with gamepad_lock:
                        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
                        gamepad.update()
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    with gamepad_lock:
                        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
                        gamepad.update()
                elif event.button == 3:  # Right mouse button
                    with gamepad_lock:
                        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                        gamepad.update()
                elif event.button == 2:  # Middle mouse button
                    with gamepad_lock:
                        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
                        gamepad.update()
            
            elif event.type == pygame.MOUSEMOTION:
                # Handle mouse movement for right stick only when captured
                if mouse_captured:
                    rel_x, rel_y = event.rel
                    global right_stick_x, right_stick_y
                    
                    # Apply sensitivity and accumulate movement
                    right_stick_x += rel_x * mouse_sensitivity * 0.008  # Reduced multiplier for smoother control
                    right_stick_y += rel_y * mouse_sensitivity * 0.008
                    
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
        
        # Apply mouse movement decay for right stick (returns to center gradually)
        right_stick_x *= 0.92  # Slightly slower decay for better camera control
        right_stick_y *= 0.92
        
        # Update the gamepad
        update_gamepad()
        
        # Draw enhanced status on screen
        screen.fill((20, 20, 30))
        font = pygame.font.Font(None, 20)
        title_font = pygame.font.Font(None, 28)
        
        # Title
        title = title_font.render("Ryujinx Controller Emulator", True, (100, 200, 255))
        screen.blit(title, (10, 10))
        
        # Status text
        status_text = [
            f"Mouse Capture: {'ON' if mouse_captured else 'OFF'} (Press F1 to toggle)",
            f"Left Stick (WASD): ({left_stick_x:.2f}, {left_stick_y:.2f})",
            f"Right Stick (Mouse): ({right_stick_x:.2f}, {right_stick_y:.2f})",
            "",
            "Buttons:",
            f"X (LMB): {'ON' if pygame.mouse.get_pressed()[0] else 'OFF'}",
            f"A (RMB/Z): {'ON' if (pygame.mouse.get_pressed()[2] or key_states['z']) else 'OFF'}",
            f"Y (Space/C): {'ON' if (key_states['space'] or key_states['c']) else 'OFF'}",
            f"L (Q): {'ON' if key_states['q'] else 'OFF'}",
            f"R (E): {'ON' if key_states['e'] else 'OFF'}",
            f"ZL (Shift): {'ON' if key_states['shift'] else 'OFF'}",
            f"ZR (Ctrl): {'ON' if key_states['ctrl'] else 'OFF'}",
            f"Start (Enter): {'ON' if key_states['enter'] else 'OFF'}",
            f"Select (Tab): {'ON' if key_states['tab'] else 'OFF'}",
            "",
            "Press F1 to toggle mouse capture | Press ESC to exit"
        ]
        
        for i, text in enumerate(status_text):
            if text == "":
                continue
            color = (255, 255, 255)
            if "ON" in text:
                color = (100, 255, 100)
            elif "OFF" in text:
                color = (150, 150, 150)
            elif text.startswith("Buttons:"):
                color = (255, 200, 100)
            
            rendered = font.render(text, True, color)
            screen.blit(rendered, (10, 50 + i * 22))
        
        pygame.display.flip()
        clock.tick(120)  # Higher FPS for smoother input
    
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


