import { configureWunderGraphApplication, cors, EnvironmentVariable } from '@wundergraph/sdk';
import server from './wundergraph.server';
import operations from './operations';

const config = configureWunderGraphApplication({
  server,
  operations,
  cors: {
    ...cors.allowAll,
  },
  security: {
    enableGraphQLEndpoint: process.env.NODE_ENV !== 'production',
    enableIntrospection: true,
  },
});

export default config;
