# memory_usage_verification_test.py

import subprocess
import time
import psutil
import matplotlib.pyplot as plt

# Path to your verifier binary and input files
VERIFIER_CMD = ["./verifier", "firmware.bin", "signature.bin", "public_key.pem"]

def measure_ram_usage(cmd):
    process = subprocess.Popen(cmd)
    proc = psutil.Process(process.pid)
    
    peak_memory = 0

    while True:
        if process.poll() is not None:
            break
        try:
            mem = proc.memory_info().rss  # Resident Set Size in bytes
            peak_memory = max(peak_memory, mem)
        except psutil.NoSuchProcess:
            break
        time.sleep(0.01)  # Poll every 10ms

    return peak_memory / 1024  # Convert to KB

# Measure your firmware verifier
your_memory_kb = measure_ram_usage(VERIFIER_CMD)
print(f"Your Secure Verifier Peak RAM Usage: {your_memory_kb:.2f} KB")

# Public comparison values (based on known studies)
# Source values approximated from TUF and Mender documentation and papers
tuf_memory_kb = 5000    # TUF Python reference client (heavier)
mender_memory_kb = 1500  # Mender lightweight client

# Plot the results
methods = ['Your Secure Verifier', 'TUF', 'Mender']
memory_usage = [your_memory_kb, tuf_memory_kb, mender_memory_kb]

plt.bar(methods, memory_usage, color=['green', 'blue', 'orange'])
plt.ylabel('Peak Memory Usage (KB)')
plt.title('Firmware Update Memory Consumption Comparison')
plt.savefig('memory_consumption_comparison.png')
plt.show()
