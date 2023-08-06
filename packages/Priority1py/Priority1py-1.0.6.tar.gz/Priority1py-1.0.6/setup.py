
from distutils.core import setup
setup(
  name = 'Priority1py',         # How you named your package folder (MyLib)
  packages = ['Priority1py'],   # Chose the same as "name"
  version = '1.0.6',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Priority 1 web API python library',   # Give a short description about your library
  author = 'Daniel Pifer',                   # Type in your name
  author_email = '',      # Type in your E-Mail
  url = 'https://github.com/reid10305/Priority1py',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/reid10305/Priority1py/archive/refs/tags/v1.0.6.tar.gz',    # I explain this later on
  keywords = ['API', 'Priority1'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
