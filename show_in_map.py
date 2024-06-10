import folium
from folium import branca

INPUT_FILE = "filtered_coordinates.txt"

EARTHQUAKE = f'\033[38;2;10;155;155m[EARTHQUAKE]\033[0m'
CYAN = f'\033[38;2;0;255;255m'
RESET = f'\033[0m'
TAB = "  "

MIN_LAT = 24
MAX_LAT = 40
MIN_LONG = 44
MAX_LONG = 64
ZOOM_LEVEL = 6
MAP_TILES = 'CartoDB dark_matter'
# MAP_TILES = 'Jawg.Matrix'
OUTPUT_FILE = "earthquakes.html"

HTML_BOX_WIDTH = 300
HTML_BOX_HEIGHT = 200
HTML_MAX_WIDTH = 300

FILTER_MAGNITUDE_BELOW = 1.0

# - Earthquake Log Handler Class
class EarthquakeLogs:
    # - Method to Initialize Object
    def __init__(self):
        # - Records
        self.records = []
        # - Map Center
        self.map_center = None
        # - Map
        self.map = None
    # - Method to Load Data from File
    def loadData(self, input_file = INPUT_FILE):
        print(EARTHQUAKE, "Loading Data ...")
        with open(INPUT_FILE, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                self.records.append({
                    "datetime" : parts[0],
                    "latitude" : parts[1],
                    "longitude" : parts[2],
                    "depth" : parts[3],
                    "magnitude" : parts[4],
                    "event_id" : parts[5]
                })
                print(TAB, EARTHQUAKE, "Loaded {}{}{}".format(CYAN, parts[5], RESET))
            print(TAB, EARTHQUAKE, "Loaded {} Records".format(len(self.records)))
        return self.records
    # - Method to Get Color According to Magnitude
    def getColor(self, magnitude):
        magnitude = float(magnitude)
        # - Color Grades :
        if magnitude > 9.0:
            return 'darkpurple'
        elif magnitude > 8.0:
            return 'purple'
        elif magnitude > 7.0:
            return 'pink'
        elif magnitude > 6.5:
            return 'darkred'
        elif magnitude > 6.0:
            return 'red'
        elif magnitude > 5.5:
            return 'lightred'
        elif magnitude > 5.0:
            return 'orange'
        elif magnitude > 4.5:
            return 'beige'
        elif magnitude > 4.0:
            return 'darkgreen'
        elif magnitude > 3.5:
            return 'green'
        elif magnitude > 3.0:
            return 'gray'
        elif magnitude > 2.5:
            return 'blue',
        elif magnitude > 2.0:
            return 'darkblue'
        elif magnitude > 1.5:
            return 'black'
        else:
            return 'white'
    def markOnMap(self, data, filter_below = FILTER_MAGNITUDE_BELOW):
        print(EARTHQUAKE, "Marking {}{}{} on Map ...".format(CYAN, data["event_id"], RESET))
        if float(data['magnitude']) < filter_below:
            return
        html = f"""
            <div style="font-family: Arial, sans-serif; color: #333; padding: 10px;">
                <h1 style="margin-bottom: 5px; font-size: 18px;">Earthquake Information</h1>
                <hr style="border-top: 1px solid #999; margin: 10px 0;">
                <div style="margin-bottom : 10px;">
                    <strong>Date/Time :</strong> {data['datetime']}<br>
                    <strong>Location :</strong> Latitude {data['latitude']}, Longitude {data['longitude']}<br>
                    <strong>Depth :</strong> {data['depth']} km<br>
                    <strong>Magnitude :</strong> {data['magnitude']}<br>
                    <strong>Event ID :</strong> {data['event_id']}<br>
                </div>
                <button style="background-color: #4CAF50; border: none; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin: 4px 2px; cursor: pointer; border-radius: 8px;">Report</button>
            </div>
        """
        iframe = branca.element.IFrame(
            html = html,
            width = HTML_BOX_WIDTH,
            height = HTML_BOX_HEIGHT
        )
        popup = folium.Popup(iframe, max_width = HTML_MAX_WIDTH)
        folium.Marker(
            [data['latitude'], data['longitude']],
            popup = popup,
            icon = folium.Icon(
                color = self.getColor(float(data['magnitude']))
            )
        ).add_to(self.map)
        # self.map.fit_bounds([[min_lat, min_long], [max_lat, max_long]])
    # - Method to Show Result
    def showResult(self):
        print(EARTHQUAKE, "Showing Result ...")
        self.map.save(OUTPUT_FILE)
    # - Method to Run Automatically
    def automatic(self):
        self.loadData()
        self.map_center = [(MIN_LAT + MAX_LAT) / 2, (MIN_LONG + MAX_LONG) / 2]
        self.map = folium.Map(
            location = self.map_center,
            zoom_start = ZOOM_LEVEL,
            tiles = MAP_TILES
        )
        for item in self.records:
            self.markOnMap(item)
        self.showResult()

logs = EarthquakeLogs()
logs.automatic()