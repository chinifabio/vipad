# ViPad - Virtual Xbox 360 Controller

A Python application that emulates an Xbox 360 controller using mouse and keyboard inputs.

## Features

- **WASD Keys** → Left analog stick
- **Mouse Movement** → Right analog stick
- **Left Mouse Button** → X button
- **Spacebar** → Y button

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

## Usage

Run the emulator:
```bash
uv run main.py
```

### Controls

- **W/A/S/D**: Control the left analog stick (movement)
- **Mouse movement**: Control the right analog stick (camera/look)
- **Left mouse button**: X button (primary action)
- **Spacebar**: Y button (secondary action)
- **ESC**: Exit the emulator

### Important Notes

- The pygame window must be focused for input capture to work
- Mouse input is captured relatively - move the mouse to control the right stick
- The right stick will gradually return to center when not moving the mouse
- All controller inputs are sent to the system as a virtual Xbox 360 controller

## How It Works

The application uses:
- `vgamepad` to create a virtual Xbox 360 controller
- `pygame` to capture keyboard and mouse input
- Threading to handle input processing and controller updates

The virtual controller will appear to games and applications as a real Xbox 360 controller connected to your system.

## Troubleshooting

- Make sure the pygame window is focused
- If the controller isn't detected by games, try restarting the application
- Some games may require you to enable controller support in their settings