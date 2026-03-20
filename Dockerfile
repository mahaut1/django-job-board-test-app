FROM python:3.14
WORKDIR /app
#Upgrade pip
RUN pip install --upgrade pip
#Copy the requirements file
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["sh","-c", "python manage.py runserver 0.0.0.0:8000"]

