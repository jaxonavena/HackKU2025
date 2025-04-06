FROM python:3.10-slim
WORKDIR /app
COPY repo/ /app/
COPY setup.sh /app/setup.sh
RUN chmod +x /app/setup.sh && /app/setup.sh
EXPOSE 8080
CMD ["ttyd", "--writable", "-p", "8080", "bash"]
