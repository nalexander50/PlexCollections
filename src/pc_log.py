def log_message(log, depth, prepend=None):
    pad = '\t' * depth
    if prepend is not None:
        print(prepend + pad + log)
    else:
        print(pad + log)
