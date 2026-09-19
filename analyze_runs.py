from research_cascade_breaker import all_12_seqs, get_runs, opp

def analyze_all_sequences():
    print("=== SUMMARY OF ALL 12 REAL SEQUENCES ===")
    for name, seq in all_12_seqs:
        sizes = [x['size'][0] for x in seq]
        nums = [x['number'] for x in seq]
        print(f"\n{name} (len={len(seq)}):")
        print(" Sizes: " + " ".join(sizes))
        print(" Nums:  " + " ".join(str(n) for n in nums))
        runs = get_runs([x['size'] for x in seq])
        print(" Runs:  " + ", ".join(f"{s[0]}x{l}" for s, l in runs))

if __name__ == "__main__":
    analyze_all_sequences()
