# %% ------------------------------------------------------------------------------------
import sys
import os
sys.path.insert(0, os.path.realpath(os.path.pardir))
import dnnlib
import numpy as np
import PIL.Image
import legacy
import torch
import uuid
import glob

# %% ------------------------------------------------------------------------------------
# checkpoint_path = '../ffhq.pkl'
checkpoint_path = 'https://nvlabs-fi-cdn.nvidia.com/stylegan2-ada-pytorch/pretrained/ffhq.pkl'
output_dir = '../output'
device = torch.device('cuda')


# %% ------------------------------------------------------------------------------------
print('Loading networks from "%s"...' % checkpoint_path)
with dnnlib.util.open_url(checkpoint_path) as f:
    G = legacy.load_network_pkl(f)['G_ema'].to(device)  # type: ignore

# os.makedirs(output_dir, exist_ok=True)


# %% ------------------------------------------------------------------------------------
def load_replace_projection(proj_a, proj_b, idx_to_swap=slice(0, 3)):
    ws_a = np.load(proj_a)['w']
    ws_b = np.load(proj_b)['w']
    ws_a[0, idx_to_swap, :] = ws_b[0, idx_to_swap, :]
    return ws_a


# %% ------------------------------------------------------------------------------------
def generate_from_projection(projection):
    if type(projection).__module__ != np.__name__:
        ws = np.load(projection)['w']
    else:
        ws = projection

    ws = torch.tensor(ws, device=device).squeeze(0)
    img = G.synthesis(ws.unsqueeze(0), noise_mode='const')
    img = (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)

    img = PIL.Image.fromarray(img[0].cpu().numpy(), 'RGB')
    return img


# %% ------------------------------------------------------------------------------------
def generate_from_seed(seed):
    label = torch.zeros([1, G.c_dim], device=device)

    z = torch.from_numpy(np.random.RandomState(seed).randn(1, G.z_dim)).to(device)
    img = G(z, label, truncation_psi=1.0, noise_mode='const')
    img = (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)

    img = PIL.Image.fromarray(img[0].cpu().numpy(), 'RGB')
    return img


# %% ------------------------------------------------------------------------------------
if __name__ == "__main__":
    #     for i in range(20):
    #         generate_from_seed(np.random.randint(0, 1000))

    # z = load_replace_projection('z_output/z_0849.npz', 'z_output/z_0085.npz')

    z_out = glob.glob('../z_output/*.npz')
    for z in z_out:
        _z = np.load(z)['w']
        img = generate_from_projection(_z)
        fname = f"{z.split('/')[-1].split('.')[0]}.jpg"
        img.save(f"../images/{fname}")
