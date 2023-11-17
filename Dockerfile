FROM public.ecr.aws/lambda/python:3.11

# Copy the requirements for the project
COPY requirements.txt .

# Install the openssl dependency required for python SDK
RUN yum -y install openssl11

# Install the requirements for the project
RUN pip install -r requirements.txt

# Copy function code to /var/task
COPY *.py ${LAMBDA_TASK_ROOT}/

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
WORKDIR ${LAMBDA_TASK_ROOT}
CMD ["cb_kv_ops.read_document_handler"]