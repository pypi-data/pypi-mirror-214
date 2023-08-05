import markdown
from bs4 import BeautifulSoup
from rich import print


class ParserMarkdown:
    """Procesar el html generado a partir de markdown"""

    def __init__(self, file_path):
        """Obtiene el contenido del archivo"""

        self.file_path = file_path
        with open(self.file_path) as ff:
            content = ff.read()

        html_content = markdown.markdown(content)

        self.soup = BeautifulSoup(html_content, features="html.parser")

    def get_title(self):
        """Toma el título del documento (h1)"""
        try:
            h1 = self.soup.find("h1").text.strip()
        except IndexError:
            h1 = ""
        return h1

    def get_description(self):
        """Obtiene la descripción del documento"""
        try:
            h2 = self.soup.select("h2")[0]
            ps = h2.findPreviousSiblings("p")
            my_list = []
            for p in ps:
                my_list.append(p.text)
            my_list.reverse()
            text = "\n\n".join(my_list)
        except IndexError:
            text = ""

        return text

    def get_stages(self):
        """Obtiene todos los h2 del documento"""
        try:
            h2s = self.soup.select("h2")
        except IndexError:
            h2s = []
        return h2s

    def get_stage_description(self):
        """Obtiene la descripción de cada h2 (stage)"""
        pass

    def pretty(self):
        """Imprime el html en un bonito formato"""
        return self.soup.prettify()

    def get_tasks(self):
        """Obtiene todas las tareas de cada h2"""
        # obtener todos los h2, y de ahí todos los li
        # DONE: Cargar las tareas desde el archivo
        tasks = {}
        try:
            # ¿una lista de listas? Mejor un diccionario
            # {1:["strings", "string"], 2:["string", "string"]}
            # primero obtener todos los h2
            h2s = self.soup.select("h2")
            # ahora obtener los li de cada h2

            for index, h2 in enumerate(h2s):
                uls = h2.find_next_sibling("ul")
                lis = []
                if uls:
                    for li in uls.findChildren():
                        lis.append(li.text.strip())

                    tasks[index] = lis
                else:
                    tasks[index] = []

        except IndexError:
            tasks = {}
            print("Hubo error")

        return tasks
