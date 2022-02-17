# Spatial Data Analysis Exercise
A short exercise on identifying the biggest city (in terms of its population) located in a coastal zone, at most 50km from a river's mouth.
### Usage
python main.py arg1 arg2 <br><br>
Where <br>
**arg1**: Projected CRS EPSG Code <br>
**arg2**: Buffer's radius <br><br>
*Buffer radius will usually be expressed in meters as its UoM* <br><br>
Example: python main.py 4087 50000

### Visualization Output - Example
![](/visualizations/ranked_cities_4087_better_res.PNG)

### CSV Report Output - Example
|index|NAME       |POP2020                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-----|-----------|-------
|3    |Dhaka      |17015.0
|61   |Guangzhou  |10414.0
|61   |Dongguan   |5366.0 
|13   |Vancouver  |2310.0 
|39   |Panama City|1527.0 
|11   |Rostov     |1044.0 
|9    |Riga       |0.0    
|27   |Bethel     |0.0    
|28   |The Hague  |0.0    
|42   |Tampico    |0.0    
|44   |Matamoros  |0.0    
|49   |Savannah   |0.0    
|51   |Bur Said   |0.0    
|54   |Atyrau     |0.0    
|57   |Gdańsk     |0.0    
|60   |Manukau    |0.0    