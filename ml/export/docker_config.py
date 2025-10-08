"""
Docker Compose Configuration Generator
"""

# Docker Compose for TensorFlow Serving
DOCKER_COMPOSE_SERVING = """
version: '3.8'

services:
  tf-serving:
    image: tensorflow/serving:latest
    ports:
      - "8501:8501"  # REST API
      - "8500:8500"  # gRPC
    volumes:
      - ./models:/models
    environment:
      - MODEL_NAME=plant_disease_model
      - MODEL_BASE_PATH=/models/plant_disease
    command: 
      - "--model_config_file=/models/plant_disease/models.config"
      - "--model_config_file_poll_wait_seconds=60"
"""


def create_docker_compose(output_path: str = 'docker-compose.serving.yml'):
    """Create Docker Compose file for TensorFlow Serving"""
    with open(output_path, 'w') as f:
        f.write(DOCKER_COMPOSE_SERVING)
    print(f"Docker Compose file created: {output_path}")