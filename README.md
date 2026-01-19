# IoT Protocol Simulation: LoRa vs ZigBee
**Copyright (c) 2026 Anisse Imerzoukene** **Licensed under the MIT License**
## Presentation
This project provides a Python-based simulation environment to evaluate and compare **LoRa** and **ZigBee** radio protocols. It models real-world radio behaviors—including log-distance path loss and environmental interference—to determine the most suitable technology for campus-wide IoT deployments.
## Project Structure
| File / Folder | Description |
| --- | --- |
| `main.py` | The main entry point. Handles user input for campaign size and executes both simulation campaigns.|
| `LICENSE` | MIT License file registered to Anisse Imerzoukene. |
| `core/lora_model.py` | Contains the `LoRaRadioModel` class; handles outdoor path loss, RSSI, and SNR calculations based on Spreading Factors.|
| `core/zigbee_model.py` | Contains the `ZigBeeRadioModel` class; models 2.4 GHz indoor environments with wall attenuation and LQI mapping.|
| `utils/math_physics.py` | Core mathematical implementation of the Log-Distance Path Loss formula.|
| `utils/data_viz.py` | Visualization script to generate scientific plots of PDR, RSSI, and SNR/LQI.|
| `tests/` | Directory containing unit tests to validate simulator accuracy against known benchmarks.|
| `results/` | Output directory where timestamped campaign folders, CSV logs, and configuration files are stored.|
| `requirements.txt` | List of Python dependencies (numpy, pandas, matplotlib). |
---
## Getting Started
1. **Install dependencies:**
```bash
pip install -r requirements.txt

```
2. **Run the simulation:**
```bash
python main.py

```
Follow the console prompts to set the number of packets for the measurement campaign.
3. **Analyze Results:**
Check the `results/campaign_YYYYMMDD_HHMMSS/` folder for detailed logs and summary tables.
