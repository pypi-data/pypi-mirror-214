import fire

from .srsly_convert import srsly_convert


def main():
    fire.Fire(srsly_convert)


if __name__ == "__main__":
    main()
