from diffusion.diffusion_models import Models


def main():
    models = Models()

    seeds = [12, 18]
    models.run_icm_models(seeds=seeds)


if __name__ == "__main__":
    main()
