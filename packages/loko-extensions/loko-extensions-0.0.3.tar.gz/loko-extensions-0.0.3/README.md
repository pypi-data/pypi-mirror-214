<html><p><img style="vertical-align: middle;" src="https://user-images.githubusercontent.com/30443495/196493267-c328669c-10af-4670-bbfa-e3029e7fb874.png" width="8%" align="left" /></p>
<h1>&nbsp; Loko - Extensions</h1><br></html>

**Loko Extensions** helps in writing LoKo's **custom components**.

<b><ins>[Docs](https://loko-extensions.readthedocs.io/en/latest/)</ins></b> | 
<b><ins>[Tutorial](https://loko-extensions.readthedocs.io/en/latest/usage.html)</ins></b> | 
<b><ins>[LoKo AI](https://loko-ai.com/)</ins></b>

### Installation

```commandline
   (.venv) $ pip install loko-extensions
```

### Example

To create new components you have to define its inputs, outputs and arguments:


```python
from loko_extensions.model.components import Arg, Input, Output, Component, save_extensions

n = Arg(name="n", type="number", label="n", helper='Number of # in the output', value=1)
input = Input(id='input', label='Input', service='myfirstservice', to='output')
input_f = Input(id='file', label='File', service='upload_file', to='output')
output = Output(id='output', label='Output')
comp1 = Component(name="My First Component", args=[n], inputs=[input, input_f], outputs=[output], group="Custom")
save_extensions([comp1])
```

And create your services:

```python
import sanic
from loko_extensions.business.decorators import extract_value_args

app = sanic.Sanic('first_project')

@app.post('/myfirstservice')
@extract_value_args()
async def f(value, args):
    n = int(args.get('n'))
    return sanic.json(dict(msg=f"{'#'*n} {value} {'#'*n}"))

@app.post('/upload_file')
@extract_value_args(file=True)
async def f2(file, args):
    n = int(args.get('n'))
    return sanic.json(dict(msg=f"{'#'*n} File name: {file[0].name} {'#'*n}"))

app.run("0.0.0.0", port=8080)
```

Here is your new component in **LoKo**:

<p align="center"><img src="https://raw.githubusercontent.com/loko-ai/doc_resources/main/loko_extensions/imgs/loko-black.png" width="90%" /></p>