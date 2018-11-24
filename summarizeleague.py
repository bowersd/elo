import sys
import argparse
import elo

def readin(filename):
    holder = []
    with open(filename) as file_in:
        for line in file_in:
            holder.append(line.strip().split(","))
    return holder

def parse_games(*games):
    """convert games to long form outcomes"""
    holder = []
    for g in games:
        holder.append([g[0], int(g[1])-int(g[3]), g[2]]+g[4:])
        holder.append([g[2], int(g[3])-int(g[1]), g[0]]+g[4:])
    return holder

def sort_by_date(*games):
    return sorted([x for x in games], key=lambda y: y[-1])

def season_results(*games):
    """make a dict of all teams with opponents"""
    #*games needs to be sorted by date
    holder = {g[0]:[] for g in games}
    for g in games:
        holder[g[0]].append([g[1], [x for x in holder[g[2]] if x[-1] < g[-1]]]+g[3:])
    return holder

def rate_league(f, *args, **teams):
    """apply an evaluation function to dict of teams"""
    holder = []
    for t in teams:
        holder.append((t, f(teams[t], *args)))
    return holder

def sort_league(i, *teams):
    x = [y for y in teams]
    x.sort(key=lambda z: z[i])
    return reversed(x)

def ranking(detail, k, *results):
    s = season_results(*sort_by_date(*parse_games(*results)))
    if detail: return sort_league(1, *rate_league(elo.elo_plus, *[k, elo.basic_margin], **s)) 
    return sort_league(1, *rate_league(elo.elo, *[k], **s)) 

def pprint(*ranked):
    for x in ranked:
        print("{:5}{}".format(x[0], int(round(x[1]))))

def write_csv(filename, detail, k, **teams):
    holder = []
    for t in teams:
        if detail:
            for i in range(len(teams[t])): holder.append([str(i+1), t, str(elo.elo_plus(teams[t][:i+1], k, elo.basic_margin))]+[x for x in teams[t][i][2:]])
        else:
            for i in range(len(teams[t])): 
                holder.append([str(i+1), t, str(elo.elo(teams[t][:i+1], k))]+[x for x in teams[t][i][2:]])
    with open(filename, 'w') as file_out:
        for l in holder:
            file_out.write(",".join(l)+'\n')

def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help="file path to league results")
    parser.add_argument("-d", "--detailed", dest="d", action="store_true", help="whether to access more than just w/l/d")
    parser.add_argument("-k", "--kfactor", dest="k", nargs="?", type=int, default=32, help="k factor to manage response to w/l/d")
    parser.add_argument("-o", "--output", dest="o", nargs="?", help="output file name")
    return parser.parse_args()

if __name__ == "__main__":
    #T/F, k, spreadsheet source
    args=parseargs()
    if args.o: write_csv(args.o, args.d, args.k, **season_results(*sort_by_date(*parse_games(*readin(args.csv_file)))))
    pprint(*ranking(args.d, args.k, *readin(args.csv_file)))
