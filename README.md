# TEST_SESAME
This python code plot the efficiency of the SESAME converter.

## Setup
one power supply and three DMMs were used in the setup.

 - 1 HAMEG / ROHDE & SCHARZ HMP4030
 - 1 ESCORT 3146A DMM
 - 2 HP/AGILENT 34401A
 - 1 homemade DC load. The setpoint of which is controlled by the power supply.
 
![sesame test](https://user-images.githubusercontent.com/1360703/191019980-da6eb1cb-6837-425a-bdff-fdbdba81e3f3.png)

A Raspberry PI 4 was utilized to concentrate the data and run the script.

## Outupt of the script
The script generates PNGs files like this one: \
![Cout-Eff-2021-12-25_05-20-interpolled](https://user-images.githubusercontent.com/1360703/191021179-31c387e9-8165-4717-8735-22893d57a047.png)

## How to run
To run the script, first install the dependencies with: \
```python3 -m pip install -i requirements.txt```

And then execute the script: \
```python3 mult_test.py```

Note: Due to the poor writing of my code, you have to plug the equipment in a defined sequence.

## Youtube Video 
[![Alt text](https://img.youtube.com/vi/wNqoPtnReCA/0.jpg)](https://www.youtube.com/watch?v=wNqoPtnReCA) \
This video briefly showcases the test bench.
