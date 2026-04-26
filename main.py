import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

from src.gruzdata import sessions, train_test_split
from src.metrics import hit_at_k
from src.mod import build_graph, top_popular, recommend
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(current_dir, ".", "images")
os.makedirs(images_dir, exist_ok=True)

def eda(ss):
    items = [x for s in ss for x in s]
    lens = [len(s) for s in ss]
    freq = Counter(items)

    print("sessions:", len(ss))
    print("unique items:", len(freq))
    print("avg length:", np.mean(lens))

    plt.figure(figsize=(6,4))
    plt.hist(lens, bins=15)
    plt.title("Session length")
    plt.savefig("images/eda_len.png")
    plt.close()

    vals = sorted(freq.values(), reverse=True)
    plt.figure(figsize=(6,4))
    plt.plot(vals)
    plt.yscale("log")
    plt.title("Item popularity")
    plt.savefig("images/eda_pop.png")
    plt.close()

def main():
    train, target = train_test_split(sessions)

    eda(sessions)

    nxt = build_graph(train)

    popular = top_popular(train, 10)

    preds_model = [recommend(s, nxt, popular, 10) for s in train]
    preds_base = [popular for _ in train]

    score_model = hit_at_k(preds_model, target)
    score_base = hit_at_k(preds_base, target)

    print("\nRESULTS")
    print("model:", score_model)
    print("baseline:", score_base)
    print("gain:", score_model - score_base)

    plt.figure(figsize=(5,4))
    plt.bar(["model", "baseline"], [score_model, score_base])
    plt.title("Hit@10 comparison")
    plt.savefig("images/results.png")
    plt.close()

if __name__ == "__main__":
    main() 