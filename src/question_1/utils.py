import requests
from langchain_community.document_loaders import PyPDFLoader
from bs4 import BeautifulSoup


from src.constants import INVALID_LINKS, CONTENT_FETCHING_EXCEPTION


def load_pdf(pdf_url):
    """
    Load the content of PDF.
    :param pdf_url: The PDF path
    :return: content of PDF
    """
    try:
        pdf_loader = PyPDFLoader(pdf_url)
        return pdf_loader.load()
    except Exception:
        raise


def request_url_and_return_soup(website_url):
    """
    Get the text content from the Website.
    :param website_url: The URL to be requested.
    :return: The text content of the website.
    """
    try:
        response = requests.get(website_url)
        return BeautifulSoup(response.text, "html.parser")
    except Exception:
        raise


def crawl_website(website_url):
    """
    Crawl the websites from the given URL and return the text content of all URLs.
    :param website_url: The URL of the website to be crawled.
    :return:
    """
    try:
        soup = request_url_and_return_soup(website_url)
        web_data = " ".join(soup.text.replace("\n", " ").replace("\t", " ").split())

        data_dict = {website_url: web_data}
        links = soup.find_all("a")
        link_hrefs = (link.get('href') for link in links)
        invalid_links = INVALID_LINKS
        valid_link_hrefs = {link for link in link_hrefs if "http" in link and not link.startswith(
            "tel:+") and not link.startswith("mailto:") and link not in invalid_links}
        for link in list(valid_link_hrefs):
            try:
                response_soup = request_url_and_return_soup(link)
                link_data = " ".join(response_soup.text.replace("\n", "").replace("\t", "").split())
                data_dict[link] = link_data
            except Exception as e:
                print(CONTENT_FETCHING_EXCEPTION.format(link=link, error=e))
        return data_dict
    except Exception:
        raise



