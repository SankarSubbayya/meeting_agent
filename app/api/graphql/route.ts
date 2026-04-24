import { NextRequest, NextResponse } from 'next/server';

// Simple GraphQL query executor that calls the operations
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { query, variables } = body;

    // Parse the GraphQL query to determine which operation to call
    if (query.includes('GetMeeting') && !query.includes('GetMeetings')) {
      // Single meeting query
      const jobId = variables?.jobId;
      const response = await fetch(`http://localhost:8000/api/meeting/${jobId}`);
      const data = await response.json();
      return NextResponse.json({
        data: { meeting: data }
      });
    }

    if (query.includes('GetMeetings')) {
      // List meetings query
      const response = await fetch('http://localhost:8000/api/meetings');
      const data = await response.json();
      return NextResponse.json({
        data: { meetings: data }
      });
    }

    if (query.includes('GetStatus')) {
      // Status query
      const jobId = variables?.jobId;
      const response = await fetch(`http://localhost:8000/api/status/${jobId}`);
      const data = await response.json();
      return NextResponse.json({
        data: { status: data }
      });
    }

    return NextResponse.json({
      errors: [{ message: 'Unknown query' }]
    }, { status: 400 });

  } catch (error) {
    console.error('GraphQL error:', error);
    return NextResponse.json({
      errors: [{ message: error instanceof Error ? error.message : 'Unknown error' }]
    }, { status: 500 });
  }
}

// GraphQL endpoint info
export async function GET(request: NextRequest) {
  return NextResponse.json({
    message: 'GraphQL endpoint',
    url: '/api/graphql',
    methods: ['POST'],
    operations: ['GetMeeting', 'GetMeetings', 'GetStatus', 'UploadMeeting']
  });
}
