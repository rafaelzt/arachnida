import os, re, argparse, requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="the URL to download")
    parser.add_argument("-l", "--length", type=int, default=2, help="the recursion depth")
    parser.add_argument("-r", "--recursive", action="store_true", help="whether to recursively download links")
    parser.add_argument("-p", "--path", default="./data", help="the path to save the file")
    args = parser.parse_args()

    return (args)

def obter_imagens_do_dominio(url, subniveis=1, extensoes=['.png', '.bmp', '.jpeg', '.jpg', '.pdf']):
    imagens = set()
    visitados = set()

    def obter_html(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None

    def encontrar_imagens_html(html, url):
        soup = BeautifulSoup(html, 'html.parser')

        # Obtém as imagens das tags <img>
        img_tags = soup.find_all('img')
        for img_tag in img_tags:
            src = img_tag.get('src')
            if src and any(src.endswith(extensao) for extensao in extensoes):
                imagens.add(urljoin(url, src))

        # Obtém as imagens das tags <div> com estilos de background definidos no CSS
        div_tags = soup.find_all('div')
        for div_tag in div_tags:
            style = div_tag.get('style')
            if style:
                urls = re.findall(r'url\((.*?)\)', style)
                for u in urls:
                    if any(u.endswith(extensao) for extensao in extensoes):
                        imagens.add(urljoin(url, u.strip('\'"')))

        # Obtém as imagens dos links
        link_tags = soup.find_all('a')
        for link_tag in link_tags:
            href = link_tag.get('href')
            if href and any(href.endswith(extensao) for extensao in extensoes):
                imagens.add(urljoin(url, href))

        return imagens

    def obter_imagens_subniveis(url, nivel):
        if nivel > subniveis or url in visitados:
            return

        visitados.add(url)
        html = obter_html(url)
        if html:
            imagens = encontrar_imagens_html(html, url)

            # Obtém as imagens dos subníveis
            soup = BeautifulSoup(html, 'html.parser')
            link_tags = soup.find_all('a')
            for link_tag in link_tags:
                href = link_tag.get('href')
                if href and not href.startswith(('http', '#', 'mailto:', 'javascript:')):
                    subnivel_url = urljoin(url, href)
                    obter_imagens_subniveis(subnivel_url, nivel + 1)

    obter_imagens_subniveis(url, 1)

    return list(imagens)



if __name__ == "__main__":
    args = get_arguments()

    if not os.path.exists(args.path):
        os.makedirs(args.path)

    url = 'https://42madrid.com'
    imagens = obter_imagens_do_dominio(url, 5)
    for imagem in imagens:
        print(imagem)