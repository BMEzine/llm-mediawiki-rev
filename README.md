Due to an unfortunate data loss incident we had to recover our wiki content from the internet archives (way back machine).
This meant we had to restore using the HTML output rather than wiki markdown, as well as loosing all edit history.
HTML editing permissions in mediawiki present dangers and should not be given to regular users.
Therefore we could not allow public editing of the wiki reducing its overall usefulness.
In order to restore content we need to revert our HTML pages into mediawiki markdown.
This presents a complex problem for parsers as not all pages follow the same format and many of our pages/tags were out of date.
Using GPT we crafted a prompt that was capable of converting our HTML pages into markdown with the proper components.

You will need a valid OpenAI API key to use this project. Other local LLMs might also work but they've not been tested.

Over 2000 pages were converted with this prompt with minimal issues. The main being pages that exceed the allowed token size.

While you probably won't have the same issue perhaps this code will serve as a helper for some other mediawiki llm effort. No warranties of course.

```
# cat .env
OPENAI_API_KEY=
WIKI_USER=
WIKI_PASSWORD=
```
