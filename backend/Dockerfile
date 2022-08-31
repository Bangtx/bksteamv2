FROM public.ecr.aws/lambda/python:3.9

WORKDIR /app/backend

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.in-project true

# Install serverless for deployment
RUN curl -sL https://rpm.nodesource.com/setup_14.x | bash -
RUN yum install -y nodejs
RUN npm install -g serverless@2
RUN npm install -g serverless-plugin-warmup@6.2.0
RUN npm install -g serverless-python-requirements@5.3.0
RUN npm install -g serverless-domain-manager@5.6.0
RUN yum install -y poppler-utils