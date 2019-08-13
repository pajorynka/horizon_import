from urllib.request import urlopen as u_req
from bs4 import BeautifulSoup as b_soup

# URL example from Horizon website
my_url = "https://www.horizondiscovery.com/human-akt2-hct116-cell-line-hd-r02-005"


def get_soup_from_url(url):
    """Reads it as page_html.

    Arguments:
        url -- [link to web page of vendor]

    Returns:
        html code (page_soup)

    """
    try:
        u_client = u_req(my_url)
        page_html = u_client.read()
        u_client.close()
    except Exception as message:
        print(message)
        return None
    page_soup = b_soup(page_html, "html.parser")
    # page_soup is a html code from vendor's webpage
    return page_soup


def horizon(url):
    """Read vendor url and strip cell line data inot dictionary.
    Arguments:
        url -- [link to web page of vendor]
    Returns:
        dictionary -- [list of keys and values describing cell line]
    """
    page_soup = get_soup_from_url(url)
    result_dict = {}
    # result_dict is a dictionary with all cell line's properties 
    if page_soup:
        cell_line_properties = page_soup.findAll("dl", {"class":"spec-list"})
        # cell_property - keys and values in dictionary of properties
        for cell_property in cell_line_properties:
            key = cell_property.dt.text.strip()
            value = cell_property.dd.text.strip()
            result_dict[key] = value
    
        names = page_soup.findAll("h1", {"property":"name"})
        # main name of cell line
        synonyms = page_soup.findAll("div", {"class":"product-spec"})
        # synonyms of cell line's name
        descriptions = page_soup.findAll("div", {"itemprop":"description"})
        # short description of cell line

        name = names[0]
        key = 'Name'
        value = name.text.strip() 
        result_dict[key] = value
    
        key = 'Synonyms'
        value = synonyms[0].p.text.split('\n')[1].strip()
        result_dict[key] = value
        
        key = 'Description'
        value = descriptions[0].text.strip()
        result_dict[key] = value
    
    else:
        return None

    return result_dict

AKT2 = horizon(my_url)
# Dictionary is now assigned to 'AKT2' which is a name of cell line.
print(AKT2)
