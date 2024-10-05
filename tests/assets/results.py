import datetime


basic = {'meta': {'title': 'Document title', 
			'creation_date': datetime.datetime(2024, 9, 22, 10, 27)}, 
			'content': {'stuff': 'Example text.\n'}}


test_paths = {'about': {'applications': {}, 'quotes': {}, 'getting_started': {}}, 
			'downloads': {'all_releases': {}, 'source_code': {}, 'windows': {}, 
			'mac_os': {}, 'other_platforms': {}}, 'documentation': {'beginners_guide': {}, 
			'developers_guide': {}, 'faq': {}}, 'community': {'mailing_lists': {}, 
			'forums': {}, 'conferences': {}}, 'news': {}}


test_basic_paths = {'about': [{'applications': {}, 'getting_started': {}}]}
