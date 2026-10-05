import argparse

def parse_cli_args():

   # decalre the parser
   parser = argparse.ArgumentParser(description="Run a configured OpsRunner Job") 
   parser.add_argument("job_name", help="Name of the configured job to run")

   return parser.parse_args()