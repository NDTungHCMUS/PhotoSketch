@echo off
set dataDir=data
set trainDir=train

REM Duyệt qua tất cả các thư mục asin-id trong train/<category>/<asin-id>/
for /d %%C in (%trainDir%\*) do (
    for /d %%A in (%%C\*) do (
        echo Processing %%A
        python test_pretrained.py ^
            --name pretrained ^
            --dataset_mode test_dir ^
            --dataroot %%A ^
            --results_dir %%A\ ^
            --checkpoints_dir %dataDir%\Exp\PhotoSketch\Checkpoints\ ^
            --model pix2pix ^
            --which_direction AtoB ^
            --norm batch ^
            --input_nc 3 ^
            --output_nc 1 ^
            --which_model_netG resnet_9blocks ^
            --no_dropout ^
    )
)
