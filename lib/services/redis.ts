import { createClient } from 'redis';
import { ActionItem } from './claude';

let client: ReturnType<typeof createClient> | null = null;

async function getClient() {
  if (!client) {
    client = createClient({
      url: process.env.REDIS_URL || 'redis://localhost:6379',
    });
    await client.connect();
  }
  return client;
}

export async function cacheMeetingData(
  jobId: string,
  data: {
    transcript: string;
    actions: ActionItem[];
    emailResults: any[];
  }
) {
  try {
    const redis = await getClient();
    await redis.set(
      `meeting:${jobId}`,
      JSON.stringify({
        ...data,
        createdAt: new Date().toISOString(),
      }),
      {
        EX: 86400, // 24 hour TTL
      }
    );
    console.log(`[Redis] Cached meeting ${jobId}`);
  } catch (error) {
    console.error('Redis cache error:', error);
    // Don't throw - caching is optional
  }
}

export async function getMeetingData(jobId: string) {
  try {
    const redis = await getClient();
    const data = await redis.get(`meeting:${jobId}`);
    return data ? JSON.parse(data) : null;
  } catch (error) {
    console.error('Redis get error:', error);
    return null;
  }
}

export async function closeConnection() {
  if (client) {
    await client.quit();
    client = null;
  }
}
