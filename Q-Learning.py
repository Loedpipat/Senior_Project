import requests
import random
import time
import json
import urllib3
from requests.auth import HTTPBasicAuth

# Suppress SSL warnings and disable certificate verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define constants for ODL controller and authentication
ODL_IP = '192.168.56.201' 
ODL_PORT = '8181'
USERNAME = 'admin'
PASSWORD = 'admin'

# Parameters for Q-learning
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EPISODES = 300
EXPLORATION_RATE = 1.0  # Declare this variable before usage
EXPLORATION_DECAY = 0.995

# Initialize Q-table
q_table = {}

# Function to fetch OpenFlow data from ODL controller with retry logic
def fetch_openflow_data():
    url = f"http://{ODL_IP}:{ODL_PORT}/restconf/operational/opendaylight-inventory:nodes"  # ใช้ HTTP แทน HTTPS
    
    try:
        # Use requests without SSLAdapter for simplicity
        response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), headers={"Accept": "application/json"}, verify=False)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching data: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {e}")
        return None

# Reward function based on duration, n_bytes, and n_packets
def calculate_reward(duration, n_bytes, n_packets, congestion_factor=1):
    # Duration time: short duration (fast flow) is better
    duration_penalty = max(0, duration - 100)  # Penalize long durations (e.g., > 100 seconds)

    # n_bytes and n_packets: more is better (for throughput)
    throughput_reward = n_bytes / (duration + 1)  # Reward for more bytes sent in less time
    packet_count_reward = n_packets / (duration + 1)  # Reward for more packets sent in less time

    # Congestion penalty: apply when there is congestion (e.g., long duration or low throughput)
    congestion_penalty = congestion_factor * (duration_penalty + (n_bytes < 5000))  # Apply heavier penalty if throughput is low

    # Total reward: Combine throughput reward, packet count reward, and congestion penalty
    reward = throughput_reward + packet_count_reward - congestion_penalty
    return reward

# Get possible actions for each state (you need to define these actions)
def get_possible_actions(state):
    actions = ['Increase Priority', 'Decrease Priority', 'Modify Actions', 'Keep Same']
    return actions

# Update the Q-table based on the Q-learning formula
def update_q_table(q_table, state, action, reward, next_state):
    best_next_action = max(q_table.get(next_state, {}), key=q_table.get(next_state, {}).get, default=None)
    q_value = q_table.get(state, {}).get(action, 0) + LEARNING_RATE * (reward + DISCOUNT_FACTOR * q_table.get(next_state, {}).get(best_next_action, 0) - q_table.get(state, {}).get(action, 0))
    if state not in q_table:
        q_table[state] = {}
    q_table[state][action] = q_value

# Update OpenFlow flow entries in the ODL controller (stub function)
def update_openflow_flow(node_id, state, action):
    flow_id = state[0]  # Flow ID from state
    cookie = state[1]  # Get the cookie from the state (use the cookie from the existing flow)

    if action == 'Increase Priority':
        priority = 50
    elif action == 'Decrease Priority':
        priority = 5
    else:
        priority = 2

    flow_data = {
        "flow-node-inventory:flow": [
            {
                "id": flow_id,
                "cookie": cookie,  # Set the cookie to the existing flow's cookie
                "table_id": 0,
                "priority": priority,
                "match": {
                    "in-port": "1"
                },
                "instructions": {
                    "instruction": [
                        {
                            "order": 0,
                            "apply-actions": {
                                "action": [
                                    {
                                        "order": 0,
                                        "output-action": {
                                            "output-node-connector": "1"
                                        }
                                    },
                                    {
                                        "order": 1,
                                        "output-action": {
                                            "output-node-connector": "2"
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        ]
    }

    url_put = f"http://{ODL_IP}:{ODL_PORT}/restconf/config/opendaylight-inventory:nodes/node/{node_id}/flow-node-inventory:table/0/flow/{flow_id}"  # ใช้ HTTP
    response_put = requests.put(url_put, auth=HTTPBasicAuth(USERNAME, PASSWORD), json=flow_data, headers={"Content-Type": "application/json"}, verify=False)

    if response_put.status_code == 200 or response_put.status_code == 201:
        print(f"Successfully updated flow {flow_id} with cookie {cookie}!")
    else:
        print(f"Failed to update flow {flow_id}. Status code: {response_put.status_code}")
        print(response_put.text)


# Q-learning loop
def q_learning():
    global EXPLORATION_RATE
    episode_times = []  # List to store time for each episode

    for episode in range(EPISODES):
        start_time = time.time()  # Start timing the episode

        print(f"Episode {episode + 1}/{EPISODES} started...")

        openflow_data = fetch_openflow_data()
        if not openflow_data:
            break

        for node in openflow_data['nodes']['node']:
            node_id = node['id']

            if node_id in [f"openflow:{i}" for i in range(1, 11)]:
                print(f"Fetching flows for node: {node_id}")

                for table in node['flow-node-inventory:table']:
                    table_id = table['id']

                    # Only process flow entries where 'priority' exists and priority != 0
                    if table_id == 0:
                        for flow in table['flow']:
                            if "#" not in flow['id']:
                                flow_id = flow['id']
                                priority = flow['priority']
                                match = flow['match']

                                # Get flow statistics such as duration, bytes, and packet count
                                flow_stats = flow.get("opendaylight-flow-statistics:flow-statistics", {})
                                duration = flow_stats.get("duration", {}).get("second", 0)
                                n_bytes = flow_stats.get("byte-count", 0)
                                n_packets = flow_stats.get("packet-count", 0)

                                state = (flow_id, flow['cookie'], json.dumps(match))  # Add cookie to state

                                # Initialize Q-table if not already present
                                if state not in q_table:
                                    q_table[state] = {action: 0 for action in get_possible_actions(state)}

                                # Calculate the reward based on flow statistics
                                reward = calculate_reward(duration, n_bytes, n_packets)

                                # Select action using epsilon-greedy policy
                                if random.uniform(0, 1) < EXPLORATION_RATE:
                                    action = random.choice(get_possible_actions(state))  # Exploration
                                else:
                                    action = max(q_table[state], key=q_table[state].get)  # Exploitation

                                # Get next state (for simplicity, assume the same state here for the demonstration)
                                next_state = state

                                # Update Q-table with the chosen action and reward
                                update_q_table(q_table, state, action, reward, next_state)

                                # Optionally, update OpenFlow flow entry based on action (simulated, real implementation needed)
                                update_openflow_flow(node_id, state, action)

        # Calculate and store time taken for this episode
        episode_duration = time.time() - start_time
        episode_times.append(f"Episode {episode + 1}/{EPISODES}: {int(episode_duration)}s")

        # Decay exploration rate
        EXPLORATION_RATE *= EXPLORATION_DECAY

        time.sleep(1)  # Simulate waiting before the next iteration

    # Print all episode times after completion
    print("\nEpisode times:")
    for episode_time in episode_times:
        print(episode_time)


# Run Q-learning
q_learning()
