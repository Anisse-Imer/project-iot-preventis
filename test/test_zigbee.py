import numpy as np
from core.zigbee_model import ZigBeeRadioModel

def run_zigbee_test():
    zigbee = ZigBeeRadioModel()
    
    try:
        size = int(input("Enter number of packets for ZigBee test (Etape 3): "))
    except ValueError:
        size = 200

    print(f"\n--- Testing ZigBee: 10m, 1 Wall ({size} packets) ---")
    
    rssi_values = []
    lqi_values = []
    
    for _ in range(size):
        # Simulation parameters from Etape 3.2
        rssi = zigbee.calculate_rssi(distance=10, num_walls=1) [cite: 47, 48]
        lqi = zigbee.calculate_lqi(rssi) [cite: 35]
        
        rssi_values.append(rssi)
        lqi_values.append(lqi)
            
    avg_rssi = np.mean(rssi_values)
    avg_lqi = np.mean(lqi_values)
    
    # Validation checks [cite: 48, 49]
    print(f"Results:")
    print(f"- Average RSSI: {avg_rssi:.2f} dBm (Target: -60 to -70 dBm)")
    print(f"- Average LQI: {avg_lqi:.2f} (Target: > 150)")
    
    if -70 <= avg_rssi <= -60 and avg_lqi > 150:
        print(">>> TEST PASSED: ZigBee simulator is valid.")
    else:
        print(">>> TEST FAILED: Check radio parameters.")

if __name__ == "__main__":
    run_zigbee_test()
    