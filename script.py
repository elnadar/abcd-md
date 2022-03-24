import markdown
import pymdownx
import argparse

import markdown.extensions.toc
import markdown.extensions.smarty
import pymdownx.emoji, pymdownx.superfences
import pymdownx.arithmatex as arithmatex


ap = argparse.ArgumentParser()

ap.add_argument("-d", "--dir", default='rtl', type=str,
help="docuemnt direction: rtl or ltr")

ap.add_argument("-f", "--file", type=str, default="file.md",
help="path to markdown file you want to parse")
ap.add_argument("-o", "--output", type=str, default="file.html",
help="path to output html file you want")

args = vars(ap.parse_args())

emoji = {
        "emoji_index": pymdownx.emoji.emojione,
        "emoji_generator": pymdownx.emoji.to_png,
        "alt": "short",
        "options": {
            "attributes": {
                "align": "absmiddle",
                "height": "20px",
                "width": "20px"
            }
        }
    }

def fence_diagram_format(source, language, class_name, options, md, **kwargs):
    atrs = kwargs['attrs']
    title = atrs.get('title', 0)
    if title:
        return f"""
            <div class="admonition {language} {atrs.get('inline', atrs.get('center', ''))}">
                <p class="admonition-title">{title}</p>
                {pymdownx.superfences.fence_div_format(source, language, class_name, options, md, **kwargs)}
            </div>
        """
    return pymdownx.superfences.fence_div_format(source, language, class_name, options, md, **kwargs)

superfences = {
        "custom_fences": [
            {
                'name': 'diagram',
                'class': 'mermaid',
                'format': fence_diagram_format
            },
            {
                'name': 'رسم',
                'class': 'mermaid',
                'format': fence_diagram_format
            },
            {
                'name': 'شكل',
                'class': 'mermaid',
                'format': fence_diagram_format
            },
            {"name": "math", "class": "arithmatex", 'format': arithmatex.arithmatex_fenced_format(which="generic")}

        ]
}

tasklist = {"custom_checkbox": True}

md = markdown.Markdown(extensions=['def_list', 'attr_list', 'tables',
                                   'toc', 'footnotes', 'md_in_html', 'admonition', 'abbr',
                                   'smarty', 'pymdownx.mark', 'pymdownx.tilde',
                                   'pymdownx.superfences', 'pymdownx.b64', 'pymdownx.caret',
                                   'pymdownx.critic', 'pymdownx.details', 'pymdownx.emoji',
                                   'pymdownx.keys', 'pymdownx.progressbar', 'pymdownx.smartsymbols',
                                   'pymdownx.tasklist', 'pymdownx.inlinehilite', 'pymdownx.magiclink'],
    extension_configs = {
    "pymdownx.superfences": superfences,
    "pymdownx.emoji": emoji,
    "pymdownx.tasklist": tasklist,
    "pymdownx.highlight": {
        "auto_title": True,
    },
    "pymdownx.inlinehilite": {
        "custom_inline": [
            {"name": "math", "class": "arithmatex", "format": arithmatex.arithmatex_inline_format(which="generic")}
        ]
    },
    "smarty": {
        "smart_angled_quotes": True
    }

})

md.convertFile(args['file'], args['output'])

with open(args['output'], 'r') as f:
    output = f.read()
    
html = f"""
<!DOCTYPE html>
<html dir="{args['dir']}">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="/home/compulack/myPC/myDev/myScripts/pymd/assest/extra.css">
    <link rel="stylesheet" href="/home/compulack/myPC/myDev/myScripts/pymd/assest/style.css">
    <link rel="stylesheet" href="/home/compulack/myPC/myDev/myScripts/pymd/assest/progressbar.css">
    <script src="https://unpkg.com/mermaid@8.6.4/dist/mermaid.min.js" defer></script>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6" defer></script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" defer></script>
    
</head>
<body class="md-typeset">
    {output}
</body>
</html>
"""

with open(args['output'], 'w') as f:
    f.write(html)