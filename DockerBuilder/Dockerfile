FROM python:3.10-slim
WORKDIR /app
COPY repo/ /app/
COPY install_deps.sh /app/install_deps.sh
RUN chmod +x /app/install_deps.sh && /app/install_deps.sh
EXPOSE 8080
EXPOSE 5000
CMD ["ttyd", "--writable", "-p", "8080", "bash"]
