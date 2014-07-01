from distutils.core import setup

setup(name="emotion", version="0.1",
      description="ESRF Motion library",
      author="M. Guijarro, M. Perez (ESRF)",
      package_dir={"emotion": "emotion"},
      packages=["emotion", 'emotion.controllers', 'emotion.config', 'emotion.comm'])  # , "cool.control_objects"])
