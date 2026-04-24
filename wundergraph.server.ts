import { configureWunderGraphServer } from '@wundergraph/sdk/server';
import { Application } from '@wundergraph/sdk';

export default configureWunderGraphServer<Application>(() => ({
  // Health check
  hooks: {
    authentication: {
      // Optional: Add auth hooks here
    },
  },
  graphqlServers: [
    {
      serverName: 'meetingAPI',
      // Internal GraphQL endpoint for meeting data
      // Will be populated by Next.js API routes
      apiNamespace: 'meeting',
    },
  ],
}));
