from PyInfinity.init import getVersion, getLicense, getLocalTime, getAuthor, getContributors, getCopyright
from . import printAllDataOfPyInfinity
import argparse

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()

    # Define the version argument
    argparser.add_argument(
        '-v', '-vn', '--version', 
        action='version', 
        version=getVersion())  # Specify the version here

    # Define other arguments
    argparser.add_argument(
        '-aff', '-adf', '--alldfpyinf', 
        action='store_true', 
        help="Print all data of PyInfinity")
    
    argparser.add_argument(
        '-ls', '--license', 
        action='store_true', 
        help="Show the license information")
    
    argparser.add_argument(
        '-lt', '--localtime', 
        action='store_true', 
        help="Show local time")
    
    argparser.add_argument(
        '-ar', '--author', 
        action='store_true', 
        help="Show author information")
    
    argparser.add_argument(
        '-cn', '--contributors', 
        action='store_true', 
        help="Show contributors information")
    
    argparser.add_argument(
        '-cp', '--copyright', 
        action='store_true', 
        help="Show copyright information")

    # Parse arguments
    args = argparser.parse_args()

    # Now just check for the other arguments that we need to handle
    if args.license: 
        print(getLicense())
    if args.localtime: 
        print(getLocalTime())
    if args.author: 
        print(getAuthor())
    if args.contributors: 
        print(getContributors())
    if args.copyright: 
        print(getCopyright())
    if args.alldfpyinf: 
        printAllDataOfPyInfinity()