# Lab 2 Submission README

## Student Information
- Name: Matt Tonks
- Date: 2026-03-19

## Deliverables Included
- `inference_api/Dockerfile`
- `preprocessor/Dockerfile`
- `inference_api/app.py` (with `/health` and `/stats`)
- `sample_classifications_20.jsonl` (first 20 lines from logs)
- `Reflection.md`

## Docker Build Commands Used

### Volume creation
```bash
docker volume create mydata
```

### Inference API
```bash
docker build -t inference-app .
```

### Preprocessor
```bash
docker build -t preprocessor-app .
```

## Docker Run Commands Used

### Inference API Container
```bash
docker run -d --name inference-api -p 8000:8000 -v $(pwd)/logs:/logs inference-app
```

### Preprocessor Container
```bash
docker run -d --name preprocessor -v $(pwd)/incoming:/incoming -e API_URL=http://host.docker.internal:8000 preprocessor-app
```

## Brief Explanation: How the Containers Communicate
The preprocessor container monitors the `/incoming` volume for new images. When it finds one, it parses the filename and sends the image as a POST request to the inference API's `/predict` endpoint. The preprocessor finds the API using the `API_URL` environment variable, which is set to `http://host.docker.internal:8000` to reach the host's port 8000 from within the container. Images and logs persist across container restarts because they are stored in mounted host folders (`incoming/` and `logs/`). `localhost` inside a container refers to the container itself, so `host.docker.internal` is used on macOS/Windows to reach the host machine and access the mapped port of the API container.

