#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "mbedtls/pk.h"
#include "mbedtls/md.h"

#define FIRMWARE_PATH "firmware.bin"
#define SIGNATURE_PATH "signature.bin"
#define PUBLIC_KEY_PATH "public_key.pem"

#define BUFFER_SIZE 4096

int main() {
    FILE *fw = fopen(FIRMWARE_PATH, "rb");
    FILE *sig = fopen(SIGNATURE_PATH, "rb");
    FILE *pub = fopen(PUBLIC_KEY_PATH, "rb");

    if (!fw || !sig || !pub) {
        printf("❌ Failed to open files.\n");
        return 1;
    }

    // Load firmware into buffer
    fseek(fw, 0, SEEK_END);
    size_t fw_size = ftell(fw);
    rewind(fw);
    unsigned char *firmware = malloc(fw_size);
    fread(firmware, 1, fw_size, fw);

    // Load signature
    fseek(sig, 0, SEEK_END);
    size_t sig_size = ftell(sig);
    rewind(sig);
    unsigned char *signature = malloc(sig_size);
    fread(signature, 1, sig_size, sig);

    // Load public key
    mbedtls_pk_context pk;
    mbedtls_pk_init(&pk);
    if (mbedtls_pk_parse_public_keyfile(&pk, PUBLIC_KEY_PATH) != 0) {
        printf("❌ Failed to parse public key.\n");
        return 1;
    }

    // Compute hash of the firmware
    unsigned char hash[32];
    mbedtls_md(mbedtls_md_info_from_type(MBEDTLS_MD_SHA256), firmware, fw_size, hash);

    // Verify the signature
    int result = mbedtls_pk_verify(
        &pk,
        MBEDTLS_MD_SHA256,
        hash,
        0,
        signature,
        sig_size
    );

    if (result == 0) {
        printf("✅ Signature and integrity check passed. Proceeding with update.\n");
        // Proceed to flash firmware
    } else {
        printf("❌ Firmware verification failed! Rejecting update.\n");
    }

    // Cleanup
    fclose(fw);
    fclose(sig);
    fclose(pub);
    free(firmware);
    free(signature);
    mbedtls_pk_free(&pk);
    return 0;
}
