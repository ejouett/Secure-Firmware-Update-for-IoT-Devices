# flash_size_comparison_test.py

import os
import matplotlib.pyplot as plt

# Path to your verifier binary
verifier_binary_path = "firmware_verifier/verifier"

def get_file_size_kb(path):
    size_bytes = os.path.getsize(path)
    return size_bytes / 1024  # Convert to KB

# Measure your verifier binary size
your_flash_size_kb = get_file_size_kb(verifier_binary_path)
print(f"Your Verifier Binary Size: {your_flash_size_kb:.2f} KB")

# Real-world public values
# Approximate from TUF and Mender project sources
tuf_flash_size_kb = 4000  # TUF Python client (interpreted)
mender_flash_size_kb = 800  # Mender C client (compiled)

# Plot the results
methods = ['Your Secure Verifier', 'TUF', 'Mender']
flash_sizes = [your_flash_size_kb, tuf_flash_size_kb, mender_flash_size_kb]

plt.bar(methods, flash_sizes, color=['green', 'blue', 'orange'])
plt.ylabel('Flash Size (KB)')
plt.title('Firmware Update Flash Storage Comparison')
plt.savefig('flash_size_comparison.png')
plt.show()
