from main import *
from datetime import date

chart = Chart("Example Chart Title")

chart.add_task(
    task_id="T1",
    task_label="Task 1", 
    resource="Resource 1",
    start=date(2024,10,1),
    end=None, 
    duration=1,
    dependencies=None,
    percent_complete=100,
    )

chart.add_task(
    task_id="T2",
    task_label="Task 2", 
    resource="Resource 2",
    start=date(2024,10,3),
    end=date(2024,10,5), 
    duration=None,
    dependencies="T1",
    percent_complete=30,
    )

chart.add_task(
    task_id="T3",
    task_label="Task 3", 
    resource="Resource 2",
    start=None,
    end=None, 
    duration=3,
    dependencies="T1,T2",
    percent_complete=0,
    )

chart.enable_critical_path(True)

chart.set_dimensions(1500,1000)

chart.show()
