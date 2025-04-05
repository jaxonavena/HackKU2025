# 1. Use the base image from the JSON
FROM ubuntu:22.04

# 2. Copy over the generated shell script
COPY install.sh /tmp/install.sh

# 3. Make the script executable, then run it
RUN chmod +x /tmp/install.sh
RUN /tmp/install.sh

# 4. (Optional) set a default command or entrypoint
CMD ["bash"]
