import asyncio
import time
from datetime import datetime, timedelta
def test(key, status = {}):
    print("key: ", key)
    print("here: ", status)
    v = status if key in status.keys() else {}
    return v

async def test2(start_time, time_length, keys, status):
    current_time=datetime.now()
    print(current_time)
    await asyncio.sleep(5)
    status = test(keys[0], status)
    keys.pop(0)
    print("Wake up!")
    print(current_time)
    if (current_time < time_length) and status:
        print("snoooooze")
        await test2(start_time, time_length, keys, status)
    elif not(status):
        return status
    elif current_time >= time_length:
        return status.update({"derp": "time's up"})
    
def test3(start_time, time_length, keys, status):
    current_time=datetime.now()
    print(current_time)
    time.sleep(5)
    status = test(keys[0], status)
    keys.pop(0)
    print("Wake up!")
    print(current_time)
    if (current_time < time_length) and status:
        print("snoooooze")
        test3(start_time, time_length, keys, status)
    elif not(status):
        return status
    elif current_time >= time_length:
        return status.update({"derp": "time's up"})

async def say_after(start_time, time_length, key, status = {}):
    await asyncio.sleep(30)
    status = test(key[0], status)
    if status:
        print(status, ": ", time.strftime('%X'))
        await say_after(5, 'lol', 'a', status)
    else:
        print("done!")

async def main():
    print(f"started at {time.strftime('%X')}")
    start = datetime.now()
    end = start + timedelta(seconds=2)
    print("Start: ", start, " End: ", end)
    status = await asyncio.gather(test2(start, end, ['x', 'y', 'a', 'c', 1], {'x': 1, 'y': 1, 'a': 2, 'c': 1}))
    print("Status: ", status)
    #await say_after(5, 'hello', 'x', {"x": 1})
    

    print(f"finished at {time.strftime('%X')}")

def main2():
    print(f"started at {time.strftime('%X')}")
    start = datetime.now()
    end = start + timedelta(seconds=1)
    print("Start: ", start, " End: ", end)
    status = test3(start, end, ['x', 'y', 'a', 'c', 1], {'x': 1, 'y': 1, 'a': 2, 'c': 1})
    print("Status: ", status)

main2()
