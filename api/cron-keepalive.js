// Vercel Serverless Function for automated background keep-alive ping
export default async function handler(req, res) {
  const backendUrl = process.env.VITE_API_URL || process.env.BACKEND_URL;
  
  if (!backendUrl) {
    return res.status(400).json({ 
      error: 'VITE_API_URL or BACKEND_URL environment variable is not configured on Vercel.' 
    });
  }

  try {
    const healthUrl = `${backendUrl.replace(/\/$/, '')}/health`;
    console.log(`[Vercel Cron] Pinging backend health endpoint: ${healthUrl}`);

    const response = await fetch(healthUrl, {
      method: 'GET',
      headers: {
        'User-Agent': 'Vercel-Cron-KeepAlive/1.0',
      },
    });

    if (response.ok) {
      const data = await response.json();
      console.log(`[Vercel Cron] ✅ Keep-alive ping successful:`, data);
      return res.status(200).json({ 
        success: true, 
        timestamp: new Date().toISOString(), 
        backend: healthUrl,
        data 
      });
    } else {
      console.warn(`[Vercel Cron] ⚠️ Keep-alive ping returned status ${response.status}`);
      return res.status(response.status).json({ 
        success: false, 
        status: response.status, 
        backend: healthUrl 
      });
    }
  } catch (error) {
    console.error(`[Vercel Cron] ❌ Keep-alive ping failed:`, error);
    return res.status(500).json({ 
      success: false, 
      error: error.message 
    });
  }
}
