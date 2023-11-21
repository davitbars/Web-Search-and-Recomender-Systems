from bs4 import BeautifulSoup
from pymongo import MongoClient

def connectDataBase():
    client = MongoClient("mongodb://localhost:27017")  
    db = client["A3"]
    return db

def find_document(url):
    pages = db.pages
    return pages.find_one({"url": url})

def parse_document(html):
    bs = BeautifulSoup(html, 'html.parser')
    for child in bs.find_all('div', {'class': 'clearfix'}):

        # Get the professor name
        name_tag = child.find('h2')
        if name_tag:
            name = name_tag.text.strip()
        else:
            continue  # Skip this div if h2 is not found

        # Get the professor title
        title = child.find(lambda tag: tag.name == 'strong' and (('Title:' in tag.string) or ('Title' in tag.string)))
        title = title.find_next_sibling(string=True).strip() if title else ''
        title = title.replace(": ", "")

        # Get the professor office
        office = child.find(lambda tag: tag.name == 'strong' and (('Office:' in tag.string) or ('Office' in tag.string)))
        office = office.find_next_sibling(string=True).strip() if office else ''
        office = office.replace(": ", "")


        # Get the professor phone number
        phone_number = child.find(lambda tag: tag.name == 'strong' and (('Phone:' in tag.string) or ('Phone' in tag.string)))
        phone_number = phone_number.find_next_sibling(string=True).strip() if phone_number else ''
        phone_number = phone_number.replace(": ", "")


        # Get the professor email
        email_tag = child.find(lambda tag: tag.name == 'strong' and (('Email:' in tag.string) or ('Email' in tag.string)))
        email = email_tag.find_next_sibling('a').text.strip() if email_tag else ''
        email = email.replace(": ", "")

        # Get the professor website
        website_tag = child.find(lambda tag: tag.name == 'strong' and (('Web:' in tag.string) or ('Web' in tag.string)))
        website = website_tag.find_next_sibling('a').text.strip() if website_tag else ''
        website = website.replace(": ", "")

        # print(f"Professor {name}'s data: {title}, {office}, {phone_number}, {email}, {website}")

        professor = {
            "name": name,
            "title": title,
            "office": office,
            "phone_number": phone_number,
            "email": email,
            "websiite": website
        }

        add_to_db(professor)

def add_to_db(professor):
    professors = db.professors
    professors.insert_one(professor)

if __name__ == "__main__":
    db = connectDataBase()
    target_page_url = "https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml"
    html = find_document(target_page_url)['html']
    parse_document(html)
