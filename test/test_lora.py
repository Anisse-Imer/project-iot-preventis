import numpy as np
from core.lora_model import LoRaRadioModel

def run_lora_test():
    lora = LoRaRadioModel()
    
    # User-defined campaign size
    try:
        size = int(input("Enter number of packets for LoRa test (Etape 3): "))
    except ValueError:
        size = 200

    print(f"\n--- Testing LoRa: 100m, SF7, 14dBm ({size} packets) ---")
    
    successes = 0
    rssi_values = []
    
    for _ in range(size):
        # Simulation parameters from Etape 3.1
        rssi = lora.calculate_rssi(tx_power=14, distance=100) [cite: 44]
        rssi_values.append(rssi)
        
        # Verify reception based on SF7 sensitivity [cite: 26]
        if lora.is_received(rssi, spreading_factor=7):
            successes += 1
            
    avg_rssi = np.mean(rssi_values)
    pdr = (successes / size) * 100
    
    # Validation checks [cite: 45, 46]
    print(f"Results:")
    print(f"- Average RSSI: {avg_rssi:.2f} dBm (Target: -80 to -90 dBm)")
    print(f"- PDR: {pdr:.2f}% (Target: > 90%)")
    
    if -90 <= avg_rssi <= -80 and pdr > 90:
        print(">>> TEST PASSED: LoRa simulator is valid.")
    else:
        print(">>> TEST FAILED: Check radio parameters.")

if __name__ == "__main__":
    run_lora_test()
    