#!/bin/bash
# Register qemu-*-static for all supported processors except the 
# current one, but also remove all registered binfmt_misc before
docker run --rm --privileged multiarch/qemu-user-static:register --reset