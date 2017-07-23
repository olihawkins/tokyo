# tokyo
A python module for simulating the outcomes of dice rolls in King of Tokyo. This is the code that underpins this [analysis][blogpost].

### Requirements
The code is Python 3 and was developed with Python 3.5.3. It requires the following packages:

  - numpy
  - pandas
  - matplotlib
  - seaborn

The seaborn charts are generated with Helvetica Neue as the font, which I have converted to a ttf using Fondu on MacOS. If Helvetica Neue is not available to matplotlib on your computer you will either need to get/convert it or change the font in `save_heatmap`.

### Installation
Clone the repository.

### Usage
Start a python shell in the repo directory and `import tokyo`. To run the full analysis do `tokyo.run_analysis()`. Note that the full analysis takes around ten minutes to run. Reduce the number of simulations to generate output more quickly, but with less precision.

[blogpost]: <http://olihawkins.com/2017/07/1>

