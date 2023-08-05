import requests

def id_scrape(username):
    url = f"https://www.instagram.com/{username}"
    try:
    	req = requests.get(url).text
    	if 'props":{"id":"' in req:
    	   user_id = req.split('props":{"id":"')[1].split('"')[0]
    	   return user_id
    	else:
    		return 'Bad UserName'
    except:
    	return 'Bad Request'
    	
    	
def pid_scrape(link):
    try:
    	req = requests.get(link).text
    	if 'media_id":"' in req:
    	   pid = req.split('media_id":"')[1].split('"')[0]
    	   return pid
    	else:
    		return 'Bad Link'
    except:
    	return 'Bad Request'