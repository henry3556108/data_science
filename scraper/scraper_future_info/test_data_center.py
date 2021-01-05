import data_center


def test_get_pcr(dc):
    dc.get_pcr()
    # pass

def test_get_date(dc):
    dates = dc._get_date("2010/1/1", "2010/1/1")
    print(dates)
    dates = dc._get_date("2010/1/1", "2010/1/2")
    print(dates)
    dates = dc._get_date("2010/1/1", "2010/12/31")
    print(dates)
    dates = dc._get_date("2010/1/1", "2010/3/5")
    print(dates)
    

if __name__ == "__main__":
    dc = data_center.Data_center()
    # test_get_pcr(dc)
    test_get_date(dc)