import os


def boterham_load_model(filename):
    root = loader.load_model(filename)

    # Load links
    # TODO: Make recursive
    loaded = {}
    for child in root.find_all_matches('**/=__linked_file'):
        path = child.get_tag('__linked_file')
        path = os.path.dirname('./'+filename)+path
        nodename = child.get_tag('__linked_node')
        if path in loaded:
            file = loaded[path]
        else:
            file = loaded[path] = loader.load_model(path)
        node = file.find('**/'+nodename)
        instance = node.copy_to(child.parent)
        instance.set_transform(child.get_transform())
        child.detach_node()

    # Setup heightmap
    pass

    return root
