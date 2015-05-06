__author__ = 'tieni'


class SegObject:
    def __init__(self, obj_id=None, todo=None, immutable=None, position=None, supervoxels=None, category="", comment=""):
        self.id = obj_id
        self.todo = todo
        self.immutable = immutable
        self.pos = [] if position is None else position
        self.category = category
        self.comment = comment
        self.supervoxels = set() if supervoxels is None else supervoxels

    def __str__(self):
        return "object {0} at {1}: {2}".format(self.id, self.pos, self.supervoxels)


class Mergelist:
    def __init__(self, mergelist_path=None):
        self.seg_objects = []
        self.seg_subobjects = {}  # dict subobjectID : set of objectIDs
        self.max_object_id = 0

        if mergelist_path is None:
            return
        try:
            with open(mergelist_path, 'r') as txt:
                self.read(txt.read())
        except IOError:
            print("Could not open " + mergelist_path)

    def count_comment(self, comment):
        count = 0
        for seg_obj in self.seg_objects:
            if seg_obj.comment == comment:
                count += 1
        return count

    def number_todos(self):
        count = 0
        for seg_obj in self.seg_objects:
            count += 1 if seg_obj.todo else 0
        return count

    def contained_in(self, sub_id):
        try:
            return self.seg_subobjects[sub_id]
        except KeyError:
            return set()

    def are_merged(self, id1, id2):
        for seg_obj in self.seg_objects:
            if id1 in seg_obj.supervoxels and id2 in seg_obj.supervoxels:
                return True
        return False

    def add_object(self, todo, immutable, position, initial_subobjects, category="", comment=""):
        self.max_object_id += 1
        self.seg_objects.append(SegObject(self.max_object_id, todo, immutable, position, initial_subobjects, category, comment))
        for subobject in initial_subobjects:
            self.seg_subobjects[subobject] = self.max_object_id

    def read(self, stream):
        if stream is None or stream is False:
            print("stream invalid")
            return
        index = 0
        obj_id = None; todo = None; immutable = None; supervoxels = set(); coord = []; category = None
        for line in stream.split('\n'):
            if index == 0:
                content = line.split()
                if len(content) < 4:
                    break
                obj_id = int(content[0])
                todo = True if content[1] == "1" else False
                immutable = True if content[2] == "1" else False
                supervoxels = {int(sub_id) for sub_id in content[3:]}
                for supervoxel in supervoxels:
                    try:
                        self.seg_subobjects[supervoxel].add(obj_id)
                    except KeyError:
                        self.seg_subobjects[supervoxel] = {obj_id}
            if index == 1:
                coord = [int(coordinate) for coordinate in line.split()]
            if index == 2:
                category = line
            if index == 3:
                comment = line
                self.seg_objects.append(SegObject(obj_id, todo, immutable, coord, supervoxels, category, comment))
                index = 0
                continue
            index += 1

    def write(self, absolute_path):
        with open(absolute_path, 'w') as mergelist:
            for seg_obj in self.seg_objects:
                mergelist.write("{0} {1} {2} {3}\n{4}\n{5}\n{6}\n"
                                .format(seg_obj.id, 1 if seg_obj.todo else 0, 1 if seg_obj.immutable else 0,
                                        ' '.join([str(voxel) for voxel in seg_obj.supervoxels]),
                                        ' '.join([str(coord) for coord in seg_obj.pos]),
                                        seg_obj.category,
                                        seg_obj.comment))