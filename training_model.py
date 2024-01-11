import pygame
import random
import numpy as np
import csv

# Initialize pygame and game parameters
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Avoid the Falling Obstacles!")
pygame.event.pump()  
player_size = 50
player_pos = [screen_width // 2, screen_height - 2 * player_size]
enemy_size = 50
player_speed = 10
clock = pygame.time.Clock()

# Q-learning parameters
learning_rate = 0.1
discount_factor = 0.95
exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay_rate = 0.001
n_actions = 3  # Left, Stay, Right

# Q-table initialization
state_size = (screen_width // player_size, screen_height // player_size)
q_table = np.zeros((state_size[0], state_size[1], n_actions))

# Function to get the current state
def get_state(player_pos):
    x = player_pos[0] // player_size
    y = player_pos[1] // player_size
    return x, y

# Function to take an action
def take_action(state, exploration_rate):
    if random.uniform(0, 1) < exploration_rate:
        action = random.randint(0, 2)  # Explore: select a random action
    else:
        action = np.argmax(q_table[state])  # Exploit: select the action with max value
    return action

# Function to update Q-table
def update_q_table(state, action, reward, new_state, done):
    old_value = q_table[state][action]
    next_max = np.max(q_table[new_state])

    # Q-learning formula
    new_value = (1 - learning_rate) * old_value + learning_rate * (reward + discount_factor * next_max)
    q_table[state][action] = new_value

    if done:
        exploration_rate = min_exploration_rate + \
            (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate * episode)

# Main game loop
for episode in range(1000):  # Number of games the agent should play
    player_pos = [screen_width // 2, screen_height - 2 * player_size]
    enemies = [{'pos': [random.randint(0, screen_width - enemy_size), 0], 'speed': random.randint(5, 10)} for _ in range(3)]
    state = get_state(player_pos)
    done = False

    while not done:
        # Take action based on the current state
        action = take_action(state, exploration_rate)

        # Move the player based on the action
        if action == 0:
            player_pos[0] -= player_speed
        elif action == 2:
            player_pos[0] += player_speed

        # Update enemy positions and check for collision
        for enemy in enemies:
            enemy['pos'][1] += enemy['speed']
            if enemy['pos'][1] >= screen_height:
                enemy['pos'] = [random.randint(0, screen_width - enemy_size), 0]
                enemy['speed'] = random.randint(5, 10)
            if (player_pos[0] < enemy['pos'][0] + enemy_size and 
                player_pos[0] + player_size > enemy['pos'][0] and
                player_pos[1] < enemy['pos'][1] + enemy_size and 
                player_pos[1] + player_size > enemy['pos'][1]):
                done = True  # End game on collision

        # Get new state and update Q-table
        new_state = get_state(player_pos)
        reward = 1 if not done else -100
        update_q_table(state, action, reward, new_state, done)
        state = new_state

        # Rendering and screen updates
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 0, 255), (player_pos[0], player_pos[1], player_size, player_size))
        for enemy in enemies:
            pygame.draw.rect(screen, (255, 0, 0), (enemy['pos'][0], enemy['pos'][1], enemy_size, enemy_size))
        pygame.display.update()
        clock.tick(30)

    # Exploration rate decay
    exploration_rate = min_exploration_rate + \
        (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate * episode)

pygame.quit()
