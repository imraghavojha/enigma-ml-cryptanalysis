from src.data_generator import generate_plaintext, weighted_position
import random

# Set seed for reproducibility
random.seed(42)

# Test message generation
print("Generated Messages:")
for i in range(5):
    message = generate_plaintext(max_length=50)
    print(f"{i+1}. {message}")

# Test position generation
print("\nGenerated Positions:")
for i in range(5):
    position = weighted_position()
    print(f"{i+1}. {position}")