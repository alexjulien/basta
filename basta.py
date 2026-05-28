import os, random, configparser

config = configparser.ConfigParser(allow_no_value=True)     
config.read('basta.ini')


extensions = config['paths']['extensions']
base_path = config['paths']['base']
html_path = config['paths']['html']
images_path = config['paths']['images']
html = open('basta.html', 'r').read()


sort_by = {
    'name': [],
    'date_s': [],
    'size_s': [],
    'date': [],
    'size': [],
    '_any': [],
}
with os.scandir(os.path.join(base_path, images_path)) as ents:
    for e in ents:
        if e.is_file():
            sort_by['name'].append(e.name)
            sort_by['date_s'].append(f"{e.stat().st_mtime}__{e.name}")
            sort_by['size_s'].append(f"{e.stat().st_size}__{e.name}")
            sort_by['_any'].append(e.name)

sort_by['name'].sort()
sort_by['date_s'].sort()
sort_by['date_s'].reverse()
sort_by['size_s'].sort()
random.shuffle(sort_by['_any'])

for f in sort_by['date_s']:
    sort_by['date'].append(f.split('__')[1])
for f in sort_by['size_s']:  
    sort_by['size'].append(f.split('__')[1])

total_sort_by = len(sort_by['name'])
for i in range(0, len(sort_by['name'])):
    f = sort_by['_any'][i]
    f_next_any = sort_by['_any'][(i+1)%total_sort_by]
    f_prev_any = sort_by['_any'][(i-1)%total_sort_by]
    # print(f"_any: {f_prev} <- {f} -> {f_next}")

    f_next_date = sort_by['date'][(sort_by['date'].index(f)+1)%total_sort_by ]
    f_prev_date = sort_by['date'][(sort_by['date'].index(f)-1)%total_sort_by ]
    #print(f"date: {f_prev_date} <- {f} -> {f_next_date}")
    
    f_next_size = sort_by['size'][(sort_by['size'].index(f)+1)%total_sort_by ]
    f_prev_size = sort_by['size'][(sort_by['size'].index(f)-1)%total_sort_by ]
    # print(f"size: {f_prev_size} <- {f} -> {f_next_size}")

    
    f_next_name = sort_by['name'][(sort_by['name'].index(f)+1)%total_sort_by ]
    f_prev_name = sort_by['name'][(sort_by['name'].index(f)-1)%total_sort_by ]
    # print(f"name: {f_prev_name} <- {f} -> {f_next_name}")

    html_file = os.path.join(base_path, html_path, "%s.html" % f.split('.')[0])
    link_grid = [
         os.path.join(f"{html_path}/{f_prev_any.split('.')[0]}.html"),
         os.path.join(f"{html_path}/{f_next_any.split('.')[0]}.html"),
         os.path.join(f"{html_path}/{f_prev_date.split('.')[0]}.html"),
         os.path.join(f"{html_path}/{f_next_date.split('.')[0]}.html"),
         os.path.join(f"{html_path}/{f_prev_size.split('.')[0]}.html"),
         os.path.join(f"{html_path}/{f_next_size.split('.')[0]}.html"),
         os.path.join(f"{html_path}/{f_prev_name.split('.')[0]}.html"),
         os.path.join(f"{html_path}/{f_next_name.split('.')[0]}.html"),
         os.path.join(f"{html_path}/index.html"),
    ]
    html_out = html.replace("{image}", f"{images_path}/{f}")
    html_out = html_out.replace("{link_grid}", ', '.join(['"%s"' % link for link in link_grid]))
    open(html_file, 'w').write(html_out)
html_file = os.path.join(base_path, html_path, "index.html")
open(html_file, 'w').write(html_out)

print("Generated %d html files" % total_sort_by)