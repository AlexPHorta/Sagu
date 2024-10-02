import datetime


basic = {'meta': {'title': 'Document title', 
			'creation_date': datetime.datetime(2024, 9, 22, 10, 27)}, 
			'content': {'stuff': 'Example text.\n'}}

wrong_meta = {'met': {'title': 'Document title', 
			'creation_date': datetime.datetime(2024, 9, 22, 10, 27)}, 
			'content': {'stuff': 'Example text.\n'}}

wrong_content = {'meta': {'title': 'Document title', 
			'creation_date': datetime.datetime(2024, 9, 22, 10, 27)}, 
			'conent': {'stuff': 'Example text.\n'}}
