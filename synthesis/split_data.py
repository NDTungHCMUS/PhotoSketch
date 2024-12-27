import random


def split_data(items, train_ratio=0.8):
    random.shuffle(items)
    split_idx = int(len(items) * train_ratio)
    train_items = items[:split_idx]
    test_items = items[split_idx:]
    return train_items, test_items
