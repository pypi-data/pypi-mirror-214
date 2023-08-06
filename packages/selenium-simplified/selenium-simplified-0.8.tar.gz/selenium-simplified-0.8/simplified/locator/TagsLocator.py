import requests
from bs4 import BeautifulSoup


class ParseDOM:

    def xpath_input_tag(url):
        all_paths = []
        try:
            result = requests.get(url).text
            doc = BeautifulSoup(result, "html.parser")
            tag = doc.find_all('input')
            for tags in tag:
                if 'hidden' not in str(tags).lower():
                    print(f'***** Html Tag *****')
                    print(f'{tags}')
                    xpath = ['//*[@' + key + "='" + ' '.join(value) + "']" if type(value) is list else
                             '//*[@' + key + "='" + value + "']" for key, value in tags.attrs.items()]
                    print(f'***** Xpath Identified *****')
                    [print(path) for path in xpath]
                    all_paths.append(xpath)
                    return all_paths
        except:
            raise Exception('ERROR - not able to generate the xpath!')

