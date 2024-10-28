import bs4
import requests

class SCP_SCRAPPING():

    def __init__(self,number,URL,lang):
        self.number = number
        self.content = ""
        self.document = None
        self.URL = URL
        self.lang = lang
        

    def getPage(self):
        if str(self.number) == "001" and self.lang == 'esp':
            self.content = "A que o quien te refieres con 001?"
        elif str(self.number) == "001" and self.lang == 'eng':
            self.content = "What or who do you mean by 001?"
        else:
            try:
                self.URL = self.URL+str(self.number)
                response = requests.get(self.URL)
                response.raise_for_status()  # Lanza HTTPError para códigos de estado 4xx/5xx

                # Parsear la página solo si la solicitud fue exitosa
                self.document = bs4.BeautifulSoup(response.text, 'html.parser')
            except requests.exceptions.HTTPError:
                self.content = f"No se pudo encontrar el documento de {self.number}" if self.lang == 'esp' else f"Could not find document {self.number}"
    
    def getItem(self):
        self.content += f"Item #: SCP-{self.number}\n"
    
    def getDescription(self):
        p_elements = self.document.find_all('p')
        p_with_strong = []

        for p in p_elements:
            # Verifica si dentro de <p> hay un <strong> como hijo
            if p.find('strong') is not None:
                p_with_strong.append(p)

        content = p_with_strong[3].get_text()

        self.content += content
    
    def getContent(self):
        self.getPage()

        if len(self.content) == 0 and self.document is not None:
            self.getItem()
            self.getDescription()
            self.content += f"\nMore information on {self.URL}" if self.lang == 'eng' else f"\nMas información en {self.URL}"

        return str(self.content)