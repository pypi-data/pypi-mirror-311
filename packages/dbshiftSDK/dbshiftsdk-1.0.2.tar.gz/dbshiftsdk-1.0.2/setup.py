import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='dbshiftSDK',
    version='1.0.2',
    description="A tool for converting Informatica XML mappings to Snowflake SQL and dbt models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Anand",
    author_email="anandt@systechusa.com",
    packages=setuptools.find_packages(include=['dbshiftSDK']),  # Finds your obfuscated package
    package_data={  # Manually include the pyarmor_runtime directory
        '': ['pyarmor_runtime_000000/*'],  # Include everything in the pyarmor_runtime folder
    },
    install_requires=[
        "google-generativeai",
        "tabulate",
        "argparse",        
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)