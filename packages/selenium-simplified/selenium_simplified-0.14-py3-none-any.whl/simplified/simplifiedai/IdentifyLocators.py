from bs4 import BeautifulSoup


class ParseDOM:

    def custom_xpath_locator(self, tags):
        custom_locator = ['//*[@' + key + "='" + ' '.join(value) + "']" if type(value) is list else
                          '//*[@' + key + "='" + value + "']" for key, value in tags.attrs.items()]
        return custom_locator

    def give_locator_all_inputBoxes(self, source):
        all_paths = []
        try:
            doc = BeautifulSoup(source, "html.parser")
            tag = doc.find_all('input')
            for tags in tag:
                if 'hidden' not in str(tags).lower():
                    xpath = self.custom_xpath_locator(tags=tags)
                    all_paths.append(xpath)
            return all_paths
        except:
            raise Exception('ERROR - not able to generate the xpath!')
