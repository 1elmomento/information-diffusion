from diffusion.diffusion_models import Models


def main():
    models = Models()

    seed_set = [12, 27]
    models.run(seed_set=seed_set)


if __name__ == "__main__":
    main()
