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
plotter.print()

```

### styles
uuplotter uses styles to visualise data sets.

current styles avaliable:

- linear right leaning -> 
<br>![lrl](examples/images/linear_right_leaning.png)

planned styles:

- linear left leaning
- linear trail
- spider
