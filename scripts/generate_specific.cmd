@echo off
set dataDir=data
set trainDir=test

REM Danh sách các category cần xử lý
set categories=applicance comic_book

REM Duyệt qua các thư mục asin-id trong từng category
for %%C in (%categories%) do (
    for /d %%A in (%trainDir%\%%C\*) do (
        echo Found directory: %%A
        echo Processing %%A
        python test_pretrained.py ^
            --name pretrained ^
            --dataset_mode test_dir ^
            --dataroot %%A ^
            --results_dir %%A ^
            --checkpoints_dir %dataDir%\Exp\PhotoSketch\Checkpoints\ ^
            --model pix2pix ^
            --which_direction AtoB ^
            --norm batch ^
            --input_nc 3 ^
            --output_nc 1 ^
            --which_model_netG resnet_9blocks ^
            --no_dropout
    )
)
pause
