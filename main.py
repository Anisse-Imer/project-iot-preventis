import os
import numpy as np
import pandas as pd
from datetime import datetime
from core.lora_model import LoRaRadioModel
from core.zigbee_model import ZigBeeRadioModel

def save_config(path, lora_pkts, zigbee_pkts):
    """Saves the simulation parameters to a text file."""
    config_content = f"""Simulation Config
------------------
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
LoRa Packets per Distance: {lora_pkts}
LoRa Config: SF7, TX 14dBm, Outdoor
ZigBee Packets per Scenario: {zigbee_pkts}
ZigBee Config: 2.4GHz, Indoor
"""
    with open(os.path.join(path, "config.txt"), "w") as f:
        f.write(config_content)

def run_campaign(model, scenarios, packets, tech_type, campaign_path):
    summary_data = []
    detailed_data = []
    
    print(f"Running {tech_type}...")
    for sc in scenarios:
        successes = 0
        rssi_vals = []
        metrics = []
        
        for p_id in range(1, packets + 1):
            if tech_type == "LoRa":
                # Etape 4.1 Config: SF7, TX 14dBm
                rssi = model.calculate_rssi(tx_power=14, distance=sc['dist'])
                metric = model.calculate_snr(rssi)
                received = model.is_received(rssi, spreading_factor=7)
            else:
                # Etape 4.2 Config: Indoor 2.4GHz
                rssi = model.calculate_rssi(distance=sc['dist'], num_walls=sc['walls'])
                metric = model.calculate_lqi(rssi)
                received = model.is_received(rssi)
            
            if received: successes += 1
            rssi_vals.append(rssi)
            metrics.append(metric)
            
            # Store detailed packet activity (one line per activity)
            detailed_data.append({
                "Scenario_ID": sc.get('desc', sc['dist']),
                "Packet_ID": p_id,
                "RSSI": rssi,
                "Metric": metric,
                "Success": 1 if received else 0
            })
            
        # Calculate Aggregated Metrics for Etape 4 tables
        summary_data.append({
            "Scenario": sc.get('desc', sc['dist']),
            "Sent": packets,
            "Received": successes,
            "PDR_%": (successes / packets) * 100,
            "RSSI_avg": np.mean(rssi_vals),
            "Metric_avg": np.mean(metrics)
        })

    # Save summary and detailed logs in the campaign folder
    pd.DataFrame(summary_data).to_csv(os.path.join(campaign_path, f"{tech_type.lower()}_summary.csv"), index=False)
    pd.DataFrame(detailed_data).to_csv(os.path.join(campaign_path, f"{tech_type.lower()}_detailed_logs.csv"), index=False)

if __name__ == "__main__":
    # Setup Campaign Folder structure
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    campaign_path = f"results/campaign_{timestamp}"
    os.makedirs(campaign_path, exist_ok=True)
    
    try:
        # Prompt for packet counts (Etape 4 requires 20 for LoRa, 30 for ZigBee)
        l_input = input("Packets for LoRa (default 20): ")
        l_pkts = int(l_input) if l_input else 20
        
        z_input = input("Packets for ZigBee (default 30): ")
        z_pkts = int(z_input) if z_input else 30
        
        save_config(campaign_path, l_pkts, z_pkts)
        
        # Execute LoRa Campaign (Outdoor)
        l_scenarios = [{'dist': d} for d in [25, 50, 100, 200, 500]]
        run_campaign(LoRaRadioModel(), l_scenarios, l_pkts, "LoRa", campaign_path)
        
        # Execute ZigBee Campaign (Indoor)
        z_scenarios = [
            {'dist': 5,  'walls': 0, 'desc': "Meme_piece"},
            {'dist': 10, 'walls': 1, 'desc': "Piece_adjacente"},
            {'dist': 15, 'walls': 2, 'desc': "2_pieces"},
            {'dist': 20, 'walls': 3, 'desc': "Etage_different"}
        ]
        run_campaign(ZigBeeRadioModel(), z_scenarios, z_pkts, "ZigBee", campaign_path)
        
        print(f"\n[SUCCESS] Results generated in: {campaign_path}")
        
    except ValueError:
        print("Error: Please enter a valid integer for packet counts.")
        