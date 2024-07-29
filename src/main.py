from diffusion.diffusion_models import Models


def main():
    models = Models()

    seeds = [12, 27]
    models.run(seeds=seeds)


if __name__ == "__main__":
    main()
