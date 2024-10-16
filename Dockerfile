ARG IMAGE_NAME
ARG IMAGE_TAG

FROM $IMAGE_NAME:$IMAGE_TAG

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ARG APP_USER_NAME
ARG APP_UID
ARG APP_GID

#Set the locale
RUN apt update && apt dist-upgrade -y
RUN apt install -y locales libc-bin locales-all
RUN apt-get install -y build-essential libssl-dev libffi-dev python-dev-is-python3 pkg-config libcairo2-dev
RUN apt-get install -y default-mysql-client libmariadb-dev-compat libmariadb-dev 

RUN sed -i '/pt_BR.UTF-8/s/^#//g' /etc/locale.gen \
  && locale-gen en_US en_US.UTF-8 pt_BR pt_BR.UTF-8 \
  && dpkg-reconfigure locales \
  && update-locale LANG=pt_BR.UTF-8 LANGUAGE=pt_BR.UTF-8 LC_ALL=pt_BR.UTF-8
ENV LANG pt_BR.UTF-8  
ENV LANGUAGE pt_BR:pt  
ENV LC_ALL pt_BR.UTF-8
ENV LC_CTYPE pt_BR.UTF-8
ENV LC_TIME pt_BR.UTF-8

# RUN dpkg-reconfigure locales

# pip Update
RUN /usr/local/bin/python -m pip install --upgrade pip

# Install pip requirements
COPY requirements.txt .
RUN pip install wheel
RUN python -m pip install -r requirements.txt -U

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u $APP_UID --disabled-password --gecos "" $APP_USER_NAME && chown -R $APP_USER_NAME /home/$APP_USER_NAME

WORKDIR /home/$APP_USER_NAME
# COPY ./app /home/$APP_USER_NAME

# RUN chown -R $APP_USER_NAME:$APP_USER_NAME /home/$APP_USER_NAME
USER $APP_USER_NAME
# RUN mkdir /home/$APP_USER_NAME/templates
# RUN mkdir /home/$APP_USER_NAME/outputs

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
