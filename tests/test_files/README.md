# Static Site Generator

This should not # trigger an exception

## Parse Markdown to HTML

### Block and Inline levels

- Block level: Headings, paragraphs, lists
- Inline level: Normal text, bold, italic, code and images


#### Inline text: TextNode

Intermediate representation for all different types text between Markdown and HTML, specific to inline markup.


> Markdown -> TextNode -> HTML

Example:

> This is a *italic text* and **bold text** text -> [TextNode(This is), TextNode(italic text, italic), TextNode(bold text, bold), TextNode(Text)]


### HTMLNode

Represents a node in a HTML document tree and its contents. It's purpose is to render itself as HTML as HTML tags. It's subclassed into specialized representations, ParentNode and Leaf Node.

- ParentNode. Handles the nesting of HTML nodes inside of one another. Any node that has children is a ParentNode.
- LeafNode. Representes a single HTML tag with no children

Example:

```
-> Markdown

    This markdown **would be** translated to.

-> Intermediate

    ParentNode(p, children=[LeafNode(tag=None, value=This markdown), LeafNode(tag=b, value=would be, props=None), LeafNode(tag=None, value=Translated to))

-> HTML 

    <p> This markdown <b> would be </b> translated to. </p>
```


