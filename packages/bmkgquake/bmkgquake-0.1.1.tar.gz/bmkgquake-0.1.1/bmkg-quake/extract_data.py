import requests
from bs4 import BeautifulSoup


def extract_data():
    # Get HTML content from website/url
    try:
        content = requests.get('https://bmkg.go.id')
    except requests.RequestException as e:
        print(f"Error: {str(e)}")
        return None

    # If website/url working correctly, parse content using beautifulsoup4
    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')

        # Get ul-list which provide earthquake details
        result = soup.find('div', {'class': 'gempabumi-detail'})
        result = result.findChildren('li')

        # Declare earthquake variables
        datetime = None
        magnitude = None
        depth = None
        coordinate = None
        location = None
        condition = None

        # Looping result and assign value to earthquake variables
        for i, res in enumerate(result):
            if i == 0:
                datetime = res.text
            elif i == 1:
                magnitude = res.text
            elif i == 2:
                depth = res.text
            elif i == 3:
                coordinate = res.text
            elif i == 4:
                location = res.text
            elif i == 5:
                condition = res.text
            else:
                break

        # Create dictionary of earthquake variables
        res_dict = {
            'datetime': {
                'date': datetime.split(', ')[0],
                'time': datetime.split(', ')[1]
            },
            'magnitude': magnitude,
            'depth': depth,
            'coordinate': {
                'lat': coordinate.split(' - ')[0],
                'long': coordinate.split(' - ')[1]
            },
            'location': location,
            'condition': condition
        }

        # Return dictionary
        return res_dict
    else:
        print("Server error")
        return None

