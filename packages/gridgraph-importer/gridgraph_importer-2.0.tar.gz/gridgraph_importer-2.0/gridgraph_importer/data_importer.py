#!./python/bin/python3
# -*- coding: UTF-8 -*-

from gremlin_python.driver import client
from gridgraph_importer import log_utils
import sys
import os
import json
import csv
from os import listdir
from os.path import isfile, join

log_file_name, log = log_utils.init_runtime_logger('bulk_load', 'gremlin_client')
print('log file: %s\n' % log_file_name, file=sys.stderr)

graph_struct_file_name = 'graphStruct.json'
bulk_load_csv_file_name = 'bulkloadCsv.json'
graph_name_key = 'graphName'
primary_key_key = 'primaryKey'
default_schema_key = 'defaultSchema'
schemas_key = 'schemas'
name_key = 'name'
type_key = 'type'
properties_key = 'properties'
unique_key = 'unique'
nullable_key = 'nullable'
indexs_key = 'indexs'
index_name_key = 'indexName'
property_indexs_key = 'propertyIndexs'
schema_name_key = 'schemaName'
property_name_key = 'propertyName'
direction_key = 'direction'

connection_key = 'connection'
source_csv_key = 'sourCsv'
csv_splitter_char_key = 'csvSpliteChar'
csv_folder_path_key = 'csvFolderPath'
vertexes_key = 'vertexes'
file_name_key = 'fileName'
field_map_key = 'fieldMap'
edges_key = 'edges'
from_vertex_key = 'fromVertex'
to_vertex_key = 'toVertex'

GRAPH_INFO = {}
VERTEX = 'VERTEX'
EDGE = 'EDGE'
VERTEX_SCHEMA_PROPERTY_TYPE = {}
EDGE_SCHEMA_PROPERTY_TYPE = {}
VERTEX_SCHEMA_TO_CSV = {}
EDGE_SCHEMA_TO_CSV = {}
VERTEX_SCHEMA_FIELDS = {}
EDGE_SCHEMA_FIELDS = {}
EDGE_FROM_TO_VERTEX = {}


class GremlinClient:
    def __init__(self, server_ip, port, username, password):
        self._server_ip = server_ip
        self._port = port
        self._username = username
        self._password = password
        self._address = "ws://{0}:{1}/gremlin".format(server_ip, port)

    def send_gremlin_script(self, gremlin_script):
        session = client.Client(self._address, None, username=self._username, password=self._password)
        result_set = session.submit(gremlin_script)
        results = result_set.all().result()
        log.info("results=%s", results)
        session.close()


def import_csv_data(server_ip, port, data_dir, username='admin', password='admin'):
    check_csv_data_dir(data_dir)
    gremlin_client = GremlinClient("127.0.0.1", 8381, "admin", "admin")
    schema_script = parse_graph_struct_file(data_dir)
    gremlin_client.send_gremlin_script(schema_script)

    parse_bulk_load_csv_mapping_file(data_dir)

    data_scripts = parse_data_file(data_dir)
    log.info('start import data')
    for ds in data_scripts:
        log.info(ds)
        gremlin_client.send_gremlin_script(ds)

    gremlin_client.send_gremlin_script("GridGraphFactory.listGraph()")


def check_csv_data_dir(data_dir):
    log.info("check csv data dir.")
    if not os.path.isdir(data_dir):
        log.error("data dir is not exist. [data_dir=%s]", data_dir)
        return
    graph_struct_file = os.path.join(data_dir, "graphStruct.json")
    if not graph_struct_file:
        log.error("graph struct json file is not exist. [graph_struct_file={}]", graph_struct_file)
        return


