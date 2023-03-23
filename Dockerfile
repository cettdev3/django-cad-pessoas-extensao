FROM python:3.9-bullseye

ENV LANG pt_BR.UTF-8
ENV LC_ALL pt_BR.UTF-8
ENV LANGUAGE pt_BR.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive

ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt install -y ntpdate
# RUN ntpdate pool.ntp.br
RUN dpkg-reconfigure tzdata
RUN apt install -y locales libc-bin locales-all
RUN apt-get install -y build-essential libssl-dev libffi-dev python-dev
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
RUN adduser -u 1000 --disabled-password --gecos "" appuser && chown -R appuser /home/appuser

WORKDIR /home/appuser
# COPY ./app /home/appuser

# RUN chown -R appuser:appuser /home/appuser
USER appuser
# RUN mkdir /home/appuser/templates
# RUN mkdir /home/appuser/outputs

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
