from distutils.core import setup

setup(name="emotion", version="0.1",
      description="ESRF Motion library",
      author="M. Guijarro, M. Perez (ESRF)",
      package_dir={"emotion": "emotion"},
      packages=["emotion"])  # , "cool.control_objects"])
