# Results Generator App for LaunchDarkly

Inspired by : https://github.com/ttotenberg-ld/ld_funnel_experiment_runner, https://github.com/ttotenberg-ld/ld_migration_runner

This app consists of the following generator tools: 
- Funnel Experiment: Creates results for funnel experiment using metrics and percentage converted
- Migration Runner: Generates migration insights for your migration feature flag

## Setup / Running 
- Open Terminal
- Clone This Repo
- Run ```docker run -p 5002:5002 --rm -it $(docker build -q .)```
- Open browser to http://localhost:5002
- Close terminal when completed - this will remove the container

## Variables:
- SDK Key: Your LD server-side SDK Key (Required)
- Flag Key: Your LD flag key used in the experiment (Required)
- Metrics: Individual metrics part of the funnel experiment
- Percentage Converted: Number from range 1 - 100 where probability to convert metric increases as number gets closer to 100.
