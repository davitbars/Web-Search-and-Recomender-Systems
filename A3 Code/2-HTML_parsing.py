from bs4 import BeautifulSoup

bs = BeautifulSoup('<html><head><title>My first web page</title></head><body><h1>My first web page</h1><h2>What this is tutorial</h2><p>A simple page put together using HTML. <em>I said a simple page.</em>.</p><ul><li>To learn HTML</li><li>To show off<ol><li>To my boss</li><li>To my friends</li><li>To my cat</li><li>To the little talking duck in my brain</li></ol></li><li>Because I have fallen in love with my computer and want to give her some HTML loving.</li></ul><h2>Where to find the tutorial</h2><p><a href="http://www.aaa.com"><img src=http://www.aaa.com/badge1.gif></a></p><h3>Some random table</h3><table><tr class="tutorial1"><td>Row 1, cell 1</td><td>Row 1, cell 2<img src=http://www.bbb.com/badge2.gif></td><td>Row 1, cell 3</td></tr><tr class="tutorial2"><td>Row 2, cell 1</td><td>Row 2, cell 2</td><td>Row 2, cell 3<img src=http://www.ccc.com/badge3.gif></td></tr></table></body></html>', features="lxml")

# a.	The title of the HTML page. Use the HTML tags to do this search.
print(bs.title.get_text())
# Output: My first web page

# b.	The second list item element "li" below "To show off"? Use the HTML tags to do this search. The output should be "To my friends".
print(bs.select('li:-soup-contains("To show off") ol li')[1].text)
# Output: To my friends

# c.	All cells of Row 2. Use the HTML tags to do this search.
print(bs.select('tr:nth-of-type(2) td')) 
# Output: [<td>Row 2, cell 1</td>, <td>Row 2, cell 2</td>, <td>Row 2, cell 3<img src="http://www.ccc.com/badge3.gif"/></td>]

# d.	All h2 headings that include the word “tutorial”. Use the HTML tags to do this search.
print(bs.select('h2:-soup-contains("tutorial")'))
# Output: [<h2>What this is tutorial</h2>, <h2>Where to find the tutorial</h2>]

# e.	All text that includes the “HTML” word. Use the HTML text to do this search.
print(bs.find_all(string=lambda string: "HTML" in string))
# Output: ii.	['A simple page put together using HTML. ', 'To learn HTML', 'Because I have fallen in love with my computer and want to give her some HTML loving.']

# f.	All cells’ data from the first row of the table. Use the HTML tags to do this search.
print([cell.decode_contents() for cell in bs.select('tr:first-child td')])
# Output: ['Row 1, cell 1', 'Row 1, cell 2<img src="http://www.bbb.com/badge2.gif"/>', 'Row 1, cell 3']

# g.	All images from the table. Use the HTML tags to do this search.
print(bs.select('table img'))
# Output: [<img src="http://www.bbb.com/badge2.gif"/>, <img src="http://www.ccc.com/badge3.gif"/>]

