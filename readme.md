# Statistics Survey for UM 2024

## Instructions
### Build it in docker
```docker build -t statsurvey .```

### Run it in docker
```docker run -d -p 5000:5000 --name statsurvey -v ./database:/database statsurvey```