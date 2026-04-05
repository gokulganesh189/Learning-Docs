def check_pattern(G, P):
    rows_G = len(G)
    cols_G = len(G[0]) if rows_G > 0 else 0
    rows_P = len(P)
    cols_P = len(P[0]) if rows_P > 0 else 0

    for i in range(rows_G - rows_P + 1):
        for j in range(cols_G - cols_P + 1):
            match_found = True
            for x in range(rows_P):
                for y in range(cols_P):
                    if G[i + x][j + y] != P[x][y]:
                        match_found = False
                        break
                if not match_found:
                    break
            if match_found:
                return 'YES'
    
    return 'NO'

G = [
'7283455864',
'6731158619',
'8988242643',
'3830589324',
'2229505813',
'5633845374',
'6473530293',
'7053106601'
]
P = [
'9505',
'3845',
'3530'
]

print(check_pattern(G, P))