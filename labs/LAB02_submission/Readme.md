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
[PUT YOUR DOCKER RUN COMMAND FOR INFERENCE API CONTAINER HERE]
```

### Preprocessor Container
```bash
[PUT YOUR DOCKER RUN COMMAND FOR PREPROCESSOR CONTAINER HERE]
```

## Brief Explanation: How the Containers Communicate
[Write 3-6 sentences here.]

Points to cover:
- Which container calls which endpoint.
- How the preprocessor knows where to find the inference API.
- How images and logs persist using mounted host folders.
- Why `localhost` can be tricky inside containers.

