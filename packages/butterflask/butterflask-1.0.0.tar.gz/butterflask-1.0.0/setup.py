from setuptools import setup, find_packages

setup(
    name='butterflask',
    version='1.0.0',
    author='Shubh Gajjar',
    author_email='shubhgajjar2004@gmail.com',
    url='https://github.com/Shubhgajj2004/ButterFlaskUI',
    description='A modern lightweight Python framework to create highly responsible front-end code on the fly',
    long_description = '''
ButterFlask-UI is a modern lightweight Python framework for creating highly responsive websites using widgets. It provides a seamless development experience, similar to Flutter, by leveraging the power of widgets to build interactive user interfaces. With ButterFlask-UI, you can easily create elegant and dynamic web applications by composing reusable widgets. The framework simplifies the process of handling API requests in the front-end through AJAX, enabling efficient data exchange and seamless user interactions.

Key Features:
- Intuitive widget-based approach for building web interfaces
- Highly responsive design for optimal viewing across different devices
- Effortless handling of API requests
- Simplified widget composition and customization
- Effortlessly handle HTML, CSS, JS in one single Python code
- Increased reusability
- Increased redability (Not like simple HTML/CSS/JS)

ButterFlask-UI empowers developers to rapidly create feature-rich web applications with smooth user experiences. Whether you're building a personal project or a professional web application, ButterFlask-UI offers the flexibility and simplicity you need to bring your ideas to life.
''',

    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
)
