import os, random, configparser

config = configparser.ConfigParser()
config.read('basta.ini')


extensions = config['paths']['extensions']
base_path = config['paths']['base']
html_path = config['paths']['html']
images_path = config['paths']['images']


sort_by = {
    'name': [],
    'date': [],
    'size': [],
    '_any': [],
}
with os.scandir(os.path.join(base_path, images_path)) as ents:
    for e in ents:
        if e.is_file():
            sort_by['name'].append(e.name)
            sort_by['date'].append(f"{e.st_mtime}__{e.name}")
            sort_by['size'].append(f"{e.st_size}__{e.name}")

print(sort_by)
exit(0)

images = os.listdir('avif')
random.shuffle(images)
for c in range(0, len(images)):
	n=(c+1)%len(images)
	current = images[c][:-5]
	next = images[n][:-5]
	html = f"""
<html><body bgcolor="#000000">
<a href="{next}.html"><img src="avif/{current}.avif" alt="{current}" width="100%" /></a>
<br><br><a href="index.html"><hr/></a><body></html>
"""
	print(f"{current} -> {next}")
	open(f"{current}.html", 'w').write(html)

open("1.html","w").write(html)
open("index.html","w").write("<html></html>")

