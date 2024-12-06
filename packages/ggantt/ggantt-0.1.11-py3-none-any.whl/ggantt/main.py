# Created by: Brady Golomb
#
# Last Modified by: Brady Golomb
#
# Maintained by: 
# Brady Golomb
#
#

from datetime import datetime, date, timedelta 
import json
import webbrowser
import os
import tempfile

class Chart:
    """
    A class to represent a the "Chart" object of a Gantt Chart 

    """

    def __init__(self, title: str):
        """
        Constructs all the necessary attributes for the Chart object.

        Args:
            title (str): The chart title
        """
        self.tasks = []
        self.title = title
        self.categories = []
        self.options = {
            "backgroundColor": {"fill": "white"},
            "gantt": {
                "arrow": {
                    "angle": 45,
                    "color": "#000",
                    "length": 8,
                    "radius": 15,
                    "spaceAfter": 4,
                    "width": 5,
                },
                "barCornerRadius": 2,
                "criticalPathEnabled": True,
                "criticalPathStyle": {"stroke": "#e64a19", "strokeWidth": 5},
                "innerGridHorizLine": {"stroke": "#ccc", "strokeWidth": 1},
                "innerGridTrack": {"fill": "#f3f3f3"},
                "innerGridDarkTrack": {"fill": "#e0e0e0"},
                "labelMaxWidth": 500,
                "percentEnabled": True,
                "shadowEnabled": True,
                "shadowColor": "#000",
                "shadowOffset": 1,
                "sortTasks": True,
                "trackHeight": None
            },
            "width": 1500,
            "height": 1000
        }

    def add_task(
            self, 
            task_id: str, 
            task_label: str, 
            resource: str = None, 
            start: date = None, 
            end: date = None,
            duration: float = None, 
            dependencies: str = None, 
            percent_complete: int = 0
            ):  
        """
        Adds a task to a Gantt Chart object,
        Requires: Start+End, Start+Duration, End+Duration, or Duration

        Args:
            task_id (str): The task id for internal reference. (Must be unique)
            task_label (str): The task label
            start (date): a date type for the start date
            end (date): a date type for the end date
            duration (float): Number of days (can be decimal)
            dependencies (str): comma separated string of task_ids
            resource (str): Resource/category to associate task with
            percent_complete (int): Percent complete as an integer 
        """    
        
        # Calculate end only if duration is provide

        if (start and end):
            task = {
                "Task ID": task_id,
                "Task Name": task_label,
                "Start": start,
                "End": end,
                "Duration": None,
                "Percent Complete": percent_complete,
                "Dependencies": dependencies or [],
                "Resource": resource
            }
            self.tasks.append(task)
        elif (start and duration):
            task = {
                "Task ID": task_id,
                "Task Name": task_label,
                "Start": start,
                "End": None,
                "Duration": duration,
                "Percent Complete": percent_complete,
                "Dependencies": dependencies or [],
                "Resource": resource
            }
            self.tasks.append(task)
        elif (end and duration):
            task = {
                    "Task ID": task_id,
                    "Task Name": task_label,
                    "Start": None,
                    "End": end,
                    "Duration": duration,
                    "Percent Complete": percent_complete,
                    "Dependencies": dependencies or [],
                    "Resource": resource
                }
            self.tasks.append(task)
        elif duration:
            task = {
                    "Task ID": task_id,
                    "Task Name": task_label,
                    "Start": None,
                    "End": None,
                    "Duration": duration,
                    "Percent Complete": percent_complete,
                    "Dependencies": dependencies or [],
                    "Resource": resource
                }
            self.tasks.append(task)
        else:
            print("Needs 2 out of 3 (Start, End, Duration)")
        

    def set_dimensions(self, width:int, height:int):
        """
        Sets chart dimensions

        Args:
            width (int): Width of chart in pixels
            height (int): Height of chart in pixels
        """
        self.options["width"] = width
        self.options["height"] = height

    def set_background_color(self, color: str):
        """
        Sets chart background color
        
        Args:
            color (str): and str with an # representing an html compatible color
        """
        self.options["backgroundColor"]["fill"] = color
        

    def enable_critical_path(self, t_or_f:bool):
        """
        Enable/Disable Critical Path. Deafult=Disabled

        Args:
            t_or_f (bool): Boolean representing state to set critical path to
        """
        self.options["gantt"]["criticalPathEnabled"] = t_or_f

    def set_arrows(self, angle:int=45, color:str="#000", length:int=8, radius:int=15, spaceAfter:int=4, width:float=1.4):
        """
        Set arrow options

        Args:
            angle (int): The angle of the head of the arrow
            color (str): The color of the arrows like #000
            length (int): The length of the head of the arrow
            radius (int): The radius for defining the curve of the arrow between two tasks
            spaceAfter (int):The amount of whitespace between the head of an arrow and the task to which it points
            width (float): The width of the arrows
        """

        self.options["gantt"]["arrow"]["angle"] = angle
        self.options["gantt"]["arrow"]["color"] = color
        self.options["gantt"]["arrow"]["length"] = length
        self.options["gantt"]["arrow"]["radius"] = radius
        self.options["gantt"]["arrow"]["spaceAfter"] = spaceAfter
        self.options["gantt"]["arrow"]["width"] = width

    def set_bar_corner_radius(self, radius:int = 2):
        """
        Set the radius for defining the curve of a bar's corners

        Args:
            radius (int): The radius for defining the curve of a bar's corners
        """
        self.options["gantt"]["barCornerRadius"] = radius

    def enable_percent(self, t_or_f:bool):
        """
        Enable/Disable Percent Complete

        Args:
            t_or_f (bool): Boolean representing state to percent to
        """
        self.options["gantt"]["percentEnabled"] = t_or_f
    
    def enable_shadow(self, t_or_f:bool):
        """
        Enable/Disable Shadows

        Args:
            t_or_f (bool): Boolean representing state to set shadows to
        """
        self.options["gantt"]["shadowEnabled"] = t_or_f

    def enable_sort_tasks(self, t_or_f:bool):
        """
        Enable/Disable Shadows

        Args:
            t_or_f (bool): Boolean representing state to sortTasks to
        """
        self.options["gantt"]["sortTasks"]= t_or_f

    def format_value(self, value, column_name=None):
        if value is None:
            return 'null'
        elif isinstance(value, (datetime, date)):
            return f'new Date({value.year}, {value.month - 1}, {value.day})'
        elif column_name == 'Duration':
            # Format the duration as daysToMilliseconds(x)
            return str(value*24*60*60*1000)
        elif isinstance(value, list):
            # Join list elements into a comma-separated string
            return json.dumps(','.join(value))
        elif isinstance(value, str):
            return json.dumps(value)
        elif isinstance(value, (int, float)):
            return str(value)
        else:
            return json.dumps(str(value))


    def get_html(self):
        # Prepare the data rows
        data_rows = []

        for task in self.tasks:
            formatted_row = '[' + ', '.join(self.format_value(
                task.get(col, None), col) for col in [
                'Task ID', 'Task Name', 'Resource', 'Start', 'End',
                'Duration', 'Percent Complete', 'Dependencies']) + ']'
            data_rows.append(formatted_row)

        data_rows_str = ',\n        '.join(data_rows)

        # Prepare the resources (categories) and their colors
        options = {
            'height': self.options["height"],
            'width': self.options["width"],
        }

        options_json = json.dumps(options)

        # Generate the HTML content
        html_content =f'''<!DOCTYPE html>
<html>
<head>
    <title>{self.title}</title>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
    google.charts.load('current', {{'packages':['gantt']}});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {{
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Task ID');
        data.addColumn('string', 'Task Name');
        data.addColumn('string', 'Resource');
        data.addColumn('date', 'Start Date');
        data.addColumn('date', 'End Date');
        data.addColumn('number', 'Duration');
        data.addColumn('number', 'Percent Complete');
        data.addColumn('string', 'Dependencies');


        data.addRows([
        {data_rows_str}
        ]);

        var options = {options_json};

        var chart = new google.visualization.Gantt(document.getElementById('chart_div'));

        chart.draw(data, options);
    }}
    </script>
</head>
<body>
    <h1 style="text-align: center;">{self.title}</h1>
    <div id="chart_div"></div>
</body>
</html>
        '''

        return html_content

    def show(self):
        """
        Show chart in webbrowser
        """
        html_content = self.get_html()
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
            f.write(html_content)
            filename = f.name
        webbrowser.open('file://' + os.path.realpath(filename))

    def save(self, filename):
        """
        Save chart as html file

        Args:
            filename (str): Name to save file as
        """
        html_content = self.get_html()
        with open(filename, 'w') as f:
            f.write(html_content)

    def returnHTML(self):
        """
        Return html string
        """
        html_content = self.get_html()
        return html_content
