import wikipedia
import datetime

current_lang = "en"

def set_language(lang):
    global current_lang
    current_lang = lang
    wikipedia.set_lang(lang)

def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=4)
        return f"🔍 *{query.title()}*\n\n{summary}"
    except wikipedia.exceptions.DisambiguationError as e:
        return "Too many results, please be more specific."
    except Exception:
        return "❌ No results found."

def random_article():
    title = wikipedia.random()
    return search_wikipedia(title)

def today_on_history():
    now = datetime.datetime.now()
    try:
        page = wikipedia.page(f"{now.strftime('%B')} {now.day}")
        return f"📅 *On this day - {now.strftime('%B %d')}*\n\n{wikipedia.summary(page.title, sentences=3)}"
    except:
        return "No historical events found for today."