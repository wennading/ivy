# ivy: interactive visual phylogenetics

`ivy` is a lightweight library and an interactive visual programming
environment for phylogenetics.  It is built on a powerful foundation
of open-source software components, including numpy, scipy,
matplotlib, and IPython.

`ivy` emphasizes interactive, exploratory visualization of
phylogenetic trees.  For example, in IPython:


```python
from ivy.interactive import *

root = readtree("primates.newick")
fig = treefig(root)
```

This will open an interactive tree window that allows panning,
zooming, and node selection with the mouse. Additionally, you can
manipulate the figure from the console, e.g.:

```python
fig.ladderize()
fig.toggle_leaflabels()
```

## Documentation and other resources

(Woefully out of date and incomplete)

http://www.reelab.net/ivy

## Installation


Recommended for non-developers: use [conda](https://conda.io/miniconda.html) for Python 3.

1. Download and install Miniconda for **Python 3**

    https://conda.io/miniconda.html
	
    The following assumes `conda` is now in your `$PATH`.

2. Create an environment for `ivy`:


    ```bash
    conda create -n ivy ipython jupyter numpy scipy matplotlib biopython pillow pyparsing lxml  
    # here 'ivy' is just the environment name,if you want to install the mudule in the defalt 
    # path of Anaconda,then don't creat a new encironment
    ```
  
3. Activate the environment:

    ```bash
    source activate ivy
    ```

3. Install `ivy`:

    ```bash
    pip install https://github.com/rhr/ivy/zipball/master # just install from here
    ```
  
4. To update, uninstall it first:
    ```bash
    pip uninstall ivy-phylo
    ```
   then re-run `pip` as above.
