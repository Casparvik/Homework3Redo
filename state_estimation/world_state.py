#!/usr/bin/env python3

import numpy as np


# Keep track of the doors
class WorldState:
    def __init__(self):

        # Door configurations
        self.random_door_placement()
        self.set_wall_SD(0.1)

    def random_door_placement(self, n_doors = 3, n_bins = 20):
        """ Randomly place the doors """

        div = 1 / n_bins
        door_loc = np.zeros( int(n_bins) )
        while sum(door_loc) < n_doors:
            loc = np.random.uniform(0,1)
            i_loc = min(int(n_bins), max(0, int(np.floor( loc / div))))
            door_loc[i_loc] = 1

        self.door_width = div * 1.1
        self.doors = []
        for i in range(0,len(door_loc)):
            if door_loc[i]:
                self.doors.append( (i+0.5)*div )


    # Place the robot in front of the first door (testing routine)
    def place_robot_in_front_of_door(self):
        return self.doors[0]

    # Place the robot NOT in front of the first door (testing routine)
    def place_robot_NOT_in_front_of_door(self):
        div = self.door_width / 1.1

        b_found_no_door = False
        robot_loc = div/2
        while b_found_no_door == False:
            if self.is_in_front_of_door(robot_loc) == False:
                b_found_no_door = True
            else:
                robot_loc += div

        return robot_loc

    # Determine if position is in front of door
    def is_in_front_of_door(self, robot_loc):
        """
        Checks if robot overlaps door
        :param x_loc - x_loc value from 0 to 1, robot location
        :return: If robot overlaps door
        """
        # Based on width of door overlap of robot and door
        door_width = self.door_width / 2

        # Determine percentage in front of door
        inside_door = [abs(robot_loc - d) < door_width for d in self.doors]
        if True in inside_door:
            return True
        return False

    # Distance to closest door
    def closest_door(self, robot_loc):
        dists = [abs(robot_loc-d) for d in self.doors]
        return np.min(dists)

    def set_wall_SD(self, standard_deviation):
        self.wall_SD = standard_deviation

    def query_wall(self, rs):
        """ Return a distance reading (with correct noise)
        :param rs - robot state (for actual robot location) """
        loc = rs.robot_loc

        # Generate a sensor reading by adding appropriate noise
        noise = np.random.normal(0, self.wall_SD)

        return loc + noise

if __name__ == '__main__':
    ws = WorldState()

    ws.random_door_placement(3,20)

    for d in ws.doors:
        for dw in np.linspace( d - 0.49 * ws.door_width, d + 0.49 * ws.door_width):
            if ws.is_in_front_of_door( dw ) == False:
                raise ValueError("Should be in front of door {}".format(dw))

    print( "Passed tests")
