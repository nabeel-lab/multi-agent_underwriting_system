# 🎨 Deploy Your Beautiful Frontend

Your frontend is already built and connected to the backend! Now deploy it.

---

## ⚡ FASTEST: Deploy to Vercel (3 minutes)

### Step 1: Go to Vercel
1. Open: https://vercel.com
2. Click "Sign Up" or "Login" (use GitHub)

### Step 2: Import Your Project
1. Click "Add New..." → "Project"
2. Import: `nabeel-lab/multi-agent_underwriting_system`
3. Configure:
   - **Root Directory**: `front` ← IMPORTANT!
   - **Framework Preset**: Next.js (auto-detected)
   - **Build Command**: `npm run build` (auto-filled)
   - **Output Directory**: `.next` (auto-filled)

### Step 3: Add Environment Variable
Click "Environment Variables" and add:
```
Name: BACKEND_URL
Value: https://underwriting-agent-936988219342.asia-south1.run.app
```

### Step 4: Deploy
1. Click "Deploy"
2. Wait 2-3 minutes
3. Get your URL: `https://your-app.vercel.app`

**DONE! Open the URL and see your beautiful UI!** 🎉

---

## 🎯 What You'll Get

Your Vercel deployment will have:

✅ **Modern Professional UI**
- Gradient backgrounds (blue to purple)
- Glass morphism cards
- Smooth animations
- Mobile responsive
- Dark mode support

✅ **4-Agent Pipeline**
- Animated cards (fade + slide)
- Loading spinners
- Checkmarks on completion
- Color-coded badges

✅ **Beautiful Decision Card**
- Animated circular risk gauge
- Color-coded (green/yellow/red)
- Large premium display
- Confidence badges
- Bias audit summary

✅ **Connected to Real Backend**
- Calls your ADK agents on Cloud Run
- Real XGBoost scoring
- Actual bias detection
- Live data processing

---

## 🧪 Test Your Deployment

After Vercel deploys, test with these profiles:

**Profile 1: Low Risk (Should Approve)**
- Name: Raj Kumar
- Age: 35
- Occupation: Software Engineer
- Income: 80000
- City: Bangalore
- Years: 5
- Claims: 0

**Profile 2: Medium Risk**
- Name: Priya Sharma
- Age: 28
- Occupation: Gig Worker
- Income: 22000
- City: Hyderabad
- Years: 1.5
- Claims: 0

**Profile 3: High Risk**
- Name: Amit Singh
- Age: 24
- Occupation: Gig Worker
- Income: 18000
- City: Indore
- Years: 1
- Claims: 2

---

## 🎤 Your Demo URLs

**Backend (ADK Agents):**
```
https://underwriting-agent-936988219342.asia-south1.run.app
```

**Frontend (Beautiful UI):**
```
https://your-app.vercel.app (you'll get this after Vercel deployment)
```

---

## 🚀 Alternative: Deploy Frontend to Cloud Run

If you prefer everything on Google Cloud:

### In Cloud Shell:
```bash
cd multi-agent_underwriting_system/front

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
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

# Update next.config.mjs for standalone
cat > next.config.mjs << 'EOF'
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  env: {
    BACKEND_URL: process.env.BACKEND_URL || 'https://underwriting-agent-936988219342.asia-south1.run.app'
  }
};

export default nextConfig;
EOF

# Deploy
gcloud run deploy underwriting-frontend \
  --source . \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars BACKEND_URL=https://underwriting-agent-936988219342.asia-south1.run.app \
  --project multiml-agent
```

---

## 📊 Comparison

**Vercel (Recommended):**
- ✅ Faster (3 minutes)
- ✅ Easier (no Dockerfile needed)
- ✅ Auto-deploys on git push
- ✅ Global CDN
- ✅ Free tier generous

**Cloud Run:**
- ✅ Everything on Google Cloud
- ✅ More control
- ✅ Same region as backend (lower latency)
- ⚠️ Requires Dockerfile
- ⚠️ Takes longer (10 minutes)

---

## 🎯 Recommended: Use Vercel

1. Go to vercel.com
2. Import your GitHub repo
3. Set root directory to `front`
4. Add BACKEND_URL environment variable
5. Deploy
6. Done in 3 minutes!

**Your beautiful UI will be live and connected to your ADK backend!** 🚀
