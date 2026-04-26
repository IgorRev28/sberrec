from collections import Counter, defaultdict

def build_graph(train):
    "граф переходов между товарами"
    nxt = defaultdict(Counter)
    for s in train:
        for a, b in zip(s[:-1], s[1:]):
            nxt[a][b] += 1
    return nxt

def top_popular(train, k=10):
    "Самые популярные товары (baseline)"
    items = [x for s in train for x in s]
    pop = Counter(items)
    return [x for x, _ in pop.most_common(k)]

def recommend(session, nxt, popular, k=10):
    "Рекомендация"
    last = session[-1]
    recs = []
    
    if last in nxt:
        ranked = sorted(nxt[last].items(), key=lambda x: -x[1])
        recs = [item for item, _ in ranked if item != last]
    
    for p in popular:
        if len(recs) >= k:
            break
        if p not in recs and p != last:
            recs.append(p)
    
    return recs[:k]