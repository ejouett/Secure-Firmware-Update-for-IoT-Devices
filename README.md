# Secure-Firmware-Update-for-IoT-Devices
Comp 445 project
run sign2.py to generate firmware.sig, private_key.pem, public_key.pem, firmware.bin
If it returns successfully in the terminal, move on. Test the firmware signature next by running
verify_firmware.py. If it returns successfully on the terminal, continue.
Create cert.pem and key.pem for HTTPS server.
Run https_server.py the click on the link in the terminal to see the port with my directory
In a search engine.
Download the files from HTTPS and verify their signatures and hashes. If everything is verified
by the compiled verifier, then continue with the firmware update.
