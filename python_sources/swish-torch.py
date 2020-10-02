ALL = ['Swish','SwishFunction','swish','__version__']
from base64 import b64decode
from zlib import decompress
import torch
from torch.utils.cpp_extension import load_inline

__version__='0.0.1'

def load_module():
    cpp_comp = ['eNrNVE2P2jAQvedXjKiEQkXJcg3blShQ7apdqApI7SkyzkAsQhz5g+1utf+9jhNDUmBbtT30BPHMvPdm/DxeEMB7wXcQJHyHgZYoghj3gXxgMnmjuKBJQKWg5UGP5rnnea9YRlMdI1yXCfhNYSYZz3rJjaclyzaQkR3KnFCE/HHFsrjfD8OUKRQklQPPK1i5eCAihhhpSgRRphz4GrYoMkylt+csBksarcvMiOqY+JYxDBeGkAtoc61yrbpAeSYV/BRkmYl1BnWsFaHbi2AbQeLIFL0EdyFmS7ll8xohr9GD/2tgosKQ58U4SHrdSLyBggC+ewBEKw62LCJiA2+biEOx8SvMlv1tdeHKKANga/APIBUMvwzymlsMbhH6FgFcFk2QbufmmhePOfqtRpsm+yCu6wgulM/Z0++XP7veuZFrAr09STVGXLirxF2uHqOUbbGcQMeWGXRFEyiPesbfjKLf6alCeccNgxKJQPtXYbgdLcfD0B7COQ/ySl/VEcBKINmWHzGuiU6Vq17MPo9uo9HtZPTBXxvvoxnnMpM6z7lQWLi/0AKFki7IhOs0hhVCIQBWWsGGK3DjOBHuJiJQaWFez8B7Pu8+53r/z339V7azdQ7qUqmLm2r39+C6lzznmmu6ps5WPMq6CJN2FHDimH9jmOaiOW6WakC1ffE/WcjptE769PXd3XTc70f3s/Hy48QvhUy+LCbT+d1sGk2H95Mu7Mpx7Az0+vQdtxsHRvm8+AZCFduXO/+YW5kmItXKiYi5pUynaa6EFdrgqF17u3lyjqWWXac5GC0inaLnH0CgXH0=']
    cu_comp  = ['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']
    cpp_srcs = [decompress(b64decode(src)).decode() for src in cpp_comp]
    cu_srcs = [decompress(b64decode(src)).decode() for src in cu_comp]

    swish_mod = load_inline("swish_torch_inline", cpp_sources=cpp_srcs, cuda_sources=cu_srcs, extra_cuda_cflags=['--expt-extended-lambda'])
    return swish_mod

if not torch.cuda.is_available():
    print("CUDA not available but is required for swish_torch")
    swish_mod = None
else:
     swish_mod = load_module()

class SwishFunction(torch.autograd.Function):
    @staticmethod
    def forward(ctx, inp):
        ctx.save_for_backward(inp)
        return swish_mod.swish_forward(inp)
    
    @staticmethod
    def backward(ctx, grad_out):
        inp, = ctx.saved_tensors
        if not ctx.needs_input_grad[0]: return (None,)
        return swish_mod.swish_backward(inp, grad_out)
        
class Swish(torch.nn.Module):
    '''Swish Activation Function - Inline PyTorch CUDA Version'''
    def forward(self, inp): return SwishFunction.apply(inp)

swish = SwishFunction.apply

if swish_mod is not None:
    print(f"Successfully loaded swish-torch inline version {__version__}")