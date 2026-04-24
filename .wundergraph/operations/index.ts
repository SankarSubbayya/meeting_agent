import { createOperation } from '@wundergraph/sdk';

// Export all operations
export const GetMeeting = createOperation.query({
  handler: async (ctx, input: { jobId: string }) => {
    const response = await fetch(`http://localhost:8000/api/meeting/${input.jobId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch meeting');
    }
    return response.json();
  },
});

export const GetMeetings = createOperation.query({
  handler: async (ctx) => {
    const response = await fetch('http://localhost:8000/api/meetings');
    if (!response.ok) {
      throw new Error('Failed to fetch meetings');
    }
    return response.json();
  },
});

export const GetStatus = createOperation.query({
  handler: async (ctx, input: { jobId: string }) => {
    const response = await fetch(`http://localhost:8000/api/status/${input.jobId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch status');
    }
    return response.json();
  },
});

export const UploadMeeting = createOperation.mutation({
  handler: async (ctx, input: { file: File }) => {
    const formData = new FormData();
    formData.append('file', input.file);

    const response = await fetch('http://localhost:8000/api/upload', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Upload failed');
    }
    return response.json();
  },
});
