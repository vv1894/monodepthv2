kitti_data = /media/ryan/ldata/monodepth2/kitti_data

convert command:
find /media/ryan/ldata/monodepth2/kitti_data/ -name '*.png' | parallel 'convert -quality 92 -sampling-factor 2x2,1x1,1x1 {.}.png {.}.jpg && rm {}'

train with correct path
try 1
python train.py --model_name mono_model --data_path /media/ryan/ldata/monodepth2/kitti_data --batch_size 4 --num_epochs 2 --post_process
try 2
python train.py --model_name mono_model_1 --data_path /media/ryan/ldata/monodepth2/kitti_data --batch_size 4 --num_epochs 6 --post_process
try3
python train.py --model_name mono_model_2 --data_path /media/ryan/ldata/monodepth2/kitti_data --batch_size 6 --num_epochs 10

try4
python train.py --model_name mono_model_320x96 --data_path /media/ryan/ldata/project/kitti_data --batch_size 16 --log_dir ./log --num_workers 6 --num_epochs 1 --width 320 --height 96

new_data
python train.py --model_name mono_model_320x96_tryyy --data_path /media/ryan/ldata/project/kitti_data --batch_size 8 --log_dir ./log --num_workers 6 --num_epochs 2 --width 320 --height 96 --save_copy

finishrun
python train.py --model_name mono_model_320x96_final --data_path /media/ryan/ldata/project/kitti_data --batch_size 8 --log_dir ./log --num_workers 6 --width 320 --height 96

prepare ground truth m
python export_gt_depth.py --data_path /media/ryan/ldata/monodepth2/kitti_data --split eigen
python export_gt_depth.py --data_path /media/ryan/ldata/monodepth2/kitti_data --split eigen_benchmark


finetuning
python train.py --model_name finetuned_mono --load_weights_folder ~/tmp/mono_model/models/weights_1 --batch_size 4 --num_epochs 4 --data_path /media/ryan/ldata/monodepth2/kitti_data


evaluate
python evaluate_depth.py --load_weights_folder ~/tmp/mono_model/models/weights_1/ --data_path /media/ryan/ldata/monodepth2/kitti_data --eval_mono 

python evaluate_depth.py --load_weights_folder ~/tmp/mono_model_1/models/weights_5/ --data_path /media/ryan/ldata/monodepth2/kitti_data --eval_mono 

python evaluate_depth.py --load_weights_folder ~/tmp/finetuned_mono/models/weights_3 --data_path /media/ryan/ldata/monodepth2/kitti_data --eval_mono 

python evaluate_depth.py --load_weights_folder ~/文档/coding/monodepth2/log/mono_model_320x92/models/weights_9 --data_path /media/ryan/ldata/monodepth2/kitti_data --eval_mono

python evaluate_depth.py --load_weights_folder models/mono_model_320x96_labeled/models/weights_9 --data_path /media/ryan/ldata/monodepth2/kitti_data --eval_mono



test

python test_simple.py --image_path assets/p1.jpeg --model_name mono_self

python test_simple.py --image_path assets/p1.jpeg assets/p2.jpeg --model_name mono_self_ftd

python test_simple.py --image_path assets/p1.jpeg --model_name mono_epoch_6

python test_simple.py --image_path assets/test --model_name mono_model_320x96 --ext jpeg

# generate pcd
python depth2pcd.py --rgb_path assets/test_1.png --dpt_path assets/test_1_disp.png --output_path output_1.ply