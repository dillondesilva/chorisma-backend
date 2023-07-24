FROM public.ecr.aws/lambda/python:3.8

# Copy requirements.txt
COPY ./app/get_presigned_url_requirements.txt ${LAMBDA_TASK_ROOT}

# Copy function code
COPY ./app/get_presigned_url.py ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r get_presigned_url_requirements.txt

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "get_presigned_url.lambda_handler" ]