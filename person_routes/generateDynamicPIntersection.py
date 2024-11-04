import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import random

edges = [
    "1174874706", "-917450542", "-4588647", "1112806233", "4588647"
]
edges_to_remove = [
    
]
edges = [edge for edge in edges if edge not in edges_to_remove]




def prettify_element(element):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def generate_single_person_flow(route_file):
    # Create the root element
    routes = ET.Element('routes')

    # Generate individual passengers
    person_id_counter = 1
    people = []
    for _ in range(300):  # Adjust the number of passengers if needed
        passenger_type = random.choice(['rider', 'stander', 'walker'])
        #passenger_type = 'stander'
        depart_time = random.randint(0, 6500)
        if passenger_type == 'rider':
            start_edge_idx = random.randint(0, len(edges) - 2)
            end_edge_idx = random.randint(start_edge_idx + 1, len(edges) - 1)

            start_edge = edges[start_edge_idx]
            end_edge = edges[end_edge_idx]
            while start_edge == end_edge:
                end_edge = random.choice(edges)
            
            person = ET.Element('person', attrib={
                'id': f'person_{person_id_counter}',
                'depart': str(depart_time),
                'departLane': 'random',
                'departSpeed': '1.00',
                'color': '0,1,0'
            })
            
            ET.SubElement(person, 'walk', attrib={
                'from': start_edge,
                'busStop': start_edge,
                'speed': '1.5',
                
            })
            
            ET.SubElement(person, 'ride', attrib={
                'line': 'trad_line',
                'busStop': start_edge,
                'to': end_edge,
            })
            
            ET.SubElement(person, 'walk', attrib={
                'edges': end_edge,
                'speed': '1.5',
            })
        
        elif passenger_type == 'stander':
            start_edge_idx = random.randint(0, len(edges) - 2)
            end_edge_idx = random.randint(start_edge_idx + 1, len(edges) - 1)

            start_edge = edges[start_edge_idx]
            end_edge = edges[end_edge_idx]
            while start_edge == end_edge:
                end_edge = random.choice(edges)
            
            person = ET.Element('person', attrib={
                'id': f'person_{person_id_counter}',
                'depart': str(depart_time),
                'departLane': 'random',
                'departSpeed': '1.00',
                'color': '1,0,1'
            })
            ET.SubElement(person, 'walk', attrib={
                'from': start_edge,
                'busStop': start_edge,
                'speed': '1.5',
            })
            
            ET.SubElement(person, 'stop', attrib={
                'busStop': start_edge,
                'duration': str(random.randint(30,600)),
            })
        
        elif passenger_type == 'walker':
            start_edge_idx = random.randint(0, len(edges) - 2)
            end_edge_idx = random.randint(start_edge_idx + 1, len(edges) - 1)

            start_edge = edges[start_edge_idx]
            end_edge = edges[end_edge_idx]
            while start_edge == end_edge:
                end_edge = random.choice(edges)
            
            person = ET.Element('person', attrib={
                'id': f'person_{person_id_counter}',
                'depart': str(depart_time),
                'departLane': 'random',
                'departSpeed': '1.00',
                'color': '1,0,0'
            })
            ET.SubElement(person, 'walk', attrib={
                'from':start_edge,
                'busStop':start_edge,
                'speed': '1.5',
            })
            
            ET.SubElement(person, 'stop', attrib={
                'busStop': start_edge,
                'duration': str(random.randint(30,600)),
            })

            ET.SubElement(person, 'walk', attrib={
                'from':start_edge,
                'to':end_edge,
                'speed': '1.5',
            })

        people.append((depart_time, person))
        person_id_counter += 1

    # Sort the people by depart time
    people.sort(key=lambda x: x[0])

    # Append sorted people to the routes element
    for _, person in people:
        routes.append(person)

    # Write to XML file
    with open(route_file, 'w') as f:
        f.write(prettify_element(routes))

# Generate the personFlows for the given route file
generate_single_person_flow("intersection_flows.rou.xml")