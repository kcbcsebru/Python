import numpy as np
import scipy
from scipy import stats
from matplotlib import pyplot

x = np.random.normal(0, 10, size=100)
y = np.random.randint(0, 10, size=100)

# mean
print 'mean of x:'
print np.mean(x)

# median
print 'median of y:'
print np.median(y)

# mode
print 'mode of x:'
print stats.mode(x)

# var
print 'var of y:'
print np.var(y)

# std
print 'std of x:'
print np.std(x)

# corrcoef
print 'corrcoef of x and y:'
data = np.array([x, y])
print np.corrcoef(data)

# draw hist
def draw_hist(heights):
    pyplot.hist(heights, 100)
    pyplot.xlabel('Heights')
    pyplot.ylabel('Frequency')
    pyplot.title('Heights of students')
    pyplot.show()

heights = np.random.normal(165, 20, size=1000)
draw_hist(heights)
