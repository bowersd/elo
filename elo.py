import numpy as np

def new_result(team1, team2, result):
    """add a new [result, opponent] to team1"""
    return team1.append([result, team2])

def spread(e1, e2, c):
    """points spread between e1, e2"""
    #recommend c between 25 (football, 10 pts = 1.5 scores) and ~15 
    return (e1-e2)/c

def pwin(e1, e2):
    """probability e1 beats e2"""
    return (1.0/(1+(10**((e2-e1)/float(400)))))

def elo(team, k):
    """season-long evaluation of team"""
    x = 1500.0
    for t in team: #teams are composed of matches: [result, opponent] + auxiliary info like home_away, date
        x += k*(s_to_r(t[0])-(pwin(x, elo(t[1], k))))
    return x

def s_to_r(x):
    """score to result"""
    if x == 0: return 0.5
    elif x > 0: return 1
    return 0

def basic_margin(x):
    return np.log(abs(x)+2)

def elo_plus(team, k, f):
    """elo accounting for margin of result"""
    x = 1500.0
    for t in team: #teams are composed of matches: [relscore, opponent] + auxiliary info like home_away, date
        r = s_to_r(t[0])
        x += f(t[0])*k*(r-(pwin(x, elo_plus(t[1], k, f))))
    return x

def baby_elo(e1, e2, result, k):
    """change in e1 given e2, result, k"""
    return k*(result-(pwin(e1, e2)))

