
FROM public.ecr.aws/lambda/python:3.10

# Copy your application code to the Lambda task root
COPY ./app ${LAMBDA_TASK_ROOT}
COPY ./langcahin_agent ${LAMBDA_TASK_ROOT}
COPY main.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt .

# Install dependencies into the Lambda task root
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}" --no-cache-dir

# Set the CMD to your Lambda handler (for example: main.handler)
CMD [ "main.handler" ]
