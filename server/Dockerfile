FROM continuumio/miniconda:latest

WORKDIR /home/ubuntu/app

COPY environment.yml ./
COPY index.py ./
COPY boot.sh ./

RUN chmod +x boot.sh

RUN Conda env create -f environment.yml

RUN echo "source activate your-environment-name" &gt; ~/.bashrc
ENV PATH /opt/conda/envs/your-environment-name/bin:$PATH

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]