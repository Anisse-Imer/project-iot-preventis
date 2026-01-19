import numpy as np
from utils.math_physics import log_distance_path_loss

class LoRaRadioModel:
    def __init__(self):
        # Parameters for Outdoor environment [cite: 28]
        self.d0 = 1.0        # Reference distance (1m)
        self.pl_d0 = 12.0    # Path loss at d0 for LoRa frequencies
        self.n = 2.5         # Path loss exponent [cite: 13]
        self.sigma = 6.0     # Shadowing [cite: 14]
        self.sensitivity_table = {
            7: -123, 8: -126, 9: -129, 10: -132, 11: -134, 12: -137
        } # Table de sensibilité [cite: 30]

    def calculate_path_loss(self, distance):
        return log_distance_path_loss(distance, self.d0, self.pl_d0, self.n, self.sigma)

    def calculate_rssi(self, tx_power, distance):
        # RSSI = TxPower - PathLoss [cite: 24]
        return tx_power - self.calculate_path_loss(distance)

    def calculate_snr(self, rssi):
        noise_floor = -120 # Standard noise floor for SNR [cite: 25]
        return rssi - noise_floor

    def is_received(self, rssi, spreading_factor):
        # Réception réussie if RSSI > Sensitivity [cite: 26]
        threshold = self.sensitivity_table.get(spreading_factor, -123)
        return rssi >= threshold
    