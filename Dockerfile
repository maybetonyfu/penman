FROM python:3.6.6-stretch
WORKDIR /root
COPY main.py main.py
RUN pip install --upgrade pip
RUN pip install pyinstaller
RUN pip install mistune
CMD ["bash", "-c", "pyinstaller --onefile main.py"]

