FROM mcr.microsoft.com/vscode/devcontainers/python:3.8-bullseye

ENV LANG pt_BR.UTF-8
ENV LC_ALL pt_BR.UTF-8
ENV LANGUAGE pt_BR.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

ARG APP_USER_NAME
ARG APP_UID
ARG APP_GID
ARG APP_NAME

RUN adduser -u $APP_UID --disabled-password --gecos "" $APP_USER_NAME && chown -R $APP_USER_NAME /home/$APP_USER_NAME

RUN apt-get update && apt-get install git -y

RUN pip install pipenv

RUN apt install -y locales libc-bin locales-all
RUN sed -i '/pt_BR.UTF-8/s/^#//g' /etc/locale.gen \
    && locale-gen en_US en_US.UTF-8 pt_BR pt_BR.UTF-8 \
    && dpkg-reconfigure --frontend noninteractive locales \
    && update-locale LANG=pt_BR.UTF-8 LANGUAGE=pt_BR.UTF-8 LC_ALL=pt_BR.UTF-8

ENV PIPENV_VENV_IN_PROJECT=True
ENV PIPENV_SITE_PACKAGES=True
ENV PATH="/home/$APP_USER_NAME/$APP_NAME/.venv/bin:$PATH"

USER $APP_USER_NAME

WORKDIR /home/$APP_USER_NAME/$APP_NAME

CMD [ "tail", "-f", "/dev/null" ]