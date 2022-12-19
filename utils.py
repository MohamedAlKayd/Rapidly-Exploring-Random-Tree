import argparse

# Function to get the Arguements from the command line
def get_args():

    # Create Arguement Parser Object
    parser = argparse.ArgumentParser()

    # Arguement 1
    parser.add_argument('--world', type=str, default="simple.png")

    # Arguement 2
    parser.add_argument('--step_size', type=int, default=6)

    # Arguement 3
    # Uniform sampling for the Rapidly-Exploring Random Tree
    parser.add_argument('--rrt_sampling_policy', type=str, default="uniform")

    # Argument 4
    # Simple Point Robot Start Position X coordinate
    parser.add_argument('--start_pos_x', type=int, default=10)

    # Arguement 5
    # Simple Point Robot Start Position Y coordinate
    parser.add_argument('--start_pos_y', type=int, default=270)

    # Arguement 6
    # No theta angle used for Simple Point Robot Start Position
    parser.add_argument('--start_pos_theta', type=float, default=0)

    # Arguement 7
    # Simple Point Robot Target Position X coordinate
    parser.add_argument('--target_pos_x', type=int, default=900)

    # Arguement 8
    # Simple Point Robot Target Position Y coordinate
    parser.add_argument('--target_pos_y', type=int, default=30)

    # Arguement 9
    # No theta angle used for Simple Point Robot Target Position
    parser.add_argument('--target_pos_theta', type=float, default=0)

    # Arguement 10
    # Line robot length = 25 pixels
    # Run with lengths = 5 --> 50 in increments of 5
    parser.add_argument('--robot_length', type=int, default=25)

    # Arguement 11
    # Different seed --> Different paths
    parser.add_argument('--seed', type=int, default=0)

    # Arguement 12
    parser.add_argument('--visualize', type=int, default=1)

    # Argument Parser Object parses arguements through the parse_args() method
    # Command line arguement --> Convert to appropriate type --> invoke appropriate action
    args = parser.parse_args()

    # Return the arguements from the command line
    return args