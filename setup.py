from distutils.core import setup

setup(name="emotion", version="0.1",
      description="ESRF Motion library",
      author="M.Guijarro, C.Guilloud, M.Perez (ESRF)",
      package_dir={"emotion": "emotion"},
      packages=["emotion", 'emotion.controllers', 'emotion.controllers.libicepap',
                'emotion.controllers.libicepap.deep', 'emotion.config',
                'emotion.comm', 'emotion.comm.embl'])
