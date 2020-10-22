"""Simple travelling salesman problem between cities."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import pandas as pd
import numpy as np


def create_data_model():
    
    # data = pd.read_excel(r'data fixx.xlsx')

    # f1 = pd.DataFrame(data, columns = ['slg'])
    # f2 = pd.DataFrame(data, columns = ['goa_maria'])
    # f3 = pd.DataFrame(data, columns = ['kebun_matahari'])
    # f4 = pd.DataFrame(data, columns = ['goa_selomangleng'])
    # f5 = pd.DataFrame(data, columns = ['gunung_klotok'])
    # f6 = pd.DataFrame(data, columns = ['bdi'])
    # f7 = pd.DataFrame(data, columns = ['alun_kediri'])
    # f8 = pd.DataFrame(data, columns = ['taman_sekartaji'])
    # f9 = pd.DataFrame(data, columns = ['klenteng'])
    
    # data = np.hstack((f1,f2,f3,f4,f5,f6,f7,f8,f9))
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = [
        [0.0,	15.6,	12.8,	11.8,	18.7,	17.4,	8.2,	10.0,	7.8],
        [15.6,	0.0,	8.3,	8.6,	18.5,	17.3,	7.3,	8.0,	8.4],
        [12.8,	8.3,	0.0,	0.7,	13.4,	12.1,	5.9,	4.7,	6.1],
        [11.8,	8.6,	0.7,	0.0,	13.8,	12.5,	6.3,	5.0,	6.4],
        [18.7,	18.5,	13.4,	13.8,	0.0,	6.4,	15.1,	12.4,	15.3],
        [17.4,	17.3,	12.1,	12.5,	6.4,	0.0,	14.4,	11.8,	14.6],
        [8.2,	7.3,	5.9,	6.3,	15.1,	14.4,	0.0,	2.5,	0.9],
        [10.0,	8.0,	4.7,	5.0,	12.4,	11.8,	2.5,	0.0,	2.9],
        [7.8,	8.4,	6.1,	6.4,	15.3,	14.6,	0.9,	2.9,	0.0],
    ]  # yapf: disable
    data['num_vehicles'] = 1
    data['depot'] = 5
    return data


def print_solution(manager, routing, assignment):
    """Prints assignment on console."""
    print('Objective: {} miles'.format(assignment.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = assignment.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Route distance: {}Km\n'.format(route_distance)


def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if assignment:
        print_solution(manager, routing, assignment)


if __name__ == '__main__':
    main()