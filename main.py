import modules.elements as elements

coat_of_arms_path = "output/coat_of_arms.svg"
coin_output_path = "output/coin.svg"

def main():
    elements.create_coat_of_arms(coat_of_arms_path)
    elements.create_coin(coin_output_path, coat_of_arms_path)

if __name__ == "__main__":
    main()