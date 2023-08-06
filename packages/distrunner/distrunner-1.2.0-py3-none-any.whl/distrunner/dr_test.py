from distrunner import DistRunner
import whatismyip


def main():
    with DistRunner() as cldr:
        results = cldr.client.map(print_ip, range(3))
        outcome = cldr.client.gather(results)

        print(outcome)


def print_ip(x):
    return f"My IP address is {whatismyip.whatismyip()}"


if __name__ == "__main__":
    main()