def parse_graph_struct_file(data_dir) -> str:
    log.info("parse graph struct file.")
    graph_struct_file = os.path.join(data_dir, graph_struct_file_name)
    graph_struct_scripts = []
    with open(graph_struct_file, 'r') as f:
        graph_struct_json = json.load(f)
        log.info(json.dumps(graph_struct_json, indent=4))

        graph_name = graph_struct_json[graph_name_key]
        create_graph_line = "graph = GridGraphFactory.createGraph('{}')".format(graph_name)
        log.info(create_graph_line)
        graph_struct_scripts.append(create_graph_line)

        primary_key = graph_struct_json[primary_key_key]
        create_primary_key_line = "graph.createPrimaryKey('{}')".format(primary_key)
        log.info(create_primary_key_line)
        graph_struct_scripts.append(create_primary_key_line)

        schemas = graph_struct_json[schemas_key]
        for schema in schemas:
            create_schema_line = "{}Schema = graph.createSchema('{}', SchemaType.{})" \
                .format(schema[name_key], schema[name_key], schema[type_key].upper())
            log.info(create_schema_line)
            graph_struct_scripts.append(create_schema_line)
            if schema[type_key].upper() == VERTEX:
                VERTEX_SCHEMA_PROPERTY_TYPE[schema[name_key]] = {}
            elif schema[type_key].upper() == EDGE:
                EDGE_SCHEMA_PROPERTY_TYPE[schema[name_key]] = {}
            else:
                log.error("schema type error. [type=%s]", schema[type_key].upper())
                raise TypeError("schema type error.")

            properties = schema[properties_key]
            for property in properties:
                if schema[type_key].upper() == VERTEX:
                    VERTEX_SCHEMA_PROPERTY_TYPE[schema[name_key]][property[name_key]] = property[type_key]
                else:
                    EDGE_SCHEMA_PROPERTY_TYPE[schema[name_key]][property[name_key]] = property[type_key]

                if property[name_key] == primary_key:
                    continue
                create_property_line = "{}Schema.createProperty('{}', GridDataType.{}, {}, {}, null)" \
                    .format(schema[name_key], property[name_key], property[type_key], str(property[unique_key]).lower(),
                            str(property[nullable_key]).lower())
                log.info(create_property_line)
                graph_struct_scripts.append(create_property_line)

        indexs = graph_struct_json[indexs_key]
        for index in indexs:
            index_name = index[index_name_key]
            property_index = index[property_indexs_key][0]
            create_index_line = 'graph.createIndex("{}", "{}", "{}", IndexSortDirection.{})'.format(
                index_name, property_index[schema_name_key], property_index[property_name_key],
                property_index[direction_key].upper())
            graph_struct_scripts.append(create_index_line)
            log.info(create_index_line)

    graph_struct_scripts.append("graph.tx().commit()")
    log.info(json.dumps(VERTEX_SCHEMA_PROPERTY_TYPE, indent=4))
    log.info(json.dumps(EDGE_SCHEMA_PROPERTY_TYPE, indent=4))
    ret = ';'.join(graph_struct_scripts)
    log.info(ret)
    return ret


def parse_bulk_load_csv_mapping_file(data_dir):
    log.info("parse bulk load csv mapping file")
    bulk_load_csv_file = os.path.join(data_dir, bulk_load_csv_file_name)
    with open(bulk_load_csv_file, 'r') as f:
        bulk_load_csv_json = json.load(f)
        log.info(json.dumps(bulk_load_csv_json, indent=4))

        GRAPH_INFO[graph_name_key] = bulk_load_csv_json[graph_name_key]
        GRAPH_INFO[primary_key_key] = bulk_load_csv_json[primary_key_key]
        GRAPH_INFO[csv_splitter_char_key] = bulk_load_csv_json[connection_key][csv_splitter_char_key]
        vertice = bulk_load_csv_json[vertexes_key]
        for v in vertice:
            VERTEX_SCHEMA_TO_CSV[v[schema_name_key]] = v[file_name_key]
            VERTEX_SCHEMA_FIELDS[v[schema_name_key]] = list(v[field_map_key].keys())
        edges = bulk_load_csv_json[edges_key]
        for e in edges:
            EDGE_SCHEMA_TO_CSV[e[schema_name_key]] = e[file_name_key]
            EDGE_SCHEMA_FIELDS[e[schema_name_key]] = list(e[field_map_key].keys())
            from_to_vertex = dict()
            from_to_vertex[from_vertex_key] = e[from_vertex_key]
            from_to_vertex[to_vertex_key] = e[to_vertex_key]
            EDGE_FROM_TO_VERTEX[e[schema_name_key]] = from_to_vertex
    log.info(GRAPH_INFO)
    log.info(VERTEX_SCHEMA_TO_CSV)
    log.info(VERTEX_SCHEMA_FIELDS)
    log.info(EDGE_SCHEMA_TO_CSV)
    log.info(EDGE_SCHEMA_FIELDS)
    log.info(EDGE_FROM_TO_VERTEX)


