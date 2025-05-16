from src.data_generator import run_enigma

# Test with a short, known plaintext
test_plaintext = "WETTERBERICHT"
test_position = "AAA"

print(f"Testing Enigma integration:")
print(f"Plaintext: {test_plaintext}")
print(f"Position: {test_position}")

# Run the simulation
ciphertext = run_enigma(test_plaintext, test_position)

if ciphertext:
    print(f"Success! Ciphertext: {ciphertext}")
else:
    print("Error: Could not run Enigma simulation. Check the run_enigma function and your Enigma simulator path.")