from setuptools import setup, find_packages

setup(
    name='solstar',  # Replace with your package name
    version='0.1.2',    # Replace with your version
    author='Devojyoti Kansabanik',
    author_email='dkansabanik@ucar.edu',
    description='A package to simulate GHz radio Sun spectral image cubes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/devojyoti96/solstar',  # Replace with your GitHub repo URL
    packages=find_packages(),  # Automatically include all packages in the directory
    python_requires='>=3.10',  # Replace with your minimum Python version
    include_package_data=True,
    scripts=[
        'bin/aia_download_n_calib',
        'bin/make_GHz_solar_spectral_cube',
        'bin/get_total_tb',
        'bin/gen_dem',
        'bin/simulate_coronal_tb',
        'bin/simulate_chromo_tb',
        'bin/run_solstar'  
    ],
)

