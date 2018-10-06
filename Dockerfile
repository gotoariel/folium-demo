FROM heroku/miniconda

ADD ./tracker/webapp-env.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml

RUN echo "conda activate $(head -1 /tmp/environment.yml | cut -d' ' -f2)" > ~/.bashrc
