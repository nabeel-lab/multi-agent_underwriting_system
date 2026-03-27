# Deploy Frontend to Vercel

Your beautiful Next.js frontend is ready! Here's how to deploy it:

## Option 1: Deploy to Vercel (Recommended - 5 minutes)

### Step 1: Push Frontend to GitHub
```bash
# Already done - your code is on GitHub!
```

### Step 2: Deploy to Vercel
1. Go to https://vercel.com
2. Sign in with GitHub
3. Click "New Project"
4. Import your repo: `nabeel-lab/multi-agent_underwriting_system`
5. Configure:
   - **Root Directory**: `front`
   - **Framework Preset**: Next.js
   - **Environment Variables**: Add this:
     ```
     BACKEND_URL=https://underwriting-agent-936988219342.asia-south1.run.app
     ```
6. Click "Deploy"

**Wait 2-3 minutes** → You'll get a live URL like: `https://your-app.vercel.app`

---

## Option 2: Run Frontend Locally (For Testing)

### In your Windows machine:
```bash
cd front
npm install
npm run dev
```

Open: http://localhost:3000

---

## Option 3: Deploy Frontend to Cloud Run (Advanced)

### Step 1: Create Dockerfile for Frontend
```bash
cat > front/Dockerfile << 'EOF'
FROM node:20-alpine AS base

# Install dependencies
FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci

# Build
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production
FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
ENV PORT=3000
CMD ["node", "server.js"]
EOF
```

### Step 2: Update next.config.mjs
```bash
cat > front/next.config.mjs << 'EOF'
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  env: {
    BACKEND_URL: process.env.BACKEND_URL || 'https://underwriting-agent-936988219342.asia-south1.run.app'
  }
};

export default nextConfig;
EOF
```

### Step 3: Deploy to Cloud Run
```bash
cd front

# Build and deploy
gcloud run deploy underwriting-frontend \
  --source . \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars BACKEND_URL=https://underwriting-agent-936988219342.asia-south1.run.app
```

---

## What You Get

After deployment, your frontend will have:

✅ **Beautiful Modern UI**
- Gradient backgrounds
- Glass morphism cards
- Smooth animations
- Mobile responsive

✅ **4-Agent Pipeline Visualization**
- Animated agent cards
- Loading states
- Progress indicators

✅ **Decision Card**
- Circular risk gauge
- Approval status
- Premium calculation
- Bias audit summary

✅ **Connected to Your Backend**
- Calls your ADK agents
- Real XGBoost scoring
- Actual bias detection

---

## Testing

After deployment, test with these profiles:

**Low Risk:**
- Name: Raj Kumar
- Age: 35
- Occupation: Software Engineer
- Income: 80000
- City: Bangalore
- Years: 5
- Claims: 0

**Medium Risk:**
- Name: Priya Sharma
- Age: 28
- Occupation: Gig Worker
- Income: 22000
- City: Hyderabad
- Years: 1.5
- Claims: 0

**High Risk:**
- Name: Amit Singh
- Age: 24
- Occupation: Gig Worker
- Income: 18000
- City: Indore
- Years: 1
- Claims: 2

---

## Recommended: Use Vercel

Vercel is the easiest and fastest:
1. Free hosting
2. Automatic deployments on git push
3. Global CDN
4. HTTPS by default
5. Takes 3 minutes

**Go to vercel.com and deploy now!** 🚀
