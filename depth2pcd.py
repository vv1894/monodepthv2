# 转换需要depth图像和rgb图像尺寸一致，若不一致需要先resize成一样的大小
from PIL import Image
# img = Image.open('./depth.png')
# resized_img = img.resize((1600, 1184))
# resized_img.save('./depth.png')

import argparse
import open3d as o3d
import matplotlib.pyplot as plt
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser(
        description='Simple testing funtion for Monodepthv2 models.')

    parser.add_argument('--rgb_path', type=str,
                        help='path to a origin test image', required=True)
    parser.add_argument('--dpt_path', type=str,
                        help='path to a origin depth image', required=True)
    parser.add_argument('--data_dir', type=str,
                        help='directory of tested data', required=False)
    parser.add_argument('--output_path', type=str,
                        help='output path', required=True)

    return parser.parse_args()

def d2p(args):
    rgb_path = args.rgb_path
    depth_path = args.dpt_path

    intrinsic = o3d.core.Tensor([[9.591977e2, 0, 6.944383e2], [0, 9.529324e2, 2.416793e2],
                                    [0, 0, 1]])

    color_raw = o3d.io.read_image(rgb_path)
    depth_raw = o3d.io.read_image(depth_path)
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(color_raw, depth_raw, depth_scale=3000.0, depth_trunc=10, convert_rgb_to_intensity=False)
    # plt.subplot(1, 2, 1)
    # plt.title('read_depth')
    # plt.imshow(rgbd_image.color)
    # plt.subplot(1, 2, 2)
    # plt.title('depth image')
    # plt.imshow(rgbd_image.depth)
    # plt.show()

    # 若要查看自己的深度图值是多少，使用下面的np函数显示
    # print(np.asarray(rgbd_image.depth))

    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, o3d.camera.PinholeCameraIntrinsic(
        o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault))
    pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    # o3d.visualization.draw_geometries([pcd])
    # o3d.io.write_point_cloud('./output.ply', pcd)

    # 翻转点云以纠正左右颠倒的问题
    pcd.estimate_normals()
    pcd = pcd.transform(np.array([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]))  # 绕X轴旋转180度
    pcd.estimate_normals()

    # 绘制和保存点云
    # o3d.visualization.draw_geometries([pcd])
    filename = args.output_path
    o3d.io.write_point_cloud(filename, pcd)
    print(f"PCD {filename} Successfully saved!")

if __name__ == '__main__':
    args = parse_args()
    d2p(args)
