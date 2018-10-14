import csv
import sqlite3


HEXACO_KEYS = [
    'sincerity',
    'fairness',
    'greed-avoidance',
    'modesty',
    'fearfulness',
    'anxiety',
    'dependence',
    'sentimentality',
    'social-self-esteem',
    'social-boldness',
    'sociability',
    'liveliness',
    'forgiveness',
    'gentleness',
    'flexibility',
    'patience',
    'organization',
    'diligence',
    'perfectionism',
    'prudence',
    'aesthetic-appreciation',
    'inquisitiveness',
    'creativity',
    'unconventionality',
]


def compute_hexaco(answers):
    def r(i):
        return [0, 5, 4, 3, 2, 1][i]

    ans = list(map(int, answers.split('|')))
    ans = [0] + ans
    hexaco_scores = {
        'sincerity': (ans[6] + r(ans[30]) + ans[54]) / 3.0,
        'fairness': (r(ans[12]) + ans[36] + ans[60]) / 3.0,
        'greed-avoidance': (ans[18] + r(ans[42])) / 2.0,
        'modesty': (r(ans[24]) + r(ans[48])) / 2.0,
        'fearfulness': (ans[5] + ans[29] + r(ans[53])) / 3.0,
        'anxiety': (ans[11] + r(ans[35])) / 2.0,
        'dependence': (ans[17] + r(ans[41])) / 2.0,
        'sentimentality': (ans[23] + ans[47] + r(ans[59])) / 3.0,
        'social-self-esteem': (ans[4] + r(ans[28]) + r(ans[52])) / 3.0,
        'social-boldness': (r(ans[10]) + ans[34] + ans[58]) / 3.0,
        'sociability': (ans[16] + ans[40]) / 2.0,
        'liveliness': (ans[22] + r(ans[46])) / 2.0,
        'forgiveness': (ans[3] + ans[27]) / 2.0,
        'gentleness': (r(ans[9]) + ans[33] + ans[51]) / 3.0,
        'flexibility': (r(ans[15]) + ans[39] + r(ans[57])) / 3.0,
        'patience': (r(ans[21]) + ans[45]) / 2.0,
        'organization': (ans[2] + r(ans[26])) / 2.0,
        'diligence': (ans[8] + r(ans[32])) / 2.0,
        'perfectionism': (r(ans[14]) + ans[38] + ans[50]) / 3.0,
        'prudence': (r(ans[20]) + r(ans[44]) + r(ans[56])) / 3.0,
        'aesthetic-appreciation': (r(ans[1]) + ans[25]) / 2.0,
        'inquisitiveness': (ans[7] + r(ans[31])) / 2.0,
        'creativity': (ans[13] + ans[37] + r(ans[49])) / 3.0,
        'unconventionality': (r(ans[19]) + ans[43] + r(ans[55])) / 3.0,
    }
    return hexaco_scores


conn = sqlite3.connect('app.db')

cur = conn.cursor()
cur.execute('SELECT * FROM user')
rows = cur.fetchall()

users = []
for row in rows:
    if row[2] is None:
        continue
    n2_correct, n2_wrong, n2_possible = row[3].split(';')
    n3_correct, n3_wrong, n3_possible = row[6].split(';')
    user = {'ident': row[1],
            'n2_correct': n2_correct,
            'n2_wrong': n2_wrong,
            'n2_possible': n2_possible,
            'n2_time': row[4],
            'n3_correct': n3_correct,
            'n3_wrong': n3_wrong,
            'n3_possible': n3_possible,
            'n3_time': row[5],
            }
    user.update(compute_hexaco(row[2]))
    users.append(user)

with open('web_data.csv', 'w') as csvfile:
    fieldnames = ['ident', 'n2_correct', 'n2_wrong', 'n2_possible', 'n2_time',
                  'n3_correct', 'n3_wrong', 'n3_possible', 'n3_time'] + HEXACO_KEYS
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for u in users:
        writer.writerow(u)
