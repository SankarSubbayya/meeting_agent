import { GraphQLServerConfig, OperationContext } from '@wundergraph/sdk';

const config: GraphQLServerConfig = {
  hooks: {
    preResolve: async (ctx: OperationContext, input: any) => {
      // Add custom logic here if needed
      return input;
    },
    postResolve: async (ctx: OperationContext, output: any) => {
      // Add custom logic here if needed
      return output;
    },
    mutatingPreResolve: async (ctx: OperationContext, input: any) => {
      return input;
    },
    mutatingPostResolve: async (ctx: OperationContext, output: any) => {
      return output;
    },
  },
  queryValidationRules: [],
};

export default config;
