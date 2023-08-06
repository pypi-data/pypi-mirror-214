import os

import gradio as gr
import torch
from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.archs.srvgg_arch import SRVGGNetCompact
from gfpgan.utils import GFPGANer
from huggingface_hub import hf_hub_download
from realesrgan.utils import RealESRGANer

REALESRGAN_REPO_ID = 'leonelhs/realesrgan'
GFPGAN_REPO_ID = 'leonelhs/gfpgan'

os.system("pip freeze")


def showGPU():
    if torch.cuda.is_available():
        devices = torch.cuda.device_count()
        current = torch.cuda.current_device()
        return f"Running on GPU:{current} of {devices} total devices"
    return "Running on CPU"


def download_model_gfpgan(file):
    return hf_hub_download(repo_id=GFPGAN_REPO_ID, filename=file)


def download_model_realesrgan(file):
    return hf_hub_download(repo_id=REALESRGAN_REPO_ID, filename=file)


def select_upsampler(version, netscale=4):
    model = None
    dni_weight = None

    version = version + ".pth"
    model_path = download_model_realesrgan(version)

    if version == 'RealESRGAN_x4plus.pth':  # x4 RRDBNet model
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)

    if version == 'RealESRNet_x4plus.pth':  # x4 RRDBNet model
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)

    if version == 'AI-Forever_x4plus.pth':  # x4 RRDBNet model
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)

    if version == 'RealESRGAN_x4plus_anime_6B.pth':  # x4 RRDBNet model with 6 blocks
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4)

    if version == 'RealESRGAN_x2plus.pth':  # x2 RRDBNet model
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
        netscale = 2  # This is

    if version == 'AI-Forever_x2plus.pth':  # x2 RRDBNet model
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
        netscale = 2  # This is

    if version == 'realesr-animevideov3.pth':  # x4 VGG-style model (XS size)
        model = SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=16, upscale=4, act_type='prelu')

    if version == 'realesr-general-x4v3.pth':  # x4 VGG-style model (S size)
        model = SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=32, upscale=4, act_type='prelu')
        model_path = [
            download_model_realesrgan("realesr-general-x4v3.pth"),
            download_model_realesrgan("realesr-general-wdn-x4v3.pth")
        ]
        dni_weight = [0.2, 0.8]

    half = True if torch.cuda.is_available() else False

    return RealESRGANer(
        scale=netscale,
        model_path=model_path,
        dni_weight=dni_weight,
        model=model,
        tile=0,
        tile_pad=10,
        pre_pad=0,
        half=half,
        gpu_id=0)


def select_face_enhancer(version, scale, upsampler):
    if 'v1.2' in version:
        model_path = download_model_gfpgan('GFPGANv1.2.pth')
        return GFPGANer(
            model_path=model_path, upscale=scale, arch='clean', channel_multiplier=2, bg_upsampler=upsampler)
    elif 'v1.3' in version:
        model_path = download_model_gfpgan('GFPGANv1.3.pth')
        return GFPGANer(
            model_path=model_path, upscale=scale, arch='clean', channel_multiplier=2, bg_upsampler=upsampler)
    elif 'v1.4' in version:
        model_path = download_model_gfpgan('GFPGANv1.4.pth')
        return GFPGANer(
            model_path=model_path, upscale=scale, arch='clean', channel_multiplier=2, bg_upsampler=upsampler)
    elif 'RestoreFormer' in version:
        model_path = download_model_gfpgan('RestoreFormer.pth')
        return GFPGANer(
            model_path=model_path, upscale=scale, arch='RestoreFormer', channel_multiplier=2, bg_upsampler=upsampler)


def predict(image, version_upsampler, version_enhancer, scale):
    scale = int(scale)

    upsampler = select_upsampler(version_upsampler)

    if "No additional" not in version_enhancer:
        face_enhancer = select_face_enhancer(version_enhancer, scale, upsampler)
        _, _, output = face_enhancer.enhance(image, has_aligned=False, only_center_face=False, paste_back=True)
    else:
        output, _ = upsampler.enhance(image, outscale=scale)

    log = f"General enhance version: {version_upsampler}\n " \
          f"Face enhance version: {version_enhancer} \n " \
          f"Scale:{scale} \n {showGPU()}"

    return output, log


title = "Super Face"
description = r"""
<b>Practical Image Restoration Algorithm based on Real-ESRGAN, GFPGAN</b>
"""
article = r"""
<center><span>xintao.wang@outlook.com or xintaowang@tencent.com</span></center>
</br>
<center><a href='https://github.com/TencentARC/GFPGAN' target='_blank'>Github Repo ⭐ </a> are welcome</center>
"""

app = gr.Interface(
    predict, [
        gr.Image(type="numpy", label="Input"),
        gr.Dropdown([
            'RealESRGAN_x2plus',
            'RealESRGAN_x4plus',
            'RealESRNet_x4plus',
            'AI-Forever_x2plus',
            'AI-Forever_x4plus',
            'RealESRGAN_x4plus_anime_6B',
            'realesr-animevideov3',
            'realesr-general-x4v3'],
            type="value", value='RealESRGAN_x4plus', label='General restoration algorithm', info="version"),
        gr.Dropdown([
            'No additional face process',
            'GFPGANv1.2',
            'GFPGANv1.3',
            'GFPGANv1.4',
            'RestoreFormer'],
            type="value", value='No additional face process', label='Special face restoration algorithm',
            info="version"),
        gr.Dropdown(["1", "2", "3", "4"], value="2", label="Rescaling factor")
    ], [
        gr.Image(type="numpy", label="Output", interactive=False),
        gr.Textbox(label="log info")
    ],
    title=title,
    description=description,
    article=article)

