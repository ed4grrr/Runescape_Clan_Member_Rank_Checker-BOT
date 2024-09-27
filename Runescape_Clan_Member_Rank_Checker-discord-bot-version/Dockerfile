# Step 1: Use an official Python runtime as a base image
FROM python:3.10-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements file to the working directory
COPY requirements.txt .

# Step 4: Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the app’s source code to the container
COPY . .

# Step 7: Command to run the bot when the container starts
CMD [ "python", "./RS_USER_HIGHSCORE_API.py" ]