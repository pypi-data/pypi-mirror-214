from qtl_xtp_api import MdApi


class PyMdApi(MdApi):

    def __init__(self, settings):
        super().__init__()
        self.settings = settings

        client_id = 1
        save_file_path = './'
        log_level = 1
        self.CreateQuoteApi(client_id, save_file_path, log_level)

    def print_api_version(self):
        v = self.GetApiVersion()
        print(f'GetApiVersion: {v}')


def test():
    print('Test...')

    settings = {
        'client_id': 1,
        'save_file_path': './',
        'log_level': 1,


    }

    md_api = PyMdApi()
    md_api.print_api_version()


    input('Waiting...\n')



if __name__ == '__main__':
    test()
