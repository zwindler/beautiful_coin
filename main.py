import modules.elements as elements

icon_paths = [
    "svg/icon1.svg",
    "svg/icon2.svg",
    "svg/icon3.svg",
    "svg/icon4.svg",
]
shield_path = "svg/shield.svg"
coat_of_arms_path = "output/coat_of_arms.svg"
coin_output_path = "output/coin.svg"

def main():
    elements.create_coat_of_arms(coat_of_arms_path, shield_path, icon_paths)
    elements.create_coin(coin_output_path, coat_of_arms_path)

if __name__ == "__main__":
    main()