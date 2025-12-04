# ... existing code ...

# Make start script executable
COPY start.sh .
RUN chmod +x start.sh

# Use the start script
CMD ["./start.sh"]