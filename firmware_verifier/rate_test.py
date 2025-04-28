# update_time_overhead_test.py

import time
import subprocess
import requests

# URL of your HTTPS firmware server
FIRMWARE_URL = "https://localhost:8443/"  # Adjust if needed

def insecure_update():
    start = time.time()
    response = requests.get(FIRMWARE_URL, verify=False)
    if response.status_code == 200:
        with open("firmware.bin", "wb") as f:
            f.write(response.content)
    end = time.time()
    return end - start

def secure_update():
    start = time.time()
    response = requests.get(FIRMWARE_URL, verify=False)
    if response.status_code == 200:
        with open("firmware.bin", "wb") as f:
            f.write(response.content)
    # Now verify
    subprocess.run(["./verifier", "firmware.bin", "signature.bin", "public_key.pem"],
                   capture_output=True, text=True)
    end = time.time()
    return end - start

# Run multiple times and average
NUM_RUNS = 30
insecure_times = []
secure_times = []

for _ in range(NUM_RUNS):
    insecure_times.append(insecure_update())
    secure_times.append(secure_update())

# Plot results
import matplotlib.pyplot as plt

plt.plot(insecure_times, label='Insecure Update Time (Download Only)', marker='o')
plt.plot(secure_times, label='Secure Update Time (Download + Verify)', marker='x')
plt.title('Firmware Update Time: Insecure vs Secure')
plt.xlabel('Run')
plt.ylabel('Time (seconds)')
plt.legend()
plt.savefig('update_time_overhead.png')
plt.show()

print(f"Average Insecure Update Time: {sum(insecure_times)/NUM_RUNS:.4f} s")
print(f"Average Secure Update Time: {sum(secure_times)/NUM_RUNS:.4f} s")

