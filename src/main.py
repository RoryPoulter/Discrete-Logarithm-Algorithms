"""The main script that will run the different algorithms and compare run-times.
"""


from discrete_log import baby_step_giant_step, pohlig_hellman


def main():
    """Runs the DLP algorithms on random inputs and compares the run-times.
    """
    print(baby_step_giant_step(2, 7, 11))  # 7
    print(baby_step_giant_step(2, 435, 2579))  # 853
    print(pohlig_hellman(2, 7, 11))  # 7


if __name__ == "__main__":
    main()
