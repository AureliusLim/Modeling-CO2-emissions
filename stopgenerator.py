def generate_bus_stop_xml(route_edges, output_file):
    edges = route_edges.split()
    with open(output_file, 'w') as f:
        f.write('<busStops>\n')
        for edge in edges:
            edge_id = edge.split(' ')[0]
            bus_stop_id = edge_id
            x_pos = 0.0  # Start position
            y_pos = 10.0  # End position
            lane = f"{edge}_1"  # Lane parameter
            
            f.write(f'\t<busStop id="{bus_stop_id}" x="{x_pos}" y="{y_pos}" lane="{lane}"/>\n')
        
        f.write('</busstops>')

# Example usage:
jeepney_route_edges = "1174874706 -917450542 -4588647 1112806233 775437708 4588647"
output_file = "bus_stops.xml"

generate_bus_stop_xml(jeepney_route_edges, output_file)
