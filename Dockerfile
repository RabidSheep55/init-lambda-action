# Placeholder image to upload to ecr when initialising the lambda function
FROM public.ecr.aws/lambda/python:3.8

WORKDIR ${LAMBDA_TASK_ROOT}
RUN echo "def handler(e, c): return 'Placeholder Image for Grading/Algorithm Function'" > app.py

CMD ["app.handler"]
