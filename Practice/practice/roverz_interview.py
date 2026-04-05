activity = [
    {"user": 1, "action": "login", "time": 10},
    {"user": 1, "action": "click", "time": 12},
    {"user": 2, "action": "login", "time": 15},
    {"user": 1, "action": "logout", "time": 18},
    {"user": 2, "action": "logout", "time": 25},
    {"user": 1, "action": "login", "time": 30},
    {"user": 1, "action": "click", "time": 32},
    {"user": 1, "action": "logout", "time": 40},
    {"user": 3, "action": "login", "time": 20},
    {"user": 3, "action": "click", "time": 22},
    {"user": 3, "action": "purchase", "time": 23},
    {"user": 3, "action": "logout", "time": 28},
    {"user": 2, "action": "login", "time": 35},
    {"user": 2, "action": "click", "time": 36},
    {"user": 2, "action": "logout", "time": 45},
    {"user": 4, "action": "login", "time": 50},
    {"user": 4, "action": "click", "time": 55},
    {"user": 4, "action": "logout", "time": 65},
    {"user": 1, "action": "login", "time": 70},
    {"user": 1, "action": "purchase", "time": 72},
    {"user": 1, "action": "logout", "time": 80},
    {"user": 3, "action": "login", "time": 85},
    {"user": 3, "action": "click", "time": 90},
    {"user": 3, "action": "logout", "time": 95},
]


result = {}
for item in activity:
    user = item['user']
    action = item['action']
    if user in result and action == 'logout':
        user_obj = result[user]
        latest_time_object = user_obj['timings'][-1]
        count = latest_time_object['count']
        end_time = item['time']
        start_time = latest_time_object['start_time']
        session_time = end_time - start_time
        latest_time_object['end_time'] = end_time
        latest_time_object['session_time'] = session_time

    if user in result and action == 'login':
        user_obj = result[user]
        latest_time_object = user_obj['timings'][-1]
        count = latest_time_object['count']
        result[user]['timings'].append({'start_time':item['time'], 'end_time':None, 'session_time':None, 'count':count+1})
    if user not in result:
        count = 1
        result[user]={'timings':[{'start_time':item['time'], 'end_time':None, 'session_time':None, 'count':1}]}

        

        



print(result)
    