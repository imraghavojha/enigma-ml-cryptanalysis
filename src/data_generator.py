"""
Enigma Machine training data generator.
Generates synthetic message data for ML-based cryptanalysis.
"""

import os
import csv
import random
import subprocess
import argparse
import math
from collections import Counter
from tqdm import tqdm
from src import message_templates as mt

# Path to Enigma simulator executable
ENIGMA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "enigma"))

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
    """Run the Enigma simulator using command-line interface"""
    try:
        # Use the command-line interface
        cmd = [ENIGMA_PATH, "--encrypt", plaintext, "--position", position]
        
        # Run the process with a timeout
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        # Check if the process ran successfully
        if result.returncode != 0:
            print(f"Enigma process failed with return code {result.returncode}")
            print(f"Error output: {result.stderr}")
            return None
        
        # The output should be just the ciphertext
        ciphertext = result.stdout.strip()
        return ciphertext
    except subprocess.TimeoutExpired:
        print(f"Error: Enigma simulator timed out after 10 seconds")
        return None
    except Exception as e:
        print(f"Error running Enigma: {e}")
        return None

def calculate_entropy(text):
    """Calculate Shannon entropy of text"""
    freq = Counter(text)
    length = len(text)
    return -sum(count/length * math.log2(count/length) for count in freq.values())

def index_of_coincidence(text):
    """Calculate index of coincidence"""
    n = len(text)
    if n <= 1:
        return 0
    
    freq = Counter(text)
    sum_freqs = sum(count * (count - 1) for count in freq.values())
    return sum_freqs / (n * (n - 1))

def calculate_bigram_stats(text):
    """Calculate bigram statistics for the text"""
    if len(text) < 2:
        return {}, ""
    
    bigrams = [text[i:i+2] for i in range(len(text)-1)]
    bigram_counts = Counter(bigrams)
    most_common = bigram_counts.most_common(1)[0][0] if bigrams else ""
    
    return bigram_counts, most_common

def calculate_letter_shift_stats(plaintext, ciphertext):
    """Calculate statistics about letter shifts between plaintext and ciphertext"""
    if len(plaintext) != len(ciphertext):
        return {}, 0, 0
    
    # Calculate shift for each letter (how many positions it moved in the alphabet)
    shifts = [(ord(c) - ord(p)) % 26 for p, c in zip(plaintext, ciphertext)]
    
    # Count shifts by position
    shift_counts = Counter(shifts)
    
    # Count letters that encrypted to themselves (should be 0 in Enigma, helpful for verification)
    self_encryptions = shifts.count(0)
    
    # Calculate average shift
    avg_shift = sum(shifts) / len(shifts) if shifts else 0
    
    return shift_counts, self_encryptions, avg_shift

