"""
Put all the values that will have static values to them
"""

SCIENTISTS = ["Albert Einstein", "Isaac Newton", "Marie Curie", "Charles Darwin"]

WIKIPEDIA_LINK = "https://www.wikipedia.org/"

HTML_CONTENT = """
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Quandri</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
</head>
<body>
    <div class="container my-5">
        <h1 class="is-size-4">Hi again! I took around <span class='has-text-danger has-text-weight-bold'>{{ elapsed }}</span> seconds to go over all the pages for you and bring the curated brief.</h1>
        <h2 class="is-size-4">Here's the run down of all the scientists info.</h2>
        {{ content }}
    </div>
</body>
</html>
"""

FILENAME = "output.html"

INTRO_TEXT = """
I am one of the many Robo-Quandrinauts from Quandri.
I was born on May 17, 2023. Please be patient with me as I am young and naive.

As you've executed this script. I will help you gather information about the given scientists.
After a 3-second countdown, I will:
- Open the browser.
- Run for all the scientist wiki pages to fetch their basic info.
- Display the curated results on a new webpage.
"""
