FROM ubuntu:16.04
RUN apt-get update && apt-get install -y libssl-dev libffi-dev python3.5 python3-pip
RUN pip3 install --upgrade pip kubernetes -i https://mirrors.aliyun.com/pypi/simple/
RUN sed -i 's/self.verify_ssl\ =\ True/self.verify_ssl\ =\ False/g' /usr/local/lib/python3.5/dist-packages/kubernetes/client/configuration.py
RUN mkdir -p /workdir
ADD data_backup.py /workdir/data_backup.py
WORKDIR /workdir
CMD ["python3.5", "data_backup.py"]
