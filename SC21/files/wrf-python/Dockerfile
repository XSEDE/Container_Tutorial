FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "wrfpython", "/bin/bash", "-c"]
RUN echo "Make sure matplotlib is installed:"
RUN python -c "import matplotlib.pyplot"

# COPY wrf-plot-sample.py .
# ENTRYPOINT ["conda", "run", "-n", "containergateway", "python", "wrf-plot-sample.py"]

# COPY wrf-output-plot.png .