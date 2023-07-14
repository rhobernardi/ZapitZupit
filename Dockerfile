FROM python:3.10

LABEL org.label-schema.license="GPL-3.0" \
	org.label-schema.vcs-url="https://github.com/rhobernardi" \
	org.label-schema.vendor="ZapitZupit Project" \
	maintainer="Rodrigo Bernardi"

ADD zapitzupit.py requirements.txt ImageReaderAI.py log.py ./

RUN mkdir -p /log/
RUN mkdir -p /img/

RUN apt-get update \
	&& apt-get -y install tesseract-ocr libgl1-mesa-glx
RUN pip install -r requirements.txt

CMD ["python", "zapitzupit.py"]