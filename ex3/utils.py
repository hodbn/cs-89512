def concrete_predict(out_probs):
    # choose binary outputs (true iff >= 0.5)
    return [(item[0] > 0.5).astype(int) for item in out_probs]
