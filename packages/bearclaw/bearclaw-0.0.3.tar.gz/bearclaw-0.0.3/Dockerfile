# For more information, please refer to https://aka.ms/vscode-docker-python
FROM registry.gitlab.com/hylkedonker/bearclaw/grch37 as BUILD

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt update && apt install --assume-yes python3-venv
RUN pip3 install build
COPY . /opt/bearclaw/
WORKDIR /opt/bearclaw/
RUN python3 -m build && pip3 install --user .


FROM registry.gitlab.com/hylkedonker/bearclaw/grch37
COPY --from=BUILD /root/.local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/dist-packages/

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
