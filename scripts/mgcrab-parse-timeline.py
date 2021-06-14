import sys
import os
import csv

if len(sys.argv) < 3:
  print("Usage: ", sys.argv[0], " [Client Log Directory] [Output Directory]")
  exit(1)

# Inputs
CLIENT_LOG_DIR = sys.argv[1]
OUTPUT_DIR = sys.argv[2]

# Functions
def to_numbers(line):
  start_idx = line.find(':')
  tokens = line[start_idx + 1:].split(',')
  numbers = []
  for token in tokens:
    numbers.append(int(token.strip()))
  return numbers

# Read per-node throughput and latency
throughput_timelines = []
latency_timelines = []
for file_name in os.listdir(CLIENT_LOG_DIR):

  with open("{}\{}".format(CLIENT_LOG_DIR, file_name)) as file:
    throughput_timeline = {}
    latency_timeline = {}

    for line in file:
      # Get the time
      if 'Statistics at' in line:
        start_idx = line.find(' at ')
        end_idx = line.find(' second ')
        time = int(line[start_idx + 4: end_idx].strip())

      # Throughput
      if 'Each Node Throughput' in line:
        throughputs = to_numbers(line)
        throughput_timeline[time] = throughputs
      
      # Latency
      if 'Each Node Average Latency' in line:
        latencies = to_numbers(line)
        latency_timeline[time] = latencies
  
  throughput_timelines.append(throughput_timeline)
  latency_timelines.append(latency_timeline)

# Get the sorted time list
times = list(throughput_timelines[0].keys())
times.sort()

# Get the server and client count
client_count = len(throughput_timelines)
server_count = len(throughput_timelines[0][times[0]])

# Output per-node throughput timeline
with open("{}\{}".format(OUTPUT_DIR, 'throughput.csv'), 'w', newline='') as file:
  writer = csv.writer(file)

  # Output the header
  header = ['Time']
  for server in range(0, server_count):
    header.append('Server {}'.format(server))
  writer.writerow(header)

  for time in times:
    throughputs = [0] * server_count

    # Merge the throughputs
    for client in range(0, client_count):
      for server in range(0, server_count):
        throughputs[server] += throughput_timelines[client][time][server]

    # Output a row
    writer.writerow([time] + throughputs)

# Output overall latency timeline
with open("{}\{}".format(OUTPUT_DIR, 'latency.csv'), 'w', newline='') as file:
  writer = csv.writer(file)

  # Output the header
  writer.writerow(['Time', 'Average Latency'])

  for time in times:
    total_latency = 0
    total_throughput = 0

    # Calculate average latency
    for client in range(0, client_count):
      for server in range(0, server_count):
        throughput = throughput_timelines[client][time][server]
        total_latency += throughput * latency_timelines[client][time][server]
        total_throughput += throughput

    # Output a row
    if total_latency == 0:
      writer.writerow([time, total_latency])
    else:
      writer.writerow([time, total_latency / total_throughput])
