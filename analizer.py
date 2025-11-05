import pandas as pd


# TODO: add... everything????
class Analizer:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data: pd.DataFrame = data

    @classmethod
    def from_csv(cls, file: str) -> "Analizer":
        return cls(pd.read_csv(file))  # pyright: ignore[reportUnknownMemberType]


if __name__ == "__main__":
    test = Analizer.from_csv("./test_data.csv")

    print(test.data.mean())
