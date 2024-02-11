# Basic setup
FROM python:3.11-slim-bookworm

# Update and install necessary packages
RUN apt-get update && apt-get -y update
# added vim and nano for convenience
RUN apt-get install -y sudo git npm vim nano curl wget

# Setup a non-root user 'autogen' with sudo access
RUN adduser --disabled-password --gecos '' autogen
RUN adduser autogen sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER autogen
WORKDIR /home/autogen

# Set environment variable
# ENV OPENAI_API_KEY="{OpenAI-API-Key}"

# Clone the AutoGen repository
RUN git clone -b autogenstudio https://github.com/microsoft/autogen.git /home/autogen/autogen
WORKDIR /home/autogen/autogen

# Install pre-commit hooks
RUN sudo pip install pre-commit
RUN pre-commit install

# Install autogenstudio in editable mode
RUN cd samples/apps/autogen-studio
RUN sudo pip install -e .

# Setup Yarn for the frontend
RUN sudo npm install --global yarn
RUN cd samples/apps/autogen-studio/frontend
RUN yarn install --frozen-lockfile

# Exposes ports for frontend and backend
EXPOSE 8000
EXPOSE 8081

WORKDIR /home/autogen/autogen/samples/apps/autogen-studio

# Set the default command to bash
CMD ["/bin/bash"]