def parse_data_file(data_dir) -> list:
    log.info("parse data file...")
    log.info("parse vertex csv")

    add_data_scripts = list()
    step = 5


    add_vertex_scripts = list()
    log.info(VERTEX_SCHEMA_TO_CSV)
    for k, v in VERTEX_SCHEMA_TO_CSV.items():
        fields = VERTEX_SCHEMA_FIELDS[k]
        file = join(data_dir, v)
        with open(file, "r", encoding="utf-8", newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                i = 0
                add_vertex_line = 'graph.addVertex(T.label, "{}"'.format(k)
                for e in row:
                    line_part = generate_add_data_line(VERTEX, k, fields[i], row[i])
                    add_vertex_line += ', "{}", {}'.format(fields[i], line_part)
                    i = i + 1
                add_vertex_line += ')'
                log.info(add_vertex_line)
                add_vertex_scripts.append(add_vertex_line)
                # add_data_scripts.append(add_vertex_line)


    add_v_scripts_group = [add_vertex_scripts[i:i + step] for i in range(0, len(add_vertex_scripts), step)]
    log.info("V scripts group:\n %s", add_v_scripts_group)
    for g in add_v_scripts_group:
        start = "graph = GridGraphFactory.openGraph('{}')".format(GRAPH_INFO[graph_name_key])
        add_data_scripts.append(start + ';' + ';'.join(g) + ';' + "graph.tx().commit()")

    # traversal_line = "g=graph.traversal()"
    # add_data_scripts.append(traversal_line)
    # log.info(traversal_line)


    add_edge_scripts = list()
    for k, v in EDGE_SCHEMA_TO_CSV.items():
        fields = EDGE_SCHEMA_FIELDS[k]
        file = join(data_dir, v)
        with open(file, "r", encoding="utf-8", newline='') as f:
            reader = csv.reader(f)
            for row in reader:

                add_edge_line = "g.V().has('{}','{}','{}').next().addEdge('{}', g.V().has('{}','{}','{}').next()".format(
                    EDGE_FROM_TO_VERTEX[k][from_vertex_key], GRAPH_INFO[primary_key_key], row[0], k,
                    EDGE_FROM_TO_VERTEX[k][to_vertex_key], GRAPH_INFO[primary_key_key], row[1])

                # log.info(row)
                if len(row) > 2:
                    i = 0
                    for e in row:
                        if i < 2:
                            i = i + 1
                            continue
                        # log.info(row[i])
                        line_part = generate_add_data_line(EDGE, k, fields[i], row[i])
                        # log.info(line_part)
                        add_edge_line += ", '{}', {}".format(fields[i], line_part)
                        # log.info(add_edge_line)
                        i = i + 1
                add_edge_line += ')'
                # add_data_scripts.append(add_edge_line)
                add_edge_scripts.append(add_edge_line)
                log.info(add_edge_line)

    add_e_scripts_group = [add_edge_scripts[i:i + step] for i in range(0, len(add_edge_scripts), step)]
    log.info("E scripts group:\n %s", add_e_scripts_group)
    for g in add_e_scripts_group:
        start = "graph = GridGraphFactory.openGraph('{}');g=graph.traversal()".format(GRAPH_INFO[graph_name_key])
        add_data_scripts.append(start + ';' + ';'.join(g) + ';' + "graph.tx().commit()")

    # add_data_scripts.append("graph.tx().commit()")
    # ret = ';'.join(add_data_scripts)
    log.info(add_data_scripts)
    return add_data_scripts


def generate_add_data_line(schema_type, schema_name, property_name, property_value) -> str:
    if schema_type == VERTEX:
        p_type_info = VERTEX_SCHEMA_PROPERTY_TYPE[schema_name]
    else:
        p_type_info = EDGE_SCHEMA_PROPERTY_TYPE[schema_name]

    if p_type_info[property_name] == 'STRING':
        return "'{}'".format(property_value)
    elif p_type_info[property_name] == 'DOUBLE':
        return '{}d'.format(property_value)
    elif p_type_info[property_name] == 'FLOAT':
        return '{}f'.format(property_value)
    else:
        return '{}'.format(property_value)


if __name__ == '__main__':
    # cl = GremlinClient("127.0.0.1", 8381, "admin", "admin")
    # script = "graph = GridGraphFactory.listGraph();"
    # cl.send_gremlin_script(script)

    import_csv_data("127.0.0.1", 8381, '/Users/hetao/work/gridgraph/bulkload/bulkload/standalone/strong-schema')
