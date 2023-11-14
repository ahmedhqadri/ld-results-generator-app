from dotenv import load_dotenv #pip install python-dotenv
import ldclient
from ldclient import Config, ExecutionOrder, MigratorBuilder, Result, Stage
from ldclient.config import Config
import json
import names
import os
import random
import time
import uuid
import logging
import sys
from ldclient import Context

global client

def init_LD_client(sdk_key): 
    client = ldclient.set_config(Config(sdk_key))

def generate_results(data_store):

    num_contexts = 10000
    for i in range(num_contexts):
        
        context = create_multi_context()
        flag_variation = ldclient.get().variation(data_store["flag_key"], context, False)
        metrics = data_store["metrics"]
        percentages = data_store["percentages"]
        converted = True

        for metric, percentage in zip(metrics, percentages):
            
            if converted == True:
                converted = execute_call_if_converted(metric, percentage, context)

    return True

def execute_call_if_converted(metric, percent_chance, context):
    context_name = context.get('name')
    if conversion_chance(int(percent_chance)):
        ldclient.get().track(metric, context)
        print(f"User {context_name} converted for {metric}")
        return True
    else:
        print(f"User {context_name} did NOT convert for {metric}")
        return False


'''
Chance Converted for a metric
'''
def conversion_chance(chance_number):
    chance_calc = random.randint(1, 100)
    if chance_calc <= chance_number:
        return True
    else:
        return False

'''
Construct a user context
'''
def create_user_context():
  user_key = "usr-" + str(uuid.uuid4())
  name = f'{names.get_first_name()} {names.get_last_name()}'
  plan = random.choice(['platinum', 'silver', 'gold', 'diamond'])
  role = random.choice(['reader', 'writer', 'admin'])
  metro = random.choice(['New York', 'Chicago', 'Minneapolis', 'Atlanta', 'Los Angeles', 'San Francisco', 'Denver', 'Boston'])

  user_context = Context.builder(user_key) \
  .set("kind", "user") \
  .set("name", name) \
  .set("plan", plan) \
  .set("role", role) \
  .set("metro", metro) \
  .build()

  return user_context

'''
Construct a device context
'''
def create_device_context():
  device_key = "dvc-" + str(uuid.uuid4())
  os = random.choice(['Android', 'iOS', 'Mac OS', 'Windows'])
  version = random.choice(['1.0.2', '1.0.4', '1.0.7', '1.1.0', '1.1.5'])
  type = random.choice(['Fire TV', 'Roku', 'Hisense', 'Comcast', 'Verizon', 'Browser'])

  device_context = Context.builder(device_key) \
  .set("kind", "device") \
  .set("os", os) \
  .set("type", type) \
  .set("version", version) \
  .build()

  return device_context


'''
Construct an organization context
'''
def create_organization_context():
  org_key = "org-" + str(uuid.uuid4())
  # name = fake.company()
  key_name = random.choice([
    {"key": "org-7f9f58eb-c8e8-4c40-9962-43b13eeec4ea", "name": "Mayo Clinic"}, 
    {"key": "org-40fad050-3f91-49dc-8007-33d02f1869e0", "name": "IBM"}, 
    {"key": "org-fca878d0-3cab-4301-91da-bbc6dbb08fff", "name": "3M"}
    ])
  region = random.choice(['NA', 'CN', 'EU', 'IN', 'SA'])

  org_context = Context.builder(key_name["key"]) \
  .set("kind", "organization") \
  .set("name", key_name["name"]) \
  .set("region", region) \
  .build()

  return org_context

'''
Construct a multi context: User, Device, and Organization
'''
def create_multi_context():

  multi_context = Context.create_multi(
  create_user_context(),
  create_device_context(),
  create_organization_context()
  )

  return multi_context


def write_new():
    def randomizer(error_rate):
        new_rate = error_rate['new']
        value = random.randint(1, 1000)
        # Intentional pause to simulate write latency
        time.sleep(.2)
        if value >= new_rate:
            print("NEW WRITE: SUCCESS")
            return Result.success("WRITE: SUCCESS")
        else:
            print("NEW WRITE: FAIL")
            return Result.fail("WRITE: FAIL")
    return randomizer

def write_old():
    def randomizer(error_rate):
        old_rate = error_rate['old']
        value = random.randint(1, 1000)
        # Intentional pause to simulate write latency
        time.sleep(.35)
        if value >= old_rate:
            print("OLD WRITE: SUCCESS")
            return Result.success("WRITE: SUCCESS")
        else:
            print("OLD WRITE: FAIL")
            return Result.fail("WRITE: FAIL")
    return randomizer

def read_new():
    def randomizer(error_rate):
        new_rate = error_rate['new']
        value = random.randint(1, 1000)
        # Intentional pause to simulate read latency
        time.sleep(.2)
        if value >= new_rate:
            # Add an additional check on succesful read to determine whether this will be consistent with the other read
            consistency_value = random.randint(1, 1000)
            if consistency_value <= 998:
                print("NEW READ: CONSISTENT")
                return Result.success("READ: CONSISTENT")
            else: 
                print("NEW READ: INCONSISTENT")
                return Result.success("READ: INCONSISTENT")
        else:
            print("NEW READ: FAIL")
            return Result.fail("READ: FAIL")
    return randomizer

def read_old():
    def randomizer(error_rate):
        old_rate = error_rate['old']
        value = random.randint(1, 1000)
        # Intentional pause to simulate read latency
        time.sleep(.4)
        if value >= old_rate:
            # Add an additional check on succesful read to determine whether this will be consistent with the other read
            consistency_value = random.randint(1, 1000)
            if consistency_value <= 998:
                print("OLD READ: CONSISTENT")
                return Result.success("READ: CONSISTENT")
            else: 
                print("OLD READ: INCONSISTENT")
                return Result.success("READ: INCONSISTENT")
        else:
            print("OLD READ: FAIL")
            return Result.fail("READ: FAIL")
    return randomizer

def consistency_check():
    def check_consistency(a, b):
        if a == b:
            print("Consistency: TRUE")
            return True
        else:
            print("Consistency: FALSE")
            return False
    return check_consistency

def migration_builder():

  ld_logger = logging.getLogger("ldclient")
  ld_logger.setLevel(logging.ERROR)

  handler = logging.StreamHandler(sys.stdout)
  handler.setLevel(logging.ERROR)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  handler.setFormatter(formatter)
  ld_logger.addHandler(handler)
  
  builder = MigratorBuilder(ldclient.get())
  builder.read(read_old(), read_new(), consistency_check())
  builder.write(write_old(), write_new())
  builder.read_execution_order(ExecutionOrder.PARALLEL)

  migrator = builder.build()

  return migrator