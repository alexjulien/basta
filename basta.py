import os, random, configparser

config = configparser.ConfigParser(allow_no_value=True)     
config.read('basta.ini')


extensions = config['paths']['extensions']
base_path = config['paths']['base']
html_path = config['paths']['html']
images_path = config['paths']['images']
html = open('basta.html', 'r').read()

def html_url(f, base_path=html_path):
    return os.path.join(base_path, "%s.html" % f.split('.')[0])

# Source - https://stackoverflow.com/a/34325723
# Posted by Greenstick, modified by community. See post 'Timeline' for change history
# Retrieved 2026-06-05, License - CC BY-SA 4.0

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


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
            sort_by['date_s'].append(f"{e.stat().st_mtime}=={e.name}")
            sort_by['size_s'].append(f"{e.stat().st_size}=={e.name}")
            sort_by['_any'].append(e.name)

sort_by['name'].sort()
sort_by['date_s'].sort()
sort_by['date_s'].reverse()
sort_by['size_s'].sort()
random.shuffle(sort_by['_any'])

for f in sort_by['date_s']:
    sort_by['date'].append(f.split('==')[1])
for f in sort_by['size_s']:  
    sort_by['size'].append(f.split('==')[1])

total_sort_by = len(sort_by['name'])
printProgressBar(0, total_sort_by)
for i in range(0, total_sort_by):
    printProgressBar(i + 1, total_sort_by)
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
        html_url(f_prev_name),
        html_url(f_next_name),
        html_url(f_prev_any),
        html_url(f_prev_size),
        html_url(f_next_any),
        html_url(f_next_size),
        html_url(f_prev_date),
        html_url(f_next_date),
        html_url(f"{html_path}/index.html"),
    ]
    html_out = html.replace("{image}", f"{images_path}/{f}")
    html_out = html_out.replace("{link_grid}", ', '.join(['"%s"' % link for link in link_grid]))
    open(html_file, 'w').write(html_out)
    
html_index = open("index.html", "r").read()
html_index = html_index.replace("{first_date}", sort_by['date'][-1])
html_index = html_index.replace("{first_size}", sort_by['size'][-1])
html_index = html_index.replace("{first_name}", sort_by['name'][0])
html_index = html_index.replace("{first__any}", sort_by['_any'][0])

html_file = os.path.join(base_path, html_path, "index.html")
open(html_file, 'w').write(html_out)

print("\n\nGenerated %d html files" % total_sort_by)