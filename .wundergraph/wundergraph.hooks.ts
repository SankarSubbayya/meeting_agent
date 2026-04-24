import { HooksConfiguration } from '@wundergraph/sdk';

const hooks: HooksConfiguration = {
  global: {
    httpTransport: {
      onRequest: async (request, _operationName) => {
        // Add global headers if needed
        return request;
      },
    },
  },
  authentication: {
    postAuthentication: async (_input) => {
      // Handle post-authentication logic
      return _input;
    },
  },
};

export default hooks;