def generate_dataset(count, output_file, max_length=50, batch_size=1000):
    """Generate a dataset with the specified number of samples and advanced metrics"""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Define all field names in order
    fieldnames = [
        # Original fields
        "plaintext", "ciphertext", "rotor_left", "rotor_middle", "rotor_right", "full_position",
        "message_type",
        
        # Basic metrics
        "plaintext_length", "ciphertext_length",
        
        # Statistical metrics
        "entropy", "index_of_coincidence", "kappa_1",
        
        # Letter pattern metrics
        "most_common_plaintext_letter", "most_common_ciphertext_letter",
        "most_common_bigram", "top_3_bigrams",
        
        # Enigma-specific metrics
        "self_encryptions", "avg_shift", "first_letter_shift", "last_letter_shift",
        "repeated_letters",
        
        # Message structure
        "first_letter", "last_letter" 
    ]
    
    # Create the CSV file and write the header
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
    
    success_count = 0
    batch_data = []
    
    with tqdm(total=count) as progress_bar:
        while success_count < count:
            # Generate plaintext and position
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
            
            # Truncate to max length if needed
            if len(plaintext) > max_length:
                plaintext = plaintext[:max_length]
            
            # Convert to uppercase and remove non-alphabetic chars
            plaintext = ''.join(c for c in plaintext.upper() if c.isalpha())
            
            # Skip if plaintext is empty or too short
            if len(plaintext) < 8:  # Minimum length for meaningful metrics
                continue
                
            # Generate position with historical weighting
            position = weighted_position()
                
            # Run Enigma simulation
            ciphertext = run_enigma(plaintext, position)
            
            # Skip if encryption failed
            if not ciphertext:
                continue
            
            # ============= CALCULATE METRICS =============
            
            # Basic letter frequency analysis
            plaintext_freq = Counter(plaintext)
            ciphertext_freq = Counter(ciphertext)
            
            # Calculate cryptanalysis metrics
            entropy = calculate_entropy(ciphertext)
            ic = index_of_coincidence(ciphertext)
            
            # Bigram analysis
            bigram_counts, most_common_bigram = calculate_bigram_stats(ciphertext)
            top_3_bigrams = ','.join([b for b, _ in Counter(bigram_counts).most_common(3)])
            
            # Letter shift analysis
            shift_counts, self_encryptions, avg_shift = calculate_letter_shift_stats(plaintext, ciphertext)
            
            # Calculate kappa test (coincidence between offset ciphertext copies)
            # This is particularly valuable for Enigma cryptanalysis
            kappa_1 = 0
            if len(ciphertext) > 1:
                matches = sum(1 for i in range(len(ciphertext)-1) if ciphertext[i] == ciphertext[i+1])
                kappa_1 = matches / (len(ciphertext) - 1)
            
            # First and last letter stats
            first_letter_shift = (ord(ciphertext[0]) - ord(plaintext[0])) % 26
            last_letter_shift = (ord(ciphertext[-1]) - ord(plaintext[-1])) % 26
            
            # Count repeated letters in ciphertext (AA, BB, etc.)
            repeated_letters = sum(1 for i in range(len(ciphertext)-1) if ciphertext[i] == ciphertext[i+1])
            
            # Store all data
            sample_data = {
                # Original fields
                "plaintext": plaintext,
                "ciphertext": ciphertext,
                "rotor_left": position[0],
                "rotor_middle": position[1],
                "rotor_right": position[2],
                "full_position": position,
                "message_type": message_type,
                
                # Basic metrics
                "plaintext_length": len(plaintext),
                "ciphertext_length": len(ciphertext),
                
                # Statistical metrics
                "entropy": entropy,
                "index_of_coincidence": ic,
                "kappa_1": kappa_1,
                
                # Letter pattern metrics
                "most_common_plaintext_letter": plaintext_freq.most_common(1)[0][0] if plaintext_freq else "",
                "most_common_ciphertext_letter": ciphertext_freq.most_common(1)[0][0] if ciphertext_freq else "",
                "most_common_bigram": most_common_bigram,
                "top_3_bigrams": top_3_bigrams,
                
                # Enigma-specific metrics
                "self_encryptions": self_encryptions,  # Should be 0 for valid Enigma
                "avg_shift": avg_shift,
                "first_letter_shift": first_letter_shift,
                "last_letter_shift": last_letter_shift,
                "repeated_letters": repeated_letters,
                
                # Message structure 
                "first_letter": ciphertext[0] if ciphertext else "",
                "last_letter": ciphertext[-1] if ciphertext else ""
            }
            
            # Add to batch
            batch_data.append(sample_data)
            success_count += 1
            
            # Write batch to disk when it reaches batch_size
            if len(batch_data) >= batch_size:
                with open(output_file, 'a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writerows(batch_data)
                batch_data = []  # Clear the batch
            
            progress_bar.update(1)
    
    # Write any remaining samples
    if batch_data:
        with open(output_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerows(batch_data)
    
    print(f"Generated {success_count} samples and saved to {output_file}")
    print(f"Metrics calculated: {len(fieldnames) - 6} additional features")
    return True

def main():
    parser = argparse.ArgumentParser(description="Generate Enigma encryption dataset")
    parser.add_argument("--count", type=int, default=10000, help="Number of samples to generate")
    parser.add_argument("--output", type=str, default="../data/enigma_dataset.csv", help="Output CSV file path")
    parser.add_argument("--length", type=int, default=50, help="Maximum message length")
    parser.add_argument("--test", action="store_true", help="Run in test mode (5 samples only)")
    parser.add_argument("--batch-size", type=int, default=1000, help="Batch size for writing to disk")
    
    args = parser.parse_args()
    
    # Test mode for quick verification
    if args.test:
        print("Running in test mode (5 samples)")
        generate_dataset(5, args.output, args.length, args.batch_size)
    else:
        generate_dataset(args.count, args.output, args.length, args.batch_size)

if __name__ == "__main__":
    main()