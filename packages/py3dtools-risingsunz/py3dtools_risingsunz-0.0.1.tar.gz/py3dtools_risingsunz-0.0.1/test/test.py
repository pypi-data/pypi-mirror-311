import py3dtools
from py3dtools.vtp2stl import vtp2stl
from py3dtools.stl2obj import stl2obj
print(dir(py3dtools))
vtp2stl.convert_files('test', 'test')
stl2obj.convert_files('test', 'test')
