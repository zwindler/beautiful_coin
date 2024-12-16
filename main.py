import modules.elements as elements
import modules.config as config


def main():
    elements.create_coat_of_arms("output/coat_of_arms.svg", "svg/shield.svg", config.icon_paths)
    elements.create_coin("output/coin.svg", "output/coat_of_arms.svg")

if __name__ == "__main__":
    main()