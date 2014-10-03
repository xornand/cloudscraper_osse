#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from setuptools.command.install import install
from subprocess import call
import os
from cloudscraper_osse.utils import is_windows, is_linux, is_python_32bit, info, is_os_64bit

IS_OSS_VERSION = True

class CustomInstall(install):

    def run(self):
        
        # run installation
        install.run(self)
        
        corespath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'apps', 'cores')
        #os.chdir(dirpath)
        
        if is_windows():
            if not is_os_64bit():
                
                dirpath = os.path.join(corespath, 'bin','windows','32')
                os.environ['PATH'] = dirpath + ';' + os.environ['PATH']
                
                print "Installing tika service..."
                call(['install.cmd', dirpath, corespath])
                
                print "Installing suggest service..."
                call(["install_ss.cmd", dirpath, corespath, 'cores', 'default', 'suggs.dat'])
                
                if not IS_OSS_VERSION:
                    print "Installing license service..."
                    call(["install_lm.cmd", dirpath, corespath])
            
            else:
            
                dirpath = os.path.join(corespath, 'bin','windows','64')
                os.environ['PATH'] = dirpath + ';' + os.environ['PATH']
                
                print "Installing tika service..."
                call(['install64.cmd', dirpath, corespath])
                
                print "Installing suggest service..."
                call(["install64_ss.cmd", dirpath, corespath, 'cores', 'default', 'suggs.dat'])
                
                if not IS_OSS_VERSION:
                    print "Installing license service..."
                    call(["install64_lm.cmd", dirpath, corespath])
        
        elif is_linux():
        
            if not is_os_64bit():
                dirpath = os.path.join(corespath, 'bin','linux','32')
                os.environ['PATH'] = dirpath + ';' + os.environ['PATH']
                
            else:
                dirpath = os.path.join(corespath, 'bin','linux','64')
                os.environ['PATH'] = dirpath + ';' + os.environ['PATH']
                
        elif is_mac():
            logger.error("mac not supported at the moment")
            return
        else:
            logger.error("Unable to detect os and platform!")
            return
        
        print "Installation completed"

setup(
    name='cloudscraper_osse',
    version='0.0.1',
    description='The Python/C++ search engine with a Google-like frontend and Wordpress-like backend.',
    author='Bratislav Stojanovic',
    author_email='bratislav1983@gmail.com',
    url='http://www.cloudscraper.ca/',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='google wordpress python django search engine',
    license='Bratislav Stojanovic',
    packages=['cloudscraper_osse',],
    install_requires=[
        'APScheduler',
    ],
    cmdclass={'install': CustomInstall},
)

