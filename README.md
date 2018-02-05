# uuplotter
ascii data plotter

python module to visualise data.

### usage
An example of using the uuplotter module.
```python
import uuplotter

data = {
	'one': ['two', 'three'],
	'two': ['three', 'four'],
	'three': ['four', 'five']
}

plotter = uuplotter.Plotter(data)
for key in plotter.datapoints:
	plotter.center(key)
	plotter.print()

```
![usage output](examples/images/usage_example.png)
### styles
uuplotter uses styles to visualise data sets.

current styles avaliable:

- linear right leaning
<br>![lrl](examples/images/linear_right_leaning.png)<br>
- linear trail
<br>![lt](examples/images/linear_trail.png)<br>

planned styles:

- linear left leaning
- spider
