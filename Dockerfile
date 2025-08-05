# metadata
LABEL \
    org.opencontainers.image.title="{#title}" \
    org.opencontainers.image.version="{#version}" \
    org.opencontainers.image.description="Customized container for running process bigraph experiments with the following dependencies: {#dep_list}" \
    org.opencontainers.image.url="http://github.com/biosimulators/bsew" \
    org.opencontainers.image.documentation="http://github.com/biosimulators/bsew" \
    org.opencontainers.image.source="http://github.com/biosimulators/bsew" \
    org.opencontainers.image.authors="BioSimulators Team <info@biosimulators.org>" \
    org.opencontainers.image.vendor="BioSimulators Team" \
    org.opencontainers.image.licenses="MIT" \
    \
    base_image="ubuntu:nobel" \
    version="{#version}" \
    software="BioSimulators Execution Wrapper" \
    software.version="${SIMULATOR_VERSION}" \
    about.summary="Customized container for running process bigraph experiments with the following dependencies: {#dep_list}" \
    about.home="http://github.com/biosimulators/bsew" \
    about.documentation="http://github.com/biosimulators/bsew" \
    about.license_file="http://github.com/biosimulators/bsew/blob/master/license.txt" \
    about.license="SPDX:MIT" \
    about.tags="dynamical simulation,systems biology" \
    maintainer="BioSimulators Team <info@biosimulators.org>"

#from nixos
from ubuntu:nobel

RUN apt update
RUN apt upgrade -y
RUN apt install python3.11 python-pip

## Dependency Installs
RUN python3 -m pip install git+https://github.com/biosimulators/bspil-basico.git@initial_work

##
RUN mkdir /runtime
RUN cd /runtime
RUN git clone https://github.com/biosimulators/bsew.git  /runtime

ENTRYPOINT ["python3", "/runtime/main.py"]

