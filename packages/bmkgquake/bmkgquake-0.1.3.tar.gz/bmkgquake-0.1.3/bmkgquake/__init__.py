from bmkgquake.display_data import display_data
from bmkgquake.extract_data import extract_data

__all__ = ['display_data', 'extract_data']

if __name__ == '__main__':
    result = extract_data()
    display_data(result)