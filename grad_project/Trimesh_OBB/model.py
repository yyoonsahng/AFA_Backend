import numpy as np
import trimesh


class OBB:
    def __init__(self):
        self.local_axis = None
        self.obb = None

    def build(self, filename):
        trimesh.util.attach_to_log()
        mesh = trimesh.load_mesh(filename)

        # translate object to origin of world coordinate
        mesh.apply_translation(translation=(-mesh.centroid))
        box = mesh.bounding_box_oriented
        self.get_local_axis(box)

        # rotate by transformation matrix
        matrix = [np.append(self.local_axis[0], 0), np.append(self.local_axis[1], 0), np.append(self.local_axis[2], 0), np.array([0, 0, 0, 1])]
        mesh.apply_transform(matrix)

        self.obb = mesh.bounding_box_oriented
        return mesh

    def get_local_axis(self, box):
        x_axis = (box.vertices[2] - box.vertices[0])
        y_axis = (box.vertices[1] - box.vertices[0])
        z_axis = (box.vertices[4] - box.vertices[0])

        self.local_axis = [self.get_unit(x_axis), self.get_unit(y_axis), self.get_unit(z_axis)]
        return self.local_axis

    @classmethod
    def get_unit(cls, v):
        return v / np.linalg.norm(v)


# def main():
#     obb = OBB()
#     mesh = obb.build('04.jpg.off')
#
#     dl = pyrender.DirectionalLight(color=[1.0, 1.0, 1.0], intensity=3.0)
#     scene = pyrender.Scene()
#     scene.add_node(pyrender.Node(light=dl, matrix=np.eye(4)))
#
#     scene = trimesh.Scene(geometry=mesh)
#     gl = gltf.export_gltf(scene, merge_buffers=True)
#     dict_str = gl['model.gltf'].decode("UTF-8")
#     scene.add(pyrender.Mesh.from_trimesh(mesh))
#     scene.add(pyrender.Mesh.from_trimesh(obb.obb))
#     pyrender.Viewer(scene)
#
#
# if __name__ == '__main__':
#     main()
