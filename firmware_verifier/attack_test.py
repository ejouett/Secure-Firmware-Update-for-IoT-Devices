# attack_success_rate_test.py

import subprocess
import os
import random

FIRMWARE_FILE = "firmware.bin"
TAMPERED_FILE = "firmware.bin"
SIGNATURE_FILE = "signature.bin"
PUBLIC_KEY_FILE = "public_key.pem"

NUM_TESTS = 50
attack_success = 0
defense_success = 0

for i in range(NUM_TESTS):
    # Tamper with firmware: randomly flip a byte
    with open(FIRMWARE_FILE, "rb") as f:
        firmware_data = bytearray(f.read())

    # Randomly modify one byte
    index_to_modify = random.randint(0, len(firmware_data) - 1)
    firmware_data[index_to_modify] ^= 0xFF  # flip bits

    # Save tampered firmware
    with open(TAMPERED_FILE, "wb") as f:
        f.write(firmware_data)

    # Run your verifier
    result = subprocess.run(["./verifier", TAMPERED_FILE, SIGNATURE_FILE, PUBLIC_KEY_FILE],
                             capture_output=True, text=True)
    
    if "✅" in result.stdout:
        attack_success += 1
    else:
        defense_success += 1

# Clean up tampered file
os.remove(TAMPERED_FILE)

# Plot results
import matplotlib.pyplot as plt

labels = ['Attack Succeeded', 'Attack Blocked']
values = [attack_success, defense_success]

plt.bar(labels, values, color=['red', 'green'])
plt.title('Attack Success Rate vs Secure Update Verification')
plt.ylabel('Number of Attempts')
plt.savefig('attack_success_rate.png')
plt.show()

print(f"Attack Success: {attack_success}/{NUM_TESTS}")
print(f"Defense Success: {defense_success}/{NUM_TESTS}")
