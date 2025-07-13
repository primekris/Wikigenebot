import wikipedia
import datetime

def search_wikipedia(query, lang="en"):
    wikipedia.set_lang(lang)
    try:
        page = wikipedia.page(query)
        return f"*{page.title}*\n\n{page.summary[:1000]}...\n[Read more]({page.url})"
    except wikipedia.exceptions.DisambiguationError as e:
        options = "\n".join(f"- {opt}" for opt in e.options[:5])
        return f"❗ The query returned multiple results. Try being more specific:\n\n{options}"
    except wikipedia.exceptions.PageError:
        return "❌ No matching article found."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def random_article(lang="en"):
    wikipedia.set_lang(lang)
    try:
        title = wikipedia.random()
        page = wikipedia.page(title)
        return f"*{page.title}*\n\n{page.summary[:1000]}...\n[Read more]({page.url})"
    except Exception as e:
        return f"⚠️ Error fetching random article: {str(e)}"

def today_in_history(lang="en"):
    wikipedia.set_lang(lang)
    today = datetime.datetime.now()
    month = today.strftime("%B")
    day = today.day
    try:
        page = wikipedia.page(f"{month} {day}")
        return f"*On This Day — {month} {day}*\n\n{page.summary[:1000]}...\n[Read more]({page.url})"
    except Exception as e:
        return f"⚠️ Error fetching today's history: {str(e)}"
