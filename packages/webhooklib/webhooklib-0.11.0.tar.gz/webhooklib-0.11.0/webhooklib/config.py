REDIS_PREFIX = 'webhook'
PROCESS_DONE = f'{REDIS_PREFIX}:process_done'
LOGS = f'{REDIS_PREFIX}:logs'
LOGS_TTL = 60 * 60 * 24 * 7  # 7 days
