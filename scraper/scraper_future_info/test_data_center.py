import data_center


def test_get_pcr(dc):
    dc.get_pcr()
    # pass


if __name__ == "__main__":
    dc = data_center.Data_center()
    test_get_pcr(dc)