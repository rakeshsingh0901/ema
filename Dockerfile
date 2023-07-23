# Use a Python base image
FROM python:3.7

# Install TA-Lib dependencies (if required)
RUN apt-get update && apt-get install -y build-essential
# Add other dependencies as needed
RUN apt-get -y install gcc build-essential

# Install TA-Lib
# The following commands depend on the distribution you are using and the TA-Lib installation method
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
  && tar -xzf ta-lib-0.4.0-src.tar.gz \
  && rm ta-lib-0.4.0-src.tar.gz \
  && cd ta-lib/ \
  && ./configure --prefix=/usr \
  && make \
  && make install \
  && cd ~ \
  && rm -rf ta-lib/ \
  && pip install ta-lib

# Copy your Python application code to the container
COPY . /app
WORKDIR /app

ENV TZ=Asia/Kolkata

RUN pip install --upgrade pip
# Install Python dependencies
RUN pip install -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn
# Expose the necessary port (if applicable)
EXPOSE 8080

# Command to run your Python application
CMD ["gunicorn", "-b", "0.0.0.0:8000", "--timeout", "0", "trading_bot:application"]
