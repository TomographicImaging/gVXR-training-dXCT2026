import os
if os.name == 'posix':
    backend = "EGL"
else:
    backend = "OPENGL"

gvxr.createNewContext(backend)