# Funnel Experiment Generator

Inspired by : https://github.com/ttotenberg-ld/ld_funnel_experiment_runner

This tool will help generate results for Funnel Experiments in LaunchDarkly

## Setup / Running 
- Open Terminal
- Clone This Repo
- Run ```docker run -p 5002:5002 --rm -it $(docker build -q .)```
- Open browser to http://localhost:5002
- Close terminal when completed - this will remove the container

## Variables:
- SDK Key: Your LD server-side SDK Key
- Flag Key: Your LD flag key used in the experiment
- Metrics: Individual metrics part of the funnel experiment
- Percentage Converted: Number from range 1 - 100 where probability to convert metric increases as number gets closer to 100.
