import { NextRequest, NextResponse } from 'next/server';
import {
  getMeetingData,
  getMeetingStatus,
} from '../../../../lib/services/redis';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const jobId = params.id;
  const meetingData = await getMeetingData(jobId);
  if (meetingData) {
    return NextResponse.json({ status: 'done' });
  }

  const status = await getMeetingStatus(jobId);
  if (status) {
    return NextResponse.json({ status });
  }

  return NextResponse.json(
    { error: 'Meeting not found' },
    { status: 404 }
  );
}
