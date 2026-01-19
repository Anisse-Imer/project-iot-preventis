import numpy as np
from utils.math_physics import log_distance_path_loss

class ZigBeeRadioModel:
    def __init__(self):
        self.frequency = 2.4e9 # 2.4 GHz [cite: 38]
        self.d0 = 1.0
        self.pl_d0 = 40.0      # Higher path loss for 2.4GHz
        self.n = 3.0           # Indoor exponent [cite: 33]
        self.wall_attenuation = 5.0 # Atténuation par mur (dB) [cite: 39]
        self.sensitivity = -100     # Sensibilité ZigBee [cite: 40, 81]

    def calculate_path_loss_indoor(self, distance, num_walls):
        # Base loss + penalty for each wall [cite: 33]
        base_loss = log_distance_path_loss(distance, self.d0, self.pl_d0, self.n, 3.0)
        return base_loss + (num_walls * self.wall_attenuation)

    def calculate_rssi(self, distance, num_walls, tx_power=3):
        return tx_power - self.calculate_path_loss_indoor(distance, num_walls)

    def calculate_lqi(self, rssi):
        # Map RSSI (-100 to -40) to LQI (0-255) [cite: 35]
        lqi = np.clip(4 * (rssi + 100), 0, 255)
        return int(lqi)

    def is_received(self, rssi):
        return rssi >= self.sensitivity # Décision de réception [cite: 36]
    