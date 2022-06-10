import os


# generating dockerfiles for each node excepting databases (we take ready-to-use images of databases from dockerhub)
def generate_dockerfiles(nodes):
    for node in nodes.nodelist:
        if node.node_type != 'database':
            node.create_dockerfile()
            node.set_image_name(node.name + ':latest')
    return True


# generating docker images for each node excepting databases (we take ready-to-use images of databases from dockerhub)
def generate_images(nodes):
    for node in nodes.nodelist:
        if node.node_type != 'database':
            os.system('docker build --tag ' + node.image_name + ' ' + node.path)
    return True
