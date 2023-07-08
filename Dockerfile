FROM python:3.10

LABEL org.label-schema.license="GPL-3.0" \
	org.label-schema.vcs-url="https://github.com/rhobernardi" \
	org.label-schema.vendor="ZapitZupit Project" \
	maintainer="Rodrigo Bernardi"

ADD zapitzupit.py requirements.txt setup.py ./

RUN apt-get update \
	&& apt-get -y install tesseract-ocr
RUN pip install -r requirements.txt
RUN python setup.py

CMD ["python", "zapitzupit.py"]
