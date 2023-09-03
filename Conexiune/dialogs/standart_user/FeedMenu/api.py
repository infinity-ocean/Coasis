from datetime import datetime, timedelta


async def less_4h(added_time):
    elapsed_time = datetime.now() - datetime.fromtimestamp(added_time)
    return elapsed_time <= timedelta(hours=4)
