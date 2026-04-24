import { NextRequest, NextResponse } from 'next/server';
import { randomUUID } from 'crypto';
import fs from 'fs';
import path from 'path';
import { transcribeAudio } from '../../../../lib/services/vapi';
import { extractActions } from '../../../../lib/services/claude';
import { sendActionEmails } from '../../../../lib/services/email';
import {
  cacheMeetingData,
  setMeetingStatus,
} from '../../../../lib/services/redis';

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

    const jobId = randomUUID();

    const uploadsDir = path.join(process.cwd(), 'uploads');
    if (!fs.existsSync(uploadsDir)) {
      fs.mkdirSync(uploadsDir, { recursive: true });
    }

    const filePath = path.join(uploadsDir, `${jobId}.mp4`);
    const bytes = await file.arrayBuffer();
    await fs.promises.writeFile(filePath, Buffer.from(bytes));

    console.log(`[${jobId}] File uploaded: ${file.name}`);
    await setMeetingStatus(jobId, 'uploaded');

    processJob(jobId, filePath).catch((err) =>
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

async function processJob(jobId: string, filePath: string) {
  try {
    await setMeetingStatus(jobId, 'transcribing');
    const transcript = await transcribeAudio(filePath);

    await setMeetingStatus(jobId, 'extracting');
    const actions = await extractActions(transcript);

    await setMeetingStatus(jobId, 'emailing');
    const emailResults = await sendActionEmails(actions, jobId);

    await cacheMeetingData(jobId, {
      transcript,
      actions,
      emailResults,
    });

    await setMeetingStatus(jobId, 'completed');
    console.log(`[${jobId}] Processing complete`);
  } catch (error) {
    console.error(`[${jobId}] Processing failed:`, error);
    await setMeetingStatus(jobId, 'failed');
  }
}
