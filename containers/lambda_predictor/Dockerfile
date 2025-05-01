# Define custom function directory
ARG FUNCTION_DIR="/function"

FROM python:3.11 AS build-image

# Include global arg in this stage of the build
ARG FUNCTION_DIR

# Copy function code
RUN mkdir -p ${FUNCTION_DIR}
COPY . ${FUNCTION_DIR}

# Install the function's dependencies
WORKDIR ${FUNCTION_DIR}
RUN pip install --no-cache-dir --target ${FUNCTION_DIR} -r requirements.txt && \
    pip install --no-cache-dir --target ${FUNCTION_DIR} awslambdaric==3.0.1 && \
    rm -rf ~/.cache/pip

# Use a slim version of the base Python image to reduce the final image size
FROM python:3.11-slim-bookworm

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# Set runtime interface client as default command for the container runtime
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
# Pass the name of the function handler as an argument to the runtime
CMD [ "main.handler" ]