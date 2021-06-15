FROM bde2020/spark-submit:3.1.1-hadoop3.2

WORKDIR /tmp

# Flask env
ENV FLASK_ENV=development
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0

# Install git
RUN apk update && apk add git

# Python dependencies
RUN apk update && \
    apk add python3-dev gcc libc-dev libffi-dev

# Update pip
RUN python3 -m pip install --upgrade pip

# App requirements
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Dev requirements
COPY requirements-dev.txt requirements-dev.txt
RUN pip3 install --no-cache-dir -r requirements-dev.txt

# Dev user and workspace parameters
ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG WORKSPACE=/flask

# Create dev user
RUN addgroup --gid $USER_GID $USERNAME && \
    adduser --uid $USER_UID --ingroup $USERNAME --gecos '' --disabled-password --home /home/$USERNAME $USERNAME

# Workspace
RUN mkdir ${WORKSPACE} && chown -R ${USER_UID}:${USER_GID} ${WORKSPACE}
WORKDIR ${WORKSPACE}
RUN apk add alpine-sdk

EXPOSE 5000
CMD ["/bin/bash"]