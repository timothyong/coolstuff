def importfile(filename, sx, sy, sz, rx, ry, rz, mx, my, mz):
    f = open(filename,'r')
    l = f.readlines()
    i = 0
    length = 0
    while i < len(l):
        i = i + 1
        line = l.readline()
        parts = line.split()
        if len(parts) == 1:
            length = parts[0]
            i = 0
            break
    importtrig = []
    while i < length:
        line = l.readline()
        parts = line.split()
        importtrig = add_triangle([parts[0], parts[1], parts[2], 1],
                                  [parts[3], parts[4], parts[5], 1],
                                  [parts[6], parts[7], parts[8], 1],
                                  importtrig)
        i = i + 1
    importtrig = transform(scale(sx, sy, sz, matrix.create_identity_matrix()), box_triangles)
    importtrig = transform(rotate_x(rx, matrix.create_identity_matrix()), importtrig)
    importtrig = transform(rotate_y(ry, matrix.create_identity_matrix()), importtrig)
    importtrig = transform(rotate_z(rz, matrix.create_identity_matrix()), importtrig)
    importtrig = transform(move(mx, my, mz, matrix.create_identity_matrix()), importtrig)
    importtrig = transform(trans_matrix, importtrig)
    triangle_matrix = triangle_matrix + importtrig
