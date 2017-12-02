import urllib.request
import os
import shutil

# Specify the build folder
temp_folder = "temp/"
build_folder = "build/"

def get_wishlist(wishlist_id):
    '''Grab Wishlist'''
    if os.path.isfile(temp_folder + wishlist_id + '_wishlist.html'):
        print("Reading " + wishlist_id + "_wishlist.html")
        f = open(temp_folder + wishlist_id + '_wishlist.html')
        wishlist_html = f.read()
    else:
        print("Wishlist File doesn't exist, downloading from the web...")
        response = urllib.request.urlopen(
            "https://confoo.ca/en/yvr2017/wishlist/"+wishlist_id)
        wishlist_file = response.read()
        f = open(temp_folder + wishlist_id + '_wishlist.html', 'wb+')
        f.write(wishlist_file)
        wishlist_html = f.read()

    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        from bs4 import BeautifulSoup

    soup_html = BeautifulSoup(wishlist_html, 'html.parser')
    items = soup_html.select(".session-list.user-wishlist .col-sm-10 .col-")
    analyst_list = []
    for item in items:
        session_id = item['id'].split('_')[1]
        analyst_list.append(str(session_id))

    print("Wishlist for", wishlist_id, analyst_list)

    return analyst_list

def delete_file(filename):
    try:
        os.remove(filename)
    except OSError:
        pass

# Start script
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

if not os.path.exists(build_folder):
    os.makedirs(build_folder)

if os.path.isfile(temp_folder + 'schedule.html'):
    print("Reading schedule.html")
    f = open(temp_folder + 'schedule.html')
    schedules_html = f.read()
else:
    print("File doesn't exist, downloading from the web...")
    response = urllib.request.urlopen("https://confoo.ca/en/yvr2017/schedule")
    schedules = response.read()
    f = open(temp_folder + 'schedule.html', 'wb+')
    f.write(schedules)
    schedules_html = f.read()

# Grab wishlists

attendees = {
}

wishlists = {i: get_wishlist(attendees[i]) for i in attendees}

'''Parse the schedule html'''
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

soup_html = BeautifulSoup(schedules_html, 'html.parser')
daily_schedules = soup_html.select(".schedule-day")
daily_schedules_html = '\r\n'.join(
    '<div class="daily_schedule">{}</div>'.format(x) \
    for x in daily_schedules)

combined_schedules_html = """
<html>
    <head>
        <title>ConFoo Schedules</title>

        <link rel="stylesheet" href="https:///maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" />
        <link rel="stylesheet" media="screen" type="text/css" href="https://confoo.ca/css/confoo.css" />
        <link rel="stylesheet" type="text/css" media="screen" href="https://confoo.ca/css/schedule.css" />
        <link rel="stylesheet" type="text/css" media="screen" href="https://confoo.ca/css/schedule2.css" />
        <link rel="stylesheet" type="text/css" media="screen" href="https://confoo.ca/css/session.css" />
        <link rel="stylesheet" type="text/css" media="screen" href="cf_person.css" />

    </head>
    <body>
        <div id="all_schedules">
            {schedules}
        </div>
        <script type="text/javascript">
            var wishlists = {wishlists}
        </script>
        <script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
        <script src="cf_schedule.js"></script>
    </body>
""".format(wishlists=wishlists,
           schedules=daily_schedules_html).replace(
            'href="/', 'href="https://confoo.ca/')


''' Create the combined schedule html '''
print("Creating the combined schedule html")
f = open(build_folder + 'combined-schedules.html','w+')
f.write(combined_schedules_html)

# Copy css and js
shutil.copyfile('cf_person.css', build_folder + 'cf_person.css')
shutil.copyfile('cf_schedule.js', build_folder + 'cf_schedule.js')
