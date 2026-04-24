import { configureWunderGraphApplication, cors } from '@wundergraph/sdk';
import server from './wundergraph.server';
import operations from './operations';

const config = configureWunderGraphApplication({
  server,
  operations,
  cors: {
    ...cors.allowAll,
  },
  security: {
    enableGraphQLEndpoint: true,
  },
});

export default config;
