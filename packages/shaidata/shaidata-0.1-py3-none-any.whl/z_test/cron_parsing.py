from croniter import croniter
from datetime import timedelta, datetime
now = datetime.now()
next = now + timedelta(minutes=3)

cron = croniter('45 * * * *', now)
print(cron.get_current(datetime))
print(cron.get_prev(datetime))
print(cron.get_next(datetime))

from croniter import croniter_range
print('{}~{}'.format(now, next))
for dt in croniter_range(now, next, "*/2 * * * *"):
    print(dt)
