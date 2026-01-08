# Metroliner III Pedestal Simulation – Touch Display Framework

This repository contains the **UI component** of a project that simulates the **Metroliner III pedestal** on a **touchscreen display**, built with a **multithreaded event-driven architecture** in **Python**.  
It is optimized for **Raspberry Pi 3** and communicates with the X-Plane flight simulator via **UDP** for real-time synchronization.

**Note:** This repository only includes the **User Interface (UI)** portion of the project. Other components are not publicly available due to restrictions.

## UI Module Overview

The core of this repository is the **`jg_ui_mngr.py`** module, which manages the **touchscreen interface** for the Metroliner III pedestal. It builds the graphical layout using **Tkinter** and custom widgets, and emits events through a callback mechanism for integration with the rest of the system.

### Key Responsibilities
- Creates a **full-screen UI** optimized for Raspberry Pi.
- Implements interactive controls:
  - **Trim Selector** (Pilot/Copilot)
  - **Engine Stop & Feather** switches
  - **Flaps Lever** with snap positions (UP, 1/4, 1/2, DN)
  - **Landing Gear** toggle
  - **Parking Brake** button
  - **Fuel and Hydraulic switches**
  - **Aux Trim** momentary control
- Uses **image-based widgets** for realistic animations.
- Reports user actions via `jg_ui_mngr_events_cb(event_id, payload)`.


## Features
- **Multithreaded architecture**: Separate threads for event handling and GUI rendering.
- **Event-driven framework**: Scalable and modular design for responsive interaction.
- **Touchscreen support**: Interactive UI with image-based animations.
- **UDP communication**: Real-time data exchange with the simulator.
- **Optimized for Raspberry Pi**: Lightweight and efficient for resource-constrained environments.

## Video Demonstration

Watch the video demonstration of the application, titled "Metroliner III Pedestal Simulation – UI Overview & Functionality" [here](https://youtu.be/6uQhjiYeBb4).

## Technology Used
- **Language**: Python
- **Hardware**: Raspberry Pi 3
- **Concepts**: Multithreading, Event-driven architecture, Algorithms & Data Structures
- **Protocols**: UDP, UART
- **UI**: Tkinter + Pillow for image rendering

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
