FROM python:3

ADD triton/ /triton/triton/
ADD requirements.txt /triton/
RUN pip install -r /triton/requirements.txt
ENV PYTHONPATH="/triton/"
ENTRYPOINT ["python", "/triton/triton/runner.py"]
CMD []