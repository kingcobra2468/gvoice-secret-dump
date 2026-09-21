import random
import time


def human_like_sleep(base_seconds=2.0, variance=0.5):
    """
    Simulates a human-like pause.
    Applies Gaussian distribution and a randomized multiplier to
    create natural variations in timing.
    """
    # 1. Base random delay using Gaussian distribution
    # (mean = base_seconds, standard deviation = variance)
    sleep_time = random.gauss(base_seconds, variance)

    # 2. Add exponential decay (simulating getting distracted or typing slower)
    # This occasionally creates much longer pauses (micro-breaks)
    if random.random() < 0.1:  # 10% chance
        sleep_time += random.expovariate(1.0)

    # 3. Ensure the sleep time doesn't drop below a minimum threshold
    sleep_time = max(0.2, sleep_time)

    time.sleep(sleep_time)
