"""
Enigma Machine training data generator.
Generates synthetic message data for ML-based cryptanalysis.
"""

import os
import csv
import random
import subprocess
import argparse
from tqdm import tqdm
import message_templates as mt

# Path to Enigma simulator executable
ENIGMA_PATH = "../enigma" # Adjust to your actual path

def generate_position():
    """Generate a random rotor position (AAA-ZZZ)"""
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))

def weighted_position():
    """Generate positions with historical bias (some positions were more common)"""
    # 10% chance of common starting positions
    if random.random() < 0.1:
        return random.choice(['AAA', 'AAB', 'AAZ', 'ZAA', 'BCD', 'XYZ'])
    return generate_position()

def generate_weather_report():
    """Generate a realistic German weather report"""
    grid = random.choice(mt.GRID_SQUARES)
    time = f"{random.randint(0, 23):02d}{random.randint(0, 59):02d}"
    temp = random.randint(-20, 30)
    visibility = random.randint(1, 20)
    wind_dir = random.choice(["NORD", "OST", "SUED", "WEST", "NORDOST", "SUEDOST", "SUEDWEST", "NORDWEST"])
    wind_strength = random.randint(1, 12)
    pressure = random.randint(990, 1030)
    phenomenon = random.choice(["KLAR", "BEWOELKT", "REGEN", "NEBEL", "SCHNEE", "STURM", ""])
    
    return mt.WEATHER_REPORT_TEMPLATE.format(
        grid=grid, time=time, temp=temp, visibility=visibility,
        wind_dir=wind_dir, wind_strength=wind_strength,
        pressure=pressure, phenomenon=phenomenon
    )

def generate_position_report():
    """Generate a realistic German position report"""
    grid = random.choice(mt.GRID_SQUARES)
    time = f"{random.randint(0, 23):02d}{random.randint(0, 59):02d}"
    course = random.randint(0, 359)
    speed = random.randint(1, 25)
    
    return mt.POSITION_REPORT_TEMPLATE.format(
        grid=grid, time=time, course=course, speed=speed
    )

def generate_enemy_sighting():
    """Generate a realistic German enemy sighting report"""
    vessel_type = random.choice(mt.VESSELS)
    number = random.randint(1, 10)
    location = f"QUADRAT {random.choice(mt.GRID_SQUARES)}"
    time = f"{random.randint(0, 23):02d}{random.randint(0, 59):02d}"
    course = random.randint(0, 359)
    speed = random.randint(1, 25)
    
    return mt.ENEMY_SIGHTING_TEMPLATE.format(
        vessel_type=vessel_type, number=number, location=location,
        time=time, course=course, speed=speed
    )

def generate_military_message():
    """Generate a realistic German military message"""
    prefix = random.choice(mt.MESSAGE_OPENINGS)
    unit = random.choice(mt.MILITARY_UNITS)
    command = random.choice(mt.COMMAND_TERMS)
    vessel = random.choice(mt.VESSELS)
    location = f"QUADRAT {random.choice(mt.GRID_SQUARES)}"
    
    return f"{prefix} {unit} {command} {vessel} {location}"

def generate_plaintext(max_length=50):
    """Generate plaintext message using weighted message types"""
    message_type = random.choices(
        ["WEATHER", "POSITION", "SIGHTING", "MILITARY"],
        weights=[0.3, 0.3, 0.2, 0.2],
        k=1
    )[0]
    
    if message_type == "WEATHER":
        plaintext = generate_weather_report()
    elif message_type == "POSITION":
        plaintext = generate_position_report()
    elif message_type == "SIGHTING":
        plaintext = generate_enemy_sighting()
    else:
        plaintext = generate_military_message()
    
    # Truncate to max length if needed (preserve complete words)
    if len(plaintext) > max_length:
        plaintext = plaintext[:max_length]
    
    # Convert to uppercase (Enigma only uses uppercase) and remove non-alphabetic chars
    plaintext = ''.join(c for c in plaintext.upper() if c.isalpha())
    
    return plaintext

def run_enigma(plaintext, position):
    """
    Run the Enigma simulator with the provided plaintext and position.
    Returns the encrypted ciphertext.
    """
    try:
        # Command format needs to match your Enigma simulator's interface
        # This example assumes you've added a batch mode
        cmd = [ENIGMA_PATH, "--encrypt", plaintext, "--position", position]
        
        # For menu-driven interface without batch mode, use:
        # echo -e "4\n{position}\n1\n{plaintext}\n5" | ./enigma
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        ciphertext = result.stdout.strip()
        
        return ciphertext
    except subprocess.CalledProcessError as e:
        print(f"Error running Enigma simulator: {e}")
        print(f"Error output: {e.stderr}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def generate_dataset(count, output_file, max_length=50):
    """Generate a dataset with the specified number of samples"""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    data = []
    with tqdm(total=count) as progress_bar:
        for _ in range(count):
            # Generate plaintext and position
            plaintext = generate_plaintext(max_length)
            position = weighted_position()
            
            # Skip if plaintext is empty
            if not plaintext:
                continue
                
            # Run Enigma simulation
            ciphertext = run_enigma(plaintext, position)
            
            # Skip if encryption failed
            if not ciphertext:
                continue
                
            # Store sample
            data.append({
                "plaintext": plaintext,
                "ciphertext": ciphertext,
                "rotor_left": position[0],
                "rotor_middle": position[1],
                "rotor_right": position[2],
                "full_position": position
            })
            
            progress_bar.update(1)
    
    # Write to CSV file
    with open(output_file, 'w', newline='') as f:
        fieldnames = ["plaintext", "ciphertext", "rotor_left", "rotor_middle", "rotor_right", "full_position"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Generated {len(data)} samples and saved to {output_file}")
    return data

def main():
    parser = argparse.ArgumentParser(description="Generate Enigma encryption dataset")
    parser.add_argument("--count", type=int, default=10000, help="Number of samples to generate")
    parser.add_argument("--output", type=str, default="../data/enigma_dataset.csv", help="Output CSV file path")
    parser.add_argument("--length", type=int, default=50, help="Maximum message length")
    parser.add_argument("--test", action="store_true", help="Run in test mode (5 samples only)")
    
    args = parser.parse_args()
    
    # Test mode for quick verification
    if args.test:
        print("Running in test mode (5 samples)")
        generate_dataset(5, args.output, args.length)
    else:
        generate_dataset(args.count, args.output, args.length)

if __name__ == "__main__":
    main()