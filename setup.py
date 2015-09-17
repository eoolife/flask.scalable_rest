from setuptools import setup, find_packages


version = '0.0.1'

setup(name='flask_scalarest',
      version=version,
      description='',
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='eoolife@163.com',
      author_email='',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['flask_scalarest'],
      include_package_data=True,
      test_suite='nose.collector',
      test_requires=['Nose'],  
      zip_safe=False,
      install_requires=[
        # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
