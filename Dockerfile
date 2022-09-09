FROM python:3.9

WORKDIR /python-docker

COPY requirements.txt char2vec.bin ./

RUN pip3 install -r requirements.txt

RUN git clone https://github.com/facebookresearch/fastText.git && \
    cd fastText && \
    pip install .

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]