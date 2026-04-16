#!/bin/bash
# Transfer metadata for Container 194 (Manuscript Collection No. 1054) as a test

echo "Starting test transfer for Container 194 (12 disk images)"
echo "This will transfer metadata only, organized in PID-based folders"
echo "============================================================"

# Run the transfer with specific filters for this collection
# Requires: FEDORA_PASSWORD, FEDORA_URL, LIBSAFE_GO_API_URL, LIBSAFE_GO_API_KEY (see transfer_to_libsafego.py)
python transfer_to_libsafego.py \
    --fedora-password "${FEDORA_PASSWORD:?Set FEDORA_PASSWORD in the environment}" \
    --no-ssl-verify \
    --metadata-only \
    --use-pid-folders \
    --output container_194_transfer.csv \
    --skip-existing-metadata 2>&1 | grep -E "emory:(fkcdd|rg99w|ghzrf|ghzq9|ghzp5|ghzsk|ghztq|rg2md|rg2pp|rg2qt|rg2rz|rg2zs)|Processing|Total|Transferred|Skipped|Errors|^="

echo ""
echo "Transfer complete! Check container_194_transfer.csv for details"
