input_arr = [{'id':'P1', 'severity':3, 'arrivalTime':10},
              {'id':'P2', 'severity':5, 'arrivalTime':15},
              {'id':'P3', 'severity':5, 'arrivalTime':5},
              {'id':'P4', 'severity':2, 'arrivalTime':20}
              ]

sorted_by_severity = sorted(input_arr, key = lambda x: (-x['severity'], x['arrivalTime']), reverse=False)

print(sorted_by_severity)