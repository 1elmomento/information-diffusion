from measures.measures import Measures


def main():
    measures = Measures()

    seed_set = [12, 5]
    prob = 0.5
    spread = measures.run(seed_set=seed_set, prob=prob)
    print(spread)


if __name__ == "__main__":
    main()
