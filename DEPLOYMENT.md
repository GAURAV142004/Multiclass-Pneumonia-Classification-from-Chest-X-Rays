# Deployment Guide - Pneumonia Detection System

## Prerequisites
- GitHub account with your code pushed
- Email account for service signups

---

## Step 1: Setup MongoDB Atlas (Database)

### 1.1 Create Account
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Sign up with Google or email
3. Choose **FREE** M0 cluster

### 1.2 Create Database Cluster
1. Click **"Build a Database"**
2. Choose **"M0 FREE"** tier
3. Select a cloud provider (AWS recommended) and region close to you
4. Click **"Create Cluster"** (takes 3-5 minutes)

### 1.3 Setup Database Access
1. Click **"Database Access"** in left sidebar
2. Click **"Add New Database User"**
3. Choose **"Password"** authentication
4. Username: `admin` (or your choice)
5. Click **"Autogenerate Secure Password"** - **SAVE THIS PASSWORD**
6. Database User Privileges: **"Read and write to any database"**
7. Click **"Add User"**

### 1.4 Setup Network Access
1. Click **"Network Access"** in left sidebar
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (0.0.0.0/0)
4. Click **"Confirm"**

### 1.5 Get Connection String
1. Click **"Database"** in left sidebar
2. Click **"Connect"** on your cluster
3. Choose **"Connect your application"**
4. Copy the connection string (looks like):
   ```
   mongodb+srv://admin:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
5. Replace `<password>` with your saved password
6. **SAVE THIS CONNECTION STRING** - you'll need it for backend deployment

---

## Step 2: Deploy Backend to Render

### 2.1 Create Render Account
1. Go to [Render](https://render.com/)
2. Sign up with GitHub (recommended for easy deployment)
3. Authorize Render to access your GitHub repositories

### 2.2 Create Web Service
1. From dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Select your project repository
4. Configure the service:
   - **Name**: `pneumonia-detection-backend` (or your choice)
   - **Region**: Choose closest to you
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: **Free**

### 2.3 Add Environment Variables
Click **"Advanced"** and add these environment variables:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `DEBUG` | `False` |
| `SECRET_KEY` | Generate a random 32+ character string |
| `MONGODB_URL` | Your MongoDB Atlas connection string from Step 1.5 |
| `MONGODB_DB_NAME` | `pneumonia_detection` |
| `ALLOWED_ORIGINS` | `https://your-frontend.vercel.app` (add after frontend deployment) |

**Secret Key Generator**: Use this command locally:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2.4 Deploy
1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment (large models take time)
3. Once deployed, copy your backend URL: `https://your-app.onrender.com`
4. **Test it**: Visit `https://your-app.onrender.com/docs` - should see API documentation

---

## Step 3: Deploy Frontend to Vercel

### 3.1 Create Vercel Account
1. Go to [Vercel](https://vercel.com/signup)
2. Sign up with GitHub
3. Authorize Vercel to access repositories

### 3.2 Import Project
1. Click **"Add New..."** → **"Project"**
2. Import your GitHub repository
3. Configure project:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - Click **"Edit"** next to Build settings

### 3.3 Configure Build Settings
1. **Build Command**: `npm run build`
2. **Output Directory**: `dist`
3. **Install Command**: `npm install`

### 3.4 Add Environment Variables
Click **"Environment Variables"** and add:

| Name | Value |
|------|-------|
| `VITE_API_URL` | Your Render backend URL from Step 2.4 |

Example: `https://pneumonia-detection-backend.onrender.com`

### 3.5 Deploy
1. Click **"Deploy"**
2. Wait 2-3 minutes
3. Once deployed, copy your frontend URL: `https://your-app.vercel.app`

---

## Step 4: Final Configuration

### 4.1 Update Backend CORS
1. Go back to Render dashboard
2. Open your backend web service
3. Go to **"Environment"**
4. Update `ALLOWED_ORIGINS` variable:
   ```
   https://your-app.vercel.app,http://localhost:5173
   ```
5. Save changes (backend will auto-redeploy)

### 4.2 Test Your Application
1. Visit your Vercel frontend URL
2. Sign up for a new account
3. Upload a test image
4. Verify the prediction works

---

## Important Notes

### Free Tier Limitations
- **Render Free**: 
  - 750 hours/month
  - Sleeps after 15 min inactivity (30s cold start)
  - 512MB RAM
- **Vercel Free**: 
  - 100GB bandwidth/month
  - Unlimited deployments
- **MongoDB Atlas Free**: 
  - 512MB storage
  - No credit card required

### Cold Start Issue
On Render's free tier, the backend sleeps after inactivity. First request after sleep takes 30-60 seconds. This is normal.

### Model Size Considerations
Your models (~370MB) are at the edge of Render's limits. If deployment fails:
1. Consider using smaller quantized models
2. Upgrade to Render's paid tier ($7/month)
3. Use model compression techniques

---

## Troubleshooting

### Backend won't deploy
- Check Render logs for errors
- Verify all environment variables are set
- Ensure `requirements.txt` is correct

### Frontend can't connect to backend
- Check CORS settings in backend
- Verify `VITE_API_URL` is correct in Vercel
- Check browser console for errors

### Database connection fails
- Verify MongoDB connection string
- Check IP whitelist includes 0.0.0.0/0
- Confirm database user has correct permissions

---

## Updating Your Deployment

### To update code:
1. Push changes to GitHub
2. Vercel and Render automatically redeploy
3. Wait for deployment to complete

### Manual redeploy:
- **Render**: Click "Manual Deploy" → "Deploy latest commit"
- **Vercel**: Click "Deployments" → "Redeploy"

---

## Support & Monitoring

- **Render Logs**: Dashboard → Your Service → Logs
- **Vercel Logs**: Dashboard → Your Project → Deployments → View Function Logs
- **MongoDB Metrics**: Atlas Dashboard → Metrics tab

---

## Next Steps (Optional)

1. **Custom Domain**: Add your own domain in Vercel/Render settings
2. **Analytics**: Add Vercel Analytics or Google Analytics
3. **Error Monitoring**: Integrate Sentry for error tracking
4. **Upgrade**: Consider paid tiers for better performance
