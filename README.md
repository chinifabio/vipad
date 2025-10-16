# ViPad - Virtual Xbox 360 Controller for Ryujinx

A Python application that emulates an Xbox 360 controller using mouse and keyboard inputs, specifically optimized for use with Ryujinx Nintendo Switch emulator.

## Features

### Movement & Camera
- **WASD Keys** → Left analog stick (character movement)
- **Mouse Movement** → Right analog stick (camera control)

### Face Buttons (Nintendo Switch layout)
- **Left Mouse Button** → X button (confirm/primary action)
- **Right Mouse Button** → A button (back/secondary action)  
- **Z Key** → A button (alternative)
- **Spacebar/C Key** → Y button (jump/special action)

### Shoulder Buttons & Triggers
- **Q Key** → L shoulder button
- **E Key** → R shoulder button
- **Left Shift** → ZL trigger (left trigger)
- **Left Ctrl** → ZR trigger (right trigger)

### System Buttons
- **Tab** → Select/Minus button
- **Enter** → Start/Plus button

### Stick Clicks
- **V Key** → Left stick click (L3)
- **Middle Mouse Button** → Right stick click (R3)

## Requirements

- Python 3.10+
- pygame
- vgamepad

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   uv sync
   ```

## Usage with Ryujinx

1. **Start the emulator**:
   ```bash
   uv run main.py
   ```

2. **Configure Ryujinx**:
   - Open Ryujinx
   - Go to Options → Settings → Input
   - Select "Xbox Controller" as input device
   - The virtual controller should appear automatically

3. **Focus the pygame window** for input capture to work

### Ryujinx-Specific Optimizations

- **Smaller deadzone** (0.05) for precise movement
- **Higher sensitivity** for camera control in 3D games
- **Slower decay rate** for right stick (better camera control)
- **120 FPS input polling** for responsive controls
- **Complete button mapping** including triggers and system buttons
- **Multiple button options** (e.g., A button via both right-click and Z key)

## Controls Reference

| Input | Nintendo Switch | Xbox Equivalent | Common Use |
|-------|----------------|-----------------|------------|
| WASD | Left Stick | Left Stick | Movement |
| Mouse | Right Stick | Right Stick | Camera |
| Left Click | X | X | Confirm/Primary |
| Right Click/Z | A | A | Back/Secondary |
| Space/C | Y | Y | Jump/Special |
| Q | L | LB | Left shoulder |
| E | R | RB | Right shoulder |
| Shift | ZL | LT | Left trigger |
| Ctrl | ZR | RT | Right trigger |
| Tab | - (Minus) | Back | Select/Menu |
| Enter | + (Plus) | Start | Pause/Settings |
| V | L3 | LS | Left stick click |
| Middle Click | R3 | RS | Right stick click |

## Troubleshooting

### General Issues
- Make sure the pygame window is focused and visible
- If controller isn't detected, restart both the emulator and Ryujinx
- Check Ryujinx input settings to ensure Xbox controller is selected

### Ryujinx-Specific Issues
- **Controller not detected**: Restart Ryujinx after starting the emulator
- **Input lag**: Close unnecessary applications, ensure 120 FPS mode is working
- **Wrong button mapping**: Verify Ryujinx is set to "Xbox Controller" mode
- **Stick drift**: Adjust `mouse_sensitivity` in the code if needed

### Performance Tips
- Keep the pygame window focused but you can minimize it
- For demanding games, consider lowering the polling rate from 120 to 60 FPS
- Adjust mouse sensitivity in the code for your preference

## How It Works

The application creates a virtual Xbox 360 controller that Ryujinx recognizes as a real controller. The mapping is optimized for Nintendo Switch games running in Ryujinx, with proper trigger support, system buttons, and camera controls suitable for 3D games.