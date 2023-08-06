import qtl_xtp_api as m


def test_basic():
    print(m)


def test_consts():
    print(m.consts)
    print(f'XTP_EXCHANGE_SH: {m.consts.XTP_EXCHANGE_SH}')
    print(f'XTP_EXCHANGE_SZ: {m.consts.XTP_EXCHANGE_SZ}')


if __name__ == '__main__':
    test_basic()
    test_consts()
