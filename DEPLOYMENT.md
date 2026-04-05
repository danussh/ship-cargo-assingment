# Deployment Guide

This guide provides step-by-step instructions for deploying the ShipIQ Cargo Optimization Service to various cloud platforms.

## 🚀 Quick Deploy Options

### Railway (Easiest - Recommended for Demo)

Railway provides the simplest deployment with automatic HTTPS and zero configuration.

**Steps:**

1. **Sign up** at [railway.app](https://railway.app)

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your repository
   - Select the `shipiq` repository

3. **Configure Environment Variables** (Optional)
   ```
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   MAX_CARGO_COUNT=10000
   MAX_TANK_COUNT=10000
   ```

4. **Deploy**
   - Railway automatically detects the Dockerfile
   - Build and deployment start automatically
   - Get your live URL: `https://your-app.railway.app`

5. **Test**
   ```bash
   curl https://your-app.railway.app/api/v1/health
   ```

**Estimated Time:** 5 minutes  
**Cost:** Free tier available (500 hours/month)

---

### Render

Render offers similar simplicity with good free tier options.

**Steps:**

1. **Sign up** at [render.com](https://render.com)

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `shipiq` repository

3. **Configure Service**
   - **Name:** shipiq-cargo-optimizer
   - **Region:** Choose closest to your users
   - **Branch:** main
   - **Runtime:** Docker
   - **Instance Type:** Free (or paid for production)

4. **Environment Variables**
   ```
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   PORT=8000
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build and deployment
   - Access at: `https://shipiq-cargo-optimizer.onrender.com`

**Estimated Time:** 10 minutes  
**Cost:** Free tier available

---

### Heroku

Classic platform with simple deployment process.

**Steps:**

1. **Install Heroku CLI**
   ```bash
   brew install heroku/brew/heroku  # macOS
   # or download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create shipiq-cargo-optimizer
   ```

3. **Set Stack to Container**
   ```bash
   heroku stack:set container -a shipiq-cargo-optimizer
   ```

4. **Create heroku.yml**
   ```yaml
   build:
     docker:
       web: Dockerfile
   run:
     web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Set Environment Variables**
   ```bash
   heroku config:set ENVIRONMENT=production -a shipiq-cargo-optimizer
   heroku config:set LOG_LEVEL=INFO -a shipiq-cargo-optimizer
   ```

7. **Open App**
   ```bash
   heroku open -a shipiq-cargo-optimizer
   ```

**Estimated Time:** 15 minutes  
**Cost:** Free tier available (limited hours)

---

### AWS ECS Fargate

Enterprise-grade deployment with full control.

**Prerequisites:**
- AWS Account
- AWS CLI installed and configured
- Docker installed locally

**Steps:**

1. **Create ECR Repository**
   ```bash
   aws ecr create-repository --repository-name shipiq-cargo-optimizer --region us-east-1
   ```

2. **Build and Push Docker Image**
   ```bash
   # Get ECR login
   aws ecr get-login-password --region us-east-1 | \
     docker login --username AWS --password-stdin \
     <account-id>.dkr.ecr.us-east-1.amazonaws.com

   # Build image
   docker build -t shipiq-cargo-optimizer .

   # Tag image
   docker tag shipiq-cargo-optimizer:latest \
     <account-id>.dkr.ecr.us-east-1.amazonaws.com/shipiq-cargo-optimizer:latest

   # Push to ECR
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/shipiq-cargo-optimizer:latest
   ```

3. **Create ECS Cluster**
   ```bash
   aws ecs create-cluster --cluster-name shipiq-cluster --region us-east-1
   ```

4. **Create Task Definition**
   
   Create `task-definition.json`:
   ```json
   {
     "family": "shipiq-cargo-optimizer",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "256",
     "memory": "512",
     "containerDefinitions": [
       {
         "name": "shipiq-api",
         "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/shipiq-cargo-optimizer:latest",
         "portMappings": [
           {
             "containerPort": 8000,
             "protocol": "tcp"
           }
         ],
         "environment": [
           {"name": "ENVIRONMENT", "value": "production"},
           {"name": "LOG_LEVEL", "value": "INFO"}
         ],
         "logConfiguration": {
           "logDriver": "awslogs",
           "options": {
             "awslogs-group": "/ecs/shipiq",
             "awslogs-region": "us-east-1",
             "awslogs-stream-prefix": "ecs"
           }
         }
       }
     ]
   }
   ```

   Register task:
   ```bash
   aws ecs register-task-definition --cli-input-json file://task-definition.json
   ```

5. **Create Service with Load Balancer**
   - Use AWS Console to create Application Load Balancer
   - Create ECS Service pointing to the task definition
   - Configure target group for port 8000
   - Set desired count to 2 for high availability

6. **Access Application**
   - Get ALB DNS name from AWS Console
   - Access at: `http://<alb-dns-name>/api/v1/health`

**Estimated Time:** 30-45 minutes  
**Cost:** Pay-as-you-go (estimate $10-30/month for small workload)

---

### Google Cloud Run

Serverless container deployment with automatic scaling.

**Prerequisites:**
- Google Cloud account
- gcloud CLI installed

**Steps:**

1. **Set Project**
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Enable APIs**
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   ```

3. **Build and Deploy**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/shipiq-cargo-optimizer
   
   gcloud run deploy shipiq-cargo-optimizer \
     --image gcr.io/YOUR_PROJECT_ID/shipiq-cargo-optimizer \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars ENVIRONMENT=production,LOG_LEVEL=INFO
   ```

4. **Get URL**
   ```bash
   gcloud run services describe shipiq-cargo-optimizer \
     --platform managed \
     --region us-central1 \
     --format 'value(status.url)'
   ```

**Estimated Time:** 15 minutes  
**Cost:** Free tier available, then pay-per-use

---

### Azure Container Instances

Simple container deployment on Azure.

**Prerequisites:**
- Azure account
- Azure CLI installed

**Steps:**

1. **Login and Create Resource Group**
   ```bash
   az login
   az group create --name shipiq-rg --location eastus
   ```

2. **Create Container Registry**
   ```bash
   az acr create --resource-group shipiq-rg \
     --name shipiqregistry --sku Basic
   ```

3. **Build and Push**
   ```bash
   az acr build --registry shipiqregistry \
     --image shipiq-cargo-optimizer:latest .
   ```

4. **Deploy Container**
   ```bash
   az container create \
     --resource-group shipiq-rg \
     --name shipiq-cargo-optimizer \
     --image shipiqregistry.azurecr.io/shipiq-cargo-optimizer:latest \
     --dns-name-label shipiq-cargo-optimizer \
     --ports 8000 \
     --environment-variables ENVIRONMENT=production LOG_LEVEL=INFO
   ```

5. **Get URL**
   ```bash
   az container show \
     --resource-group shipiq-rg \
     --name shipiq-cargo-optimizer \
     --query ipAddress.fqdn
   ```

**Estimated Time:** 20 minutes  
**Cost:** Pay-as-you-go

---

## 🔒 Production Checklist

Before deploying to production, ensure:

- [ ] **Environment Variables Set**
  - `ENVIRONMENT=production`
  - `LOG_LEVEL=INFO` or `WARNING`
  - Resource limits configured

- [ ] **Security**
  - HTTPS enabled (most platforms do this automatically)
  - CORS configured for specific origins
  - Rate limiting considered
  - API authentication if needed

- [ ] **Monitoring**
  - Health check endpoint configured
  - Logging enabled
  - Error tracking (Sentry, etc.)
  - Uptime monitoring

- [ ] **Performance**
  - Resource limits appropriate for load
  - Auto-scaling configured
  - Database/cache if needed for large scale

- [ ] **Documentation**
  - API documentation accessible
  - Deployment runbook created
  - Incident response plan

---

## 🧪 Testing Deployment

After deployment, test with:

```bash
# Replace with your deployed URL
export API_URL="https://your-app.railway.app"

# Health check
curl $API_URL/api/v1/health

# Sample optimization
curl -X POST $API_URL/api/v1/optimize/sample

# Custom optimization
curl -X POST $API_URL/api/v1/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "cargos": [{"id": "C1", "volume": 1234}],
    "tanks": [{"id": "T1", "capacity": 5000}]
  }'
```

---

## 📊 Monitoring

### Health Check Endpoint

```bash
GET /api/v1/health
```

Returns:
- `status`: "healthy" if service is running
- `version`: API version
- `environment`: Current environment
- `timestamp`: Current server time

### Logging

Application logs include:
- Request/response logging
- Optimization metrics
- Error tracking
- Performance metrics

Access logs through your platform's logging interface.

---

## 🔄 CI/CD Setup

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Railway

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Railway
        run: npm i -g @railway/cli
      
      - name: Deploy to Railway
        run: railway up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

---

## 🆘 Troubleshooting

### Container Won't Start

- Check logs for errors
- Verify environment variables
- Ensure port 8000 is exposed
- Check health check configuration

### High Memory Usage

- Reduce MAX_CARGO_COUNT and MAX_TANK_COUNT
- Implement request size limits
- Add caching layer

### Slow Response Times

- Check dataset size
- Consider batch processing for large optimizations
- Add database for result caching
- Scale horizontally

---

## 📞 Support

For deployment issues, check:
1. Application logs
2. Platform-specific documentation
3. GitHub issues
4. Contact support

---

**Happy Deploying! 🚀**
