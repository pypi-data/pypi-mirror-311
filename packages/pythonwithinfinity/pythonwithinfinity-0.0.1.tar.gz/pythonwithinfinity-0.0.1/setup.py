from setuptools import setup
from PyInfinity.init import getVersion, getAuthor, getLicense
from PyInfinity import __doc__ as description

# python setup.py sdist
# twine upload dist/*

setup(
    name='pythonwithinfinity',
    version=getVersion(),
    
    author=getAuthor(),
    author_email='kmatvij71@gmail.com',
    
    description=description,
    
    long_description=description,  # Use the module's docstring as the long description
    
    url='https://www.allwithinfinity.com',
    
    license=getLicense(),
    
    packages=['PyInfinity'],
    
    install_requires=[],  # Add dependencies if necessary
    
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',  # Update this as the framework matures
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',  # Replace this with your custom license
        'Programming Language :: Python :: 3.12',
        'Operating System :: POSIX',  # Include POSIX to specify Linux support
        'Operating System :: Microsoft :: Windows',  # Correct classifier for Windows
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],

    keywords='python framework utilities PyInfinity',
    
    python_requires='>=3.12',  # Specify the minimum Python version required
    
    include_package_data=True,  # Include non-Python files if necessary (like LICENSE, README)
    
    project_urls={  # Optional, can provide more links
        'Documentation': 'https://www.allwithinfinity.com/docs',
    },
)

#Development Status :: 1 - Planning — на стадии планирования, проект только на начальном этапе.
#Development Status :: 2 - Pre-Alpha — проект почти не готов, возможно, только первая заготовка.
#Development Status :: 3 - Alpha — проект активно разрабатывается, но может содержать баги, документация и функции еще не завершены.
#Development Status :: 4 - Beta — проект почти готов, но все еще могут быть ошибки и недочеты.
#Development Status :: 5 - Production/Stable — проект завершен, стабильный и готов к использованию в продакшн-среде.
#Development Status :: 6 - Mature — проект зрелый, стабилен и поддерживается в долгосрочной перспективе.
#Development Status :: 7 - Inactive — проект заброшен и больше не поддерживается.