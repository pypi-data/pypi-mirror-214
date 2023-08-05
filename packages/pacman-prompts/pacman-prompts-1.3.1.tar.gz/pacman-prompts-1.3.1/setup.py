from setuptools import setup, find_packages

setup(
  name = 'pacman-prompts',
  packages = find_packages(exclude=['examples']),
  version = '1.3.1',
  license='MIT',
  description = 'Prompts As Code, man',
  long_description_content_type = 'text/markdown',
  author = 'Anish Thite',
  author_email = 'anishthite@gmail.com',
  url = 'https://github.com/anishthite/pacman',
  keywords = [
    'artificial intelligence',
    'attention mechanism',
    'image recognition'
  ],
  install_requires=[
      'pyyaml',
  ],
  setup_requires=[
  ],
  tests_require=[
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
