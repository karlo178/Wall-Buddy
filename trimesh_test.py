# install trimesh: pip install trimesh
import trimesh
# I assume you know numpy
import numpy as np


# this func helps export the point cloud as a ply file
def export_ply(out, v):
    with open(out, 'w') as fout:
        fout.write('ply\n');
        fout.write('format ascii 1.0\n');
        fout.write('element vertex '+str(v.shape[0])+'\n');
        fout.write('property float x\n');
        fout.write('property float y\n');
        fout.write('property float z\n');
        fout.write('end_header\n');

        for i in range(v.shape[0]):
            fout.write('%f %f %f\n' % (v[i, 0], v[i, 1], v[i, 2]))

# load STL file: check documentation https://trimsh.org/trimesh.html
# it should also support loading the other file formats
mesh = trimesh.load('cadobjectbypeter.stl')

# number of point we finally want to sample
N = 10000

# mesh vertices
print(mesh.vertices.shape)

# mesh faces (starting from 0)
print(mesh.faces.shape)
print(np.max(mesh.faces), np.min(mesh.faces))

# randomly sample points from the surface (This is not Furthest-point-sampling, 
# but when points are dense enough, it should also work)
pc, _ = trimesh.sample.sample_surface(mesh=mesh, count=3*N)
print(pc.shape) # 30000 x 3
# you can also use the other relevant funcs (check: https://trimsh.org/trimesh.sample.html)
#pc, _ = trimesh.sample.sample_surface_even(mesh=mesh, count=10000) # this one generates more EVENLY

# export to file
# Download MeshLab to visualize ply files: https://www.meshlab.net/
export_ply('cadobjectbypeter_random.ply', pc)


# here starts Furthest-point-sampling (It implements a greedy algorithm that start from picking one random point,
# and then iteratively add a new point that is furthest from the set of already picked points.)
# FPS: input is a point cloud, output is a subset of the point cloud
# FPS sampled point cloud is more evenly sampled on the surface than randomly sampled point cloud
# What we usually do is to first sample 3N points using random sampling, then FPS downsample to N points, so the final N points are evenly sampled

# we use pytorch here
import torch
# install https://github.com/erikwijmans/Pointnet2_PyTorch
# first, git clone --recursive https://github.com/erikwijmans/Pointnet2_PyTorch
# then, comment these two lines of code: [THIS IS IMPORTANT!]
#       https://github.com/erikwijmans/Pointnet2_PyTorch/blob/master/pointnet2_ops_lib/pointnet2_ops/_ext-src/src/sampling_gpu.cu#L100-L101
# then, pip install -r requirements.txt
# then, pip install -e .
# you are done. It is installed.
from pointnet2_ops.pointnet2_utils import furthest_point_sample

# This support batch operation
pc = torch.from_numpy(pc).unsqueeze(dim=0).float().to('cuda:0')     # pc: 1 x 3N x 3, on GPU

# input pc: B x 3N x 3 (float), output: B x N (int), here B = 1, but you can use GPU to run for multiple shapes with B > 1
idx = furthest_point_sample(pc, N)

# get the result
pc = pc[0, idx[0].long(), :].cpu().numpy()
print(pc.shape) # 10000 x 3

# export ply
export_ply('cadobjectbypeter_fps.ply', pc)