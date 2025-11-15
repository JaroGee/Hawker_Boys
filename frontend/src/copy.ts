export const errorTemplates = {
  generic: {
    title: 'Something went wrong.',
    action: 'Please retry in a few seconds.',
    escalate: 'If the issue persists after two tries, contact ops@hawkerboys.sg.'
  },
  ssgSync: {
    title: 'We could not sync with SSG.',
    action: 'Check the SSG Error Catalog for guidance and requeue the job.',
    escalate: 'If the same error repeats three times, email dev@hawkerboys.sg with the correlation ID.'
  },
  authRateLimit: {
    title: 'Too many sign-in attempts.',
    action: 'Wait one minute, then try signing in again with the correct password.',
    escalate: 'If you are still locked out, call the Duty Manager to reset your access.'
  }
} as const;
