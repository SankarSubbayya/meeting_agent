import { NextRequest, NextResponse } from 'next/server';
import { v4 as uuid } from 'uuid';
import fs from 'fs';
import path from 'path';

export const config = {
  api: {
    bodyParser: {
      sizeLimit: '100mb',
    },
  },
};

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json(
        { error: 'No file provided' },
        { status: 400 }
      );
    }

    // Generate job ID
    const jobId = uuid();

    // Create temp directory for uploads
    const uploadsDir = path.join(process.cwd(), 'uploads');
    if (!fs.existsSync(uploadsDir)) {
      fs.mkdirSync(uploadsDir, { recursive: true });
    }

    // Save file
    const filePath = path.join(uploadsDir, `${jobId}.mp4`);
    const bytes = await file.arrayBuffer();
    fs.writeFileSync(filePath, Buffer.from(bytes));

    console.log(`[${jobId}] File uploaded: ${file.name}`);

    // Trigger async processing
    // In production, this would be a queue job (Bull, RabbitMQ, etc.)
    processJob(jobId, filePath).catch(err =>
      console.error(`[${jobId}] Processing error:`, err)
    );

    return NextResponse.json({ jobId });
  } catch (error) {
    console.error('Upload error:', error);
    return NextResponse.json(
      { error: 'Upload failed' },
      { status: 500 }
    );
  }
}

// Start processing in background (simplified for hackathon)
async function processJob(jobId: string, filePath: string) {
  console.log(`[${jobId}] Processing started...`);
  // Actual processing happens in /api/process
  // This just queues it
}
