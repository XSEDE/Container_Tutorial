FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "containergateway", "/bin/bash", "-c"]

COPY Precipitation_Map.py .
ENTRYPOINT ["conda", "run", "-n", "containergateway", "python", "Precipitation_Map.py"]

COPY nws-1day-precipitation.png .