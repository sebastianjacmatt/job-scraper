import requests
from bs4 import BeautifulSoup

# The URL of the page you want to scrape
url = 'https://www.itxbergen.no/for-studenter/stillingsannonser'

# Send HTTP GET request to the URL
response = requests.get(url)

def filter_data(data, location_keyword, job_type_keyword):
    data = [item for item in data if location_keyword.lower() in item[1].lower()]
    data = [item for item in data if job_type_keyword.lower() in item[2].lower()]
    return data

def create_html_table(data):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Listings</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #000;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
    </head>
    <body>

    <table>
        <tr>
            <th>Company</th>
            <th>Location</th>
            <th>Job Type</th>
            <th>Deadline</th>
        </tr>
    """
    for row in data:
        # Ensure row has at least 4 elements and check if row[3] is empty
        if len(row) >= 4 and row[3].strip():
            deadline = row[3]
        else:
            deadline = 'N/A'  # replace with your desired default value
        
        html += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
            <td>{deadline}</td>
        </tr>
        """
    html += """
    </table>

    </body>
    </html>
    """
    with open('table.html', 'w', encoding='utf-8') as file:
        file.write(html)


# Check for a valid response (HTTP Status Code 200)
if response.status_code == 200:
    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    data = [] 
    
    for unique_parent in soup.find_all('div', {'class': 'mb-4 w-full'}):
        row_data = []
        for desired_p in unique_parent.find_all('p', {'class': 'text-gray-700'}):
            if desired_p != None:
                row_data.append(desired_p.text)
        data.append(row_data)

    data = filter_data(data, "","sommer")

    create_html_table(data)


else:
    print(f'Failed to retrieve page with status code: {response.status_code}')
