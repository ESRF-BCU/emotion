from distutils.core import setup

setup(name="emotion", version="1.8",
      description="ESRF Motion library",
      author="M.Guijarro, C.Guilloud, M.Perez (ESRF) 2014-2015",
      package_dir={"emotion": "emotion"},
      packages=["emotion", 'emotion.controllers', 'emotion.controllers.libicepap',
                'emotion.controllers.libicepap.deep', 'emotion.config',
                'emotion.comm', 'emotion.comm.embl'])
