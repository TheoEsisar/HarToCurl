"""
Author: TheoEsisar

Description: This script parses an HAR file and generates curl commands for each request in the file.
The curl commands are printed to the console or written to an output file if specified.

Usage: python script.py <file_path> [--output <output_file>]
"""

import json
import argparse
import urllib.parse

def parse_har_file(file_path):
  """
  Parse a HAR file and return the entries.
  """
  try:
      with open(file_path, 'r', encoding='utf-8') as f:
          har_data = json.load(f)
  except FileNotFoundError:
      print(f"Error: File {file_path} not found.")
      exit(1)
  except json.JSONDecodeError:
      print(f"Error: File {file_path} is not a valid JSON file.")
      exit(1)

  try:
      entries = har_data['log']['entries']
  except KeyError:
      print(f"Error: File {file_path} does not have the expected format.")
      exit(1)

  return entries

def generate_curl_command(entry):
  """
  Generate a curl command from a HAR entry.
  """
  request = entry['request']
  method = request['method']
  url = urllib.parse.quote_plus(request['url'])
  headers = request.get('headers', [])
  body = request.get('postData', {}).get('text', '')

  curl_command = f"curl -X {method} '{url}'"

  for header in headers:
      curl_command += f" -H '{header['name']}: {header['value']}'"

  if body:
      curl_command += f" -d '{body}'"

  return curl_command

def main():
  """
  Main function to parse a HAR file and print the curl commands.
  """
  parser = argparse.ArgumentParser(description='Parse a HAR file and print the curl commands.')
  parser.add_argument('file_path', type=str, help='Path to the HAR file.')
  parser.add_argument('--output', type=argparse.FileType('w'), help='Output file. If not provided, the curl commands will be printed to the console.')
  args = parser.parse_args()

  entries = parse_har_file(args.file_path)
  for entry in entries:
      curl_command = generate_curl_command(entry)
      if args.output:
          args.output.write(curl_command + "\n")
      else:
          print(curl_command)
          print("\n")

if __name__ == "__main__":
  main()
