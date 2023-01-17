from datetime import datetime,timedelta

def get_daily_slots(start, end, slot, date):
    # combine start time to respective day
    dt = datetime.combine(date, datetime.strptime(start,"%H:%M").time())
    slots = [dt]
    # increment current time by slot till the end time
    while (dt.time() < datetime.strptime(end,"%H:%M").time()):
        dt = dt + timedelta(minutes=slot)
        slots.append(dt)
    return slots


# Some Dummy values 
start_time = '9:00'
end_time = '15:00'
timeSLot = 30
days = 1
start_date = datetime.now().date()

for i in range(days):
    date_required = datetime.now().date() + timedelta(days=1)