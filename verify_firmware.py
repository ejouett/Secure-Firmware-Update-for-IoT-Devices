from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Load public key
with open("firmware_verifier/public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# Load firmware and signature
with open("firmware_verifier/firmware.bin", "rb") as f:
    firmware_data = f.read()
with open("firmware_verifier/signature.bin", "rb") as f:
    signature = f.read()

# Verify firmware
try:
    public_key.verify(
        signature,
        firmware_data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    print("✅ Firmware signature verified successfully!")
except Exception as e:
    print(f"❌ Verification failed: {e}")
