import wikipedia
import datetime

def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=3, auto_suggest=False)
        page = wikipedia.page(query, auto_suggest=False)
        return f"*{page.title}*
{summary}

🔗 {page.url}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_random_article():
    try:
        title = wikipedia.random(1)
        return search_wikipedia(title)
    except Exception as e:
        return f"❌ Error fetching random article: {str(e)}"

def get_today_on_history():
    try:
        today = datetime.datetime.now()
        month = today.strftime("%B")
        day = today.day
        query = f"{month}_{day}"
        page = wikipedia.page(query)
        return f"*{page.title}*

🔗 {page.url}"
    except Exception as e:
        return f"❌ Could not fetch today's history: {str(e)}"

def set_language(code):
    try:
        wikipedia.set_lang(code)
        return True
    except:
        return False