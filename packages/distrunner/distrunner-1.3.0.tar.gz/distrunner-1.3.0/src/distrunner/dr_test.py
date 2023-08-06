from distrunner import DistRunner
import whatismyip


REQUIREMENTS = [
    "beautifulsoup4==4.11.1",
    "bs4==0.0.1",
    "certifi==2021.10.8",
    "charset-normalizer==2.0.12",
    "cramjam==2.5.0",
    "diskcache==5.4.0",
    "distrunner>=1.0.0",
    "fastparquet==0.8.1",
    "fsspec==2022.3.0",
    "idna==3.3",
    "jq==1.2.2",
    "lxml==4.8.0",
    "numpy==1.22.3",
    "pandas==1.4.2",
    "pyarrow==7.0.0",
    "pycountry==22.3.5",
    "python-dateutil==2.8.2",
    "pytz==2022.1",
    "requests==2.27.1",
    "six==1.16.0",
    "soupsieve==2.3.2",
    "sqlitedict==2.0.0",
    "tenacity==8.0.1",
    "urllib3==1.26.9",
    "claws==0.0.20",
    "smart_open",
    "clannotation==0.0.7",
    "coiled",
    "dask[complete]",
]


def main():
    with DistRunner(
        workers=1,
        requirements=REQUIREMENTS,
        application_name="test",
    ) as cldr:
        results = cldr.client.map(print_ip, range(1))
        outcome = cldr.client.gather(results)

        print(outcome)


def print_ip(x):
    return f"My IP address is {whatismyip.whatismyip()}"


if __name__ == "__main__":
    main()
